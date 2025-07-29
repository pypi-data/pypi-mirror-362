import os
from typing import Literal
import inspect
import shutil
import json
from dataclasses import dataclass, asdict
import numpy as np
import sktopt
from sktopt import tools
from sktopt.core.optimizers import common
from sktopt.core import derivatives, projection
from sktopt.core import visualization
from sktopt.mesh import visualization as visualization_mesh
from sktopt.fea import solver
from sktopt import filter
from sktopt.fea import composer
from sktopt.core import misc
from sktopt.tools.logconf import mylogger
logger = mylogger(__name__)


@dataclass
class Evolutionary_Config(common.DensityMethodConfig):
    interpolation: Literal["SIMP"] = "SIMP"
    population_size: int = 10
    offspring_size: int = 60
    # n_generations: int = 100
    mutation_strength_init: float = 0.2
    mutation_strength: float = 0.1
    mutation_strength_step: int = 3
    elite_size: int = 5
    penalty_weight: float = 1e4


def generate_initial_population(
    cfg: Evolutionary_Config,
    n_variables: int,
    vol_frac: float
):
    pop = np.random.rand(cfg.population_size, n_variables)
    # for loop in range(pop.shape[0]):
    #     pop[i][:] = self.helmholz_solver.filter(pop[loop])
    #     projection.heaviside_projection_inplace(
    #         pop[i], beta=beta, eta=cfg.beta_eta, out=pop[i]
    #     )
    enforce_volume_constraint_inplace(pop, n_variables, vol_frac)
    return pop


def enforce_volume_constraint(
    pop,
    n_variables: int,
    vol_frac: float
):
    # 各個体がvol_fracを満たすようにスケーリング
    return np.minimum(pop, 1.0) * (
        vol_frac * n_variables
    ) / np.maximum(pop.sum(axis=1, keepdims=True), 1e-8)


def enforce_volume_constraint_inplace(
    pop: np.ndarray,
    n_variables: int,
    vol_frac: float
):
    """
    In-place version of volume constraint enforcement.
    Scales each individual in `pop` to satisfy volume constraint.
    """
    # clip in-place: pop = min(pop, 1.0)
    np.clip(pop, 0.0, 1.0, out=pop)

    # compute scaling factors
    scale = (vol_frac * n_variables) / np.maximum(pop.sum(axis=1, keepdims=True), 1e-8)

    # apply scaling in-place
    pop *= scale


def mutate(x, mutation_strength, cfg):
    x += mutation_strength * np.random.randn(*x.shape)
    np.clip(x, cfg.rho_min, cfg.rho_max, out=x)
    return x


def mutate_from_parent(
    x: np.ndarray, out: np.ndarray,
    mutation_strength: float,
    cfg: Evolutionary_Config
):
    """
    mutation: out[:] = clip(x + noise, cfg.rho_min, cfg.rho_max)
    """
    np.add(x, mutation_strength * np.random.randn(*x.shape), out=out)
    np.clip(out, cfg.rho_min, cfg.rho_max, out=out)


class Evolutionary_Optimizer(common.DensityMethod):
    """
    """
    def __init__(
        self,
        cfg: Evolutionary_Config,
        tsk: sktopt.mesh.TaskConfig,
    ):
        super().__init__(cfg, tsk)
        self.recorder = self.add_recorder(tsk)

    def add_recorder(
        self, tsk: sktopt.mesh.TaskConfig
    ) -> tools.HistoriesLogger:
        recorder = tools.HistoriesLogger(self.cfg.dst_path)
        recorder.add("rho_projected", plot_type="min-max-mean-std")
        recorder.add("volume_violation", plot_type="min-max-mean-std")
        recorder.add("compliance", plot_type="min-max-mean-std", ylog=True)
        recorder.add("penalty", plot_type="min-max-mean-std", ylog=True)
        return recorder

    def init_schedulers(self, export: bool = True):

        cfg = self.cfg
        p_init = cfg.p_init
        vol_frac_init = cfg.vol_frac_init
        self.schedulers.add(
            "p",
            p_init,
            cfg.p,
            cfg.p_step,
            cfg.max_iters
        )
        self.schedulers.add(
            "vol_frac",
            vol_frac_init,
            cfg.vol_frac,
            cfg.vol_frac_step,
            cfg.max_iters
        )
        self.schedulers.add(
            "filter_radius",
            cfg.filter_radius_init,
            cfg.filter_radius,
            cfg.filter_radius_step,
            cfg.max_iters
        )
        self.schedulers.add(
            "mutation_strength",
            cfg.mutation_strength_init,
            cfg.mutation_strength,
            cfg.mutation_strength_step,
            cfg.max_iters
        )
        self.schedulers.add_object(
            tools.SchedulerStepAccelerating(
                "beta",
                cfg.beta_init,
                cfg.beta,
                cfg.beta_step,
                cfg.max_iters,
                cfg.beta_curvature,
            )
        )
        if export:
            self.schedulers.export()

    def parameterize(self):
        self.helmholz_solver = filter.HelmholtzFilter.from_defaults(
            self.tsk.mesh,
            self.cfg.filter_radius,
            solver_option="cg_pyamg",
            # solver_option=self.cfg.solver_option,
            dst_path=f"{self.cfg.dst_path}/data",
        )

    def load_parameters(self):
        self.helmholz_solver = filter.HelmholtzFilter.from_file(
            f"{self.cfg.dst_path}/data"
        )


    def initialize_params(self):
        tsk = self.tsk
        cfg = self.cfg
        rho, iter_begin, iter_end = self.initialize_density()
        n_variables = rho.shape[0]
        population_raw = generate_initial_population(
            cfg, n_variables, cfg.vol_frac_init
        )
        force_list = tsk.force if isinstance(tsk.force, list) else [tsk.force]
        u_dofs = np.zeros((tsk.basis.N, len(force_list)))
        return (
            iter_begin,
            iter_end,
            population_raw,
            n_variables,
            force_list,
            u_dofs
        )

    def get_compliance(
        self,
        rho,
        p,
        force_list,
        u_dofs,
        density_interpolation,
    ) -> float:
        rho_projected = rho
        compliance_avg = solver.compute_compliance_basis_multi_load(
            self.tsk.basis, self.tsk.free_dofs, self.tsk.dirichlet_dofs,
            force_list,
            cfg.E0, cfg.E_min, p, tsk.nu,
            rho_projected,
            u_dofs,
            elem_func=density_interpolation,
            solver=cfg.solver_option
        )

        return compliance_avg / len(force_list)

    
    def get_compliance_list(
        self,
        rho_list,
        p,
        force_list,
        density_interpolation,
        n_joblib
    ) -> float:
        
        compliance_avg_list, u_solutions_list = solver.compute_compliance_list_basis_multi_load(
            self.tsk.basis, self.tsk.free_dofs, self.tsk.dirichlet_dofs,
            force_list,
            cfg.E0, cfg.E_min, p, tsk.nu,
            rho_list,
            elem_func=density_interpolation,
            n_joblib=n_joblib,
            solver="spsolve"
        )

        return [
            compliance_avg / len(force_list) for compliance_avg in compliance_avg_list
        ]


    def get_strain_energy(
        self,
        rho,
        p,
        force_list,
        u_dofs,
        density_interpolation,
    ) -> float:
        rho_projected = rho
        strain_energy = composer.strain_energy_skfem_multi(
            tsk.basis, rho_projected, u_dofs,
            cfg.E0, cfg.E_min, p, tsk.nu,
            elem_func=density_interpolation
        )
        return strain_energy / len(force_list)


    def get_metrics(
        self,
        rho_list,
        p,
        force_list,
        density_interpolation,
        iter,
        n_joblib,
        record = False
    ) -> float:
        
        compliance_list = list()
        penalty_list = list()
        volume_violation_list = list()
        rho_mean_list = list()
        penalty_weight = self.cfg.penalty_weight  # could be adaptive
        
        compliance_list = self.get_compliance_list(
            rho_list,
            p,
            force_list,
            density_interpolation,
            n_joblib
        )
        for rho, compliance in zip(rho_list, compliance_list):
            rho_mean_list.append(np.mean(rho))
            # compliance = self.get_compliance(
            #     rho,
            #     p,
            #     force_list,
            #     u_dofs,
            #     density_interpolation
            # )
            
            logger.info(f"np.mean(rho): {np.mean(rho)}")
            logger.info(f"compliance: {compliance}")
            # compliance_list.append(compliance)

            # Volume constraint penalty
            # elements_volume_design = self.tsk.elements_volume[self.tsk.design_elements]
            # vol_ratio = np.sum(rho[self.tsk.design_elements] * elements_volume_design) / np.sum(elements_volume_design)
            
            elements_volume_design = self.tsk.elements_volume[self.tsk.design_elements]
            rho_design = rho[self.tsk.design_elements]
            vol_ratio = np.sum(rho_design * elements_volume_design) / np.sum(elements_volume_design)
            vol_frac = self.schedulers.value_on_a_scheduler("vol_frac", iter)

            
            volume_violation = vol_ratio - vol_frac
            volume_violation_list.append(volume_violation)
            penalty = penalty_weight * max(0, volume_violation)**2
            penalty_list.append(penalty)

        compliance_list = np.array(compliance_list)
        penalty_list = np.array(penalty_list)
        volume_violation_list = np.array(volume_violation_list)
        rho_mean_list = np.array(rho_mean_list)
        
        if record is True:
            self.recorder.feed_data("rho_projected", rho_mean_list)
            self.recorder.feed_data("compliance", compliance_list)
            self.recorder.feed_data("penalty", penalty_list)
            self.recorder.feed_data("volume_violation", volume_violation_list)
            
        return compliance_list + penalty_list


    def generate_offspring(self, elite, offspring_raw, mutation_strength):
        cfg = self.cfg
        for i in range(cfg.offspring_size):
            parent_idx = np.random.randint(0, elite.shape[0])
            mutate_from_parent(
                elite[parent_idx], offspring_raw[i], mutation_strength, cfg
            )
            delta = np.linalg.norm(offspring_raw[i] - elite[parent_idx])
            logger.info(f"Mutation delta for offspring[{i}]: {delta:.4e}")
    
    
    def generate_offspring_with_crossover(self, elite, offspring_raw, mutation_strength):
        cfg = self.cfg
        rng = np.random.default_rng()

        for i in range(cfg.offspring_size):
            # 2 親選択（ランダム）
            parent1_idx, parent2_idx = rng.integers(0, elite.shape[0], size=2)
            parent1 = elite[parent1_idx]
            parent2 = elite[parent2_idx]

            # α混合交叉
            alpha = rng.uniform(0, 1)
            np.add(alpha * parent1, (1 - alpha) * parent2, out=offspring_raw[i])

            # 変異（in-place）
            offspring_raw[i] += mutation_strength * rng.standard_normal(parent1.shape)
            np.clip(offspring_raw[i], cfg.rho_min, cfg.rho_max, out=offspring_raw[i])

            # ログ（オプション）
            delta = np.linalg.norm(offspring_raw[i] - parent1)
            logger.info(f"[offspring {i}] crossover α={alpha:.2f}, delta from parent1={delta:.4e}")

    def projector(
        self,
        offspring_raw,
        offspring_projected,
        beta
    ):
        for i in range(offspring_raw.shape[0]):
            rho = offspring_raw[i].copy()
            rho = self.helmholz_solver.filter(rho)
            projection.heaviside_projection_inplace(
                rho, beta=beta, eta=self.cfg.beta_eta, out=rho
            )
            np.clip(rho, self.cfg.rho_min, self.cfg.rho_max, out=rho)

            logger.info(
                f"[{i}] After filter-scale-projection: "
                f"mean={rho.mean():.3f}, max={rho.max():.3f}"
            )

            offspring_projected[i] = rho


    
    def evaluate_offspring(
        self, rho_list, p, force_list,
        density_interpolation, iter, n_joblib
    ):
        return self.get_metrics(
            rho_list, p, force_list, density_interpolation, iter,
            n_joblib,
            True
        )

    def select_elite(self, population_raw, fitness, elite_size):
        elite_indices = np.argsort(fitness)[:elite_size]
        return population_raw[elite_indices]

    # def select_next_generation(
    #     self, population_raw, fitness, offspring_raw, offspring_fitness, pop_size
    # ):
    #     total_fitness = np.concatenate([fitness, offspring_fitness])
    #     total_population = np.vstack([population_raw, offspring_raw])
    #     best_indices = np.argsort(total_fitness)[:pop_size]
    #     return total_population[best_indices], total_fitness[best_indices]
    def select_next_generation(
        self,
        population_raw, population_projected, fitness,
        offspring_raw, offspring_projected, offspring_fitness,
        pop_size
    ):

        """
        Select next generation from current and offspring population.
        
        Parameters
        ----------
        population_raw : ndarray
            Current generation's raw design variables.
        population_projected : ndarray
            Current generation's projected densities (used for evaluation).
        fitness : ndarray
            Current generation's fitness (e.g., compliance).
        offspring_raw : ndarray
            Offspring raw design variables.
        offspring_projected : ndarray
            Offspring projected densities.
        offspring_fitness : ndarray
            Offspring fitness.
        pop_size : int
            Number of individuals to keep.

        Returns
        -------
        next_population_raw : ndarray
            Next generation's raw design variables.
        next_population_projected : ndarray
            Next generation's projected densities.
        next_fitness : ndarray
            Next generation's fitness.
        """
        # 1. Combine
        total_fitness = np.concatenate([fitness, offspring_fitness])
        total_raw = np.vstack([population_raw, offspring_raw])
        total_projected = np.vstack([population_projected, offspring_projected])

        # 2. Select best individuals by fitness (lower is better)
        best_indices = np.argsort(total_fitness)[:pop_size]

        # 3. Return next generation
        return (
            total_raw[best_indices],
            total_projected[best_indices],
            total_fitness[best_indices]
        )



    def visualizer(self, iter, population, fitness):
        
        if iter % (cfg.max_iters // cfg.record_times) == 0 or iter == 1:
            self.recorder.print()
            self.recorder.export_progress()
            visualization.export_mesh_with_info(
                tsk.mesh,
                cell_data_names=["rho"],
                cell_data_values=[population[0]],
                filepath=cfg.vtu_path(iter)
            )

            visualization.write_mesh_with_info_as_image(
                mesh_path=cfg.vtu_path(iter),
                mesh_scalar_name="rho",
                clim=(0.0, 1.0),
                image_path=cfg.image_path(iter, "rho"),
                image_title=f"Iteration : {iter}"
            )

    def optimize(self):
        self.init_schedulers()
        tsk = self.tsk
        cfg = self.cfg
        tsk.export_analysis_condition_on_mesh(cfg.dst_path)
        density_interpolation = composer.simp_interpolation
        (
            iter_begin,
            iter_end,
            population_raw,
            n_variables,
            force_list,
            u_dofs
        ) = self.initialize_params()

        # 初期評価
        population_projected = np.empty_like(population_raw)
        beta = self.schedulers.value_on_a_scheduler("beta", 1)
        self.projector(
            population_raw, population_projected, beta
        )
        fitness = self.evaluate_offspring(
            population_projected,
            p=self.schedulers.value_on_a_scheduler("p", iter_begin),
            force_list=force_list,
            density_interpolation=density_interpolation,
            iter=iter_begin,
            n_joblib=cfg.n_joblib
        )
        n_variables = population_raw.shape[1]
        offspring_raw = np.empty((cfg.offspring_size, n_variables), dtype=np.float64)
        offspring_projected = np.empty_like(offspring_raw)
        
        for iter in range(iter_begin, iter_end):
            logger.info(f"Iteration {iter}/{iter_end-1}")

            # パラメータ更新
            (
                p,
                vol_frac,
                filter_radius,
                beta,
                mutation_strength
            ) = self.schedulers.values_as_list(
                iter,
                [
                    'p', 'vol_frac', 'filter_radius', 'beta', 'mutation_strength'
                ],
                export_log=True,
                precision=6
            )

            if filter_radius != self.helmholz_solver.radius:
                self.helmholz_solver.update_radius(
                    tsk.mesh, filter_radius, solver_option="cg_pyamg"
                )

            elite = self.select_elite(population_raw, fitness, cfg.elite_size)

            # 子個体生成（設計変数空間）
            self.generate_offspring_with_crossover(elite, offspring_raw, mutation_strength)
            
            self.projector(
                offspring_raw, offspring_projected, beta
            )

            # offspring_projected に対して）
            offspring_fitness = self.evaluate_offspring(
                offspring_projected, p=p,
                force_list=force_list,
                density_interpolation=density_interpolation,
                iter=iter,
                n_joblib=cfg.n_joblib
            )

            population_raw, population_projected, fitness = self.select_next_generation(
                population_raw, population_projected, fitness,
                offspring_raw, offspring_projected, offspring_fitness,
                cfg.population_size
            )

            self.visualizer(iter, population_projected, fitness)
            logger.info(f"Best compliance this gen: {fitness[0]:.6e}")
            logger.info(f"Compliance std this gen: {np.std(fitness):.3e}")

        return population_raw[0], fitness[0]


if __name__ == '__main__':
    import argparse
    from sktopt.mesh import toy_problem

    parser = argparse.ArgumentParser(
        description=''
    )
    parser = misc.add_common_arguments(parser)
    parser.add_argument(
        '--population_size', '-PS', type=int, default=10, help=''
    )
    parser.add_argument(
        '--offspring_size', '-OS', type=int, default=60, help=''
    )
    # parser.add_argument(
    #     '--n_generations', '-NG', type=int, default=100, help=''
    # )
    parser.add_argument(
        '--mutation_strength', '-MS', type=float, default=0.1, help=''
    )
    parser.add_argument(
        '--mutation_strength_init', '-MSI', type=float, default=0.2, help=''
    )
    parser.add_argument(
        '--mutation_strength_step', '-MSS', type=int, default=3, help=''
    )
    parser.add_argument(
        '--elite_size', '-ES', type=int, default=5, help=''
    )
    parser.add_argument(
        '--penalty_weight', '-PW', type=float, default=1e5, help=''
    )
    parser.add_argument(
        '--n_joblib', '-nJ', type=int, default=3, help=''
    )
    
    args = parser.parse_args()
    if args.task_name == "toy1":
        tsk = toy_problem.toy1()
    elif args.task_name == "toy1_fine":
        tsk = toy_problem.toy1_fine()
    elif args.task_name == "toy2":
        tsk = toy_problem.toy2()
    else:
        tsk = toy_problem.toy_msh(args.task_name, args.mesh_path)

    print("load toy problem")
    print("generate LogMOC_Config")
    cfg = Evolutionary_Config.from_defaults(
        **vars(args)
    )
    print(f"cfg: {cfg}")
    print("optimizer")
    optimizer = Evolutionary_Optimizer(cfg, tsk)
    print("parameterize")
    optimizer.parameterize()
    print("optimize")
    optimizer.optimize()
