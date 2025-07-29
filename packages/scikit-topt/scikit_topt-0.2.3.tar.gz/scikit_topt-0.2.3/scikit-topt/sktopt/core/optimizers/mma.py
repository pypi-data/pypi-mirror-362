import os
from typing import Literal
import inspect
import shutil
import json
from dataclasses import dataclass, asdict
import numpy as np
import scipy.sparse.linalg as spla
import numpy as np
import nlopt
import sktopt
from sktopt import tools
from sktopt.core import derivatives, projection
from sktopt.core import visualization
from sktopt.fea import solver
from sktopt import filter
from sktopt.fea import composer
from sktopt.core import misc


@dataclass
class MMA_Config():
    dst_path: str = "./result"
    interpolation: Literal["SIMP", "RAMP"] = "RAMP"
    record_times: int=20
    max_iters: int=200
    p_init: float = 1.0
    p: float = 3.0
    p_rate: float = 20.0
    vol_frac_init: float = 0.8
    vol_frac: float = 0.4
    vol_frac_rate: float = 20.0
    beta_init: float = 1.0
    beta: float = 16
    beta_rate: float = 20.
    beta_eta: float = 0.5
    filter_radius: float = 0.5
    rho_min: float = 1e-3
    rho_max: float = 1.0
    move_limit_init: float = 0.8
    move_limit: float = 0.2
    move_limit_rate: float = 20.0
    restart: bool = False
    restart_from: int = -1
    export_img: bool = False
    
    @classmethod
    def from_defaults(cls, **args):
        sig = inspect.signature(cls)
        valid_keys = sig.parameters.keys()
        filtered_args = {k: v for k, v in args.items() if k in valid_keys}
        return cls(**filtered_args)

    
    def export(self, path: str):
        with open(f"{path}/cfg.json", "w") as f:
            json.dump(asdict(self), f, indent=2)

    def vtu_path(self, iter: int):
        return f"{self.dst_path}/mesh_rho/info_mesh-{iter:08d}.vtu",


    def image_path(self, iter: int):
        if self.export_img:
            return f"{self.dst_path}/mesh_rho/info_mesh-{iter:08d}.jpg"
        else:
            return None


def mma_objective_factory(
    tsk,
    p, vol_frac, beta, move_limit,
    helmholz_solver, force_list, density_interpolation, dC_drho_func,
    compliance_avg, strain_energy_ave,
    rho,
    rho_filtered, rho_projected, dC_drho_full, dC_drho_ave, dC_drho_projected, dH, grad_filtered,
    recorder
):
    def mma_objective(x, grad):
        nonlocal dC_drho_full, dC_drho_ave, dC_drho_projected, rho, rho_filtered, rho_projected, dH, grad_filtered
        nonlocal compliance_avg, strain_energy_ave
        print(f"p {p:.4f}, vol_frac {vol_frac:.4f}, beta {beta:.4f}, move_limit {move_limit:.4f}")

        rho[tsk.design_elements] = x
        rho_filtered[:] = helmholz_solver.filter(rho)
        projection.heaviside_projection_inplace(
            rho_filtered, beta=beta, eta=cfg.beta_eta, out=rho_projected
        )

        dC_drho_full[:] = 0.0
        dC_drho_ave[:] = 0.0
        strain_energy_ave = 0.0
        compliance_avg = 0.0
        for force in force_list:
            compliance, u = solver.compute_compliance_basis_numba(
                tsk.basis, tsk.free_nodes, tsk.dirichlet_nodes, force,
                tsk.E0, tsk.Emin, p, tsk.nu0,
                rho_projected,
                density_interpolation
            )
            compliance_avg += compliance
            strain_energy = composer.compute_strain_energy_numba(
                u,
                tsk.basis.element_dofs,
                tsk.mesh.p,
                rho_projected,
                tsk.E0,
                tsk.Emin,
                p,
                tsk.nu0,
            )
            strain_energy_ave += strain_energy
            dC_drho_projected[:] = dC_drho_func(
                rho_projected,
                strain_energy, tsk.E0, tsk.Emin, p
            )
            projection.heaviside_projection_derivative_inplace(
                rho_filtered,
                beta=beta, eta=cfg.beta_eta, out=dH
            )
            np.multiply(dC_drho_projected, dH, out=grad_filtered)
            dC_drho_full += helmholz_solver.gradient(grad_filtered)
                
        dC_drho_full /= len(force_list)
        strain_energy_ave /= len(force_list)
        compliance_avg /= len(force_list)

        recorder.feed_data("dC", dC_drho_full)
        recorder.feed_data("strain_energy", strain_energy_ave)
        recorder.feed_data("rho", rho[tsk.design_elements])
        recorder.feed_data("rho_projected", rho_projected[tsk.design_elements])
        recorder.feed_data("compliance", compliance_avg)
        if grad.size > 0:
            grad[:] = dC_drho_full[tsk.design_elements]
        return compliance_avg
    return mma_objective


def mma_constraint_factory(
    tsk,
    helmholz_solver,
    rho, rho_filtered, rho_projected,
    beta, beta_eta, elements_volume, vol_frac, recorder
):
    elements_volume_sum = np.sum(elements_volume)
    def mma_constraint(x, grad):
        nonlocal rho, rho_filtered, rho_projected
        rho[tsk.design_elements] = x
        rho_filtered[:] = helmholz_solver.filter(rho)
        projection.heaviside_projection_inplace(
            rho_filtered, beta=beta, eta=beta_eta, out=rho_projected
        )
        vol_error = np.sum(
            rho_projected[tsk.design_elements] * elements_volume
        ) / elements_volume_sum - vol_frac
        recorder.feed_data("vol_error", vol_error)
        if grad.size > 0:
            grad[:] = elements_volume
        return vol_error
    return mma_constraint


class MMA_Optimizer():
    def __init__(
        self,
        cfg: MMA_Config,
        tsk: sktopt.mesh.TaskConfig,
    ):
        self.cfg = cfg
        self.tsk = tsk
        if not os.path.exists(self.cfg.dst_path):
            os.makedirs(self.cfg.dst_path)
        # self.tsk.export(self.cfg.dst_path)
        self.cfg.export(self.cfg.dst_path)
        self.tsk.nodes_and_elements_stats(self.cfg.dst_path)
        
        if os.path.exists(f"{self.cfg.dst_path}/mesh_rho"):
            shutil.rmtree(f"{self.cfg.dst_path}/mesh_rho")
        os.makedirs(f"{self.cfg.dst_path}/mesh_rho")
        if os.path.exists(f"{self.cfg.dst_path}/rho-histo"):
            shutil.rmtree(f"{self.cfg.dst_path}/rho-histo")
        os.makedirs(f"{self.cfg.dst_path}/rho-histo")
        if not os.path.exists(f"{self.cfg.dst_path}/data"):
            os.makedirs(f"{self.cfg.dst_path}/data")

        self.recorder = tools.HistoriesLogger(self.cfg.dst_path)
        self.recorder.add("rho")
        self.recorder.add("rho_projected")
        self.recorder.add("compliance")
        self.recorder.add("dC")
        self.recorder.add("strain_energy")
        self.recorder.add("vol_error")
        self.schedulers = tools.Schedulers(self.cfg.dst_path)
    
    
    def init_schedulers(self):

        cfg = self.cfg
        p_init = cfg.p_init
        vol_frac_init = cfg.vol_frac_init
        move_limit_init = cfg.move_limit_init
        beta_init = cfg.beta_init
        self.schedulers.add(
            "p",
            p_init,
            cfg.p,
            cfg.p_rate,
            cfg.max_iters
        )
        self.schedulers.add(
            "vol_frac",
            vol_frac_init,
            cfg.vol_frac,
            cfg.vol_frac_rate,
            cfg.max_iters
        )
        # print(move_init)
        # print(cfg.move_limit, cfg.move_limit_rate)
        self.schedulers.add(
            "move_limit",
            move_limit_init,
            cfg.move_limit,
            cfg.move_limit_rate,
            cfg.max_iters
        )
        self.schedulers.add(
            "beta",
            beta_init,
            cfg.beta,
            cfg.beta_rate,
            cfg.max_iters
        )
        self.schedulers.export()
    
    def parameterize(self, preprocess=True):
        self.helmholz_solver = filter.HelmholtzFilter.from_defaults(
            self.tsk.mesh, self.cfg.filter_radius, f"{self.cfg.dst_path}/data"
        )
        if preprocess:
            print("preprocessing....")
            # self.helmholz_solver.create_solver()
            self.helmholz_solver.create_LinearOperator()
            print("...end")
        else:
            self.helmholz_solver.create_solver()

    def load_parameters(self):
        self.helmholz_solver = filter.HelmholtzFilter.from_file(
            f"{self.cfg.dst_path}/data"
        )
    

    def optimize(self):
        tsk = self.tsk
        cfg = self.cfg
        elements_volume = tsk.elements_volume[tsk.design_elements]
        rho = np.ones(tsk.all_elements.shape)
        rho = rho * cfg.vol_frac if cfg.vol_frac_rate < 0 else rho * cfg.vol_frac_init
        rho += 0.1
        if cfg.restart:
            if cfg.restart_from > 0:
                data = np.load(
                    f"{cfg.dst_path}/data/{str(cfg.restart_from).zfill(6)}-rho.npz"
                )
            else:
                iter, data_path = misc.find_latest_iter_file(f"{cfg.dst_path}/data")
                data = np.load(data_path)
                iter_begin = iter

            rho[tsk.design_elements] = data["rho_design_elements"]
            del data
        else:
            pass
        print("np.average(rho[tsk.design_elements]):", np.average(rho[tsk.design_elements]))
        # rho[tsk.dirichlet_force_elements] = 1.0
        rho[tsk.fixed_elements_in_rho] = 1.0
        self.init_schedulers()

        
        rho_prev = np.zeros_like(rho)
        if cfg.interpolation == "SIMP":
        # if False:
            density_interpolation = composer.simp_interpolation_numba
            dC_drho_func = derivatives.dC_drho_simp
        elif cfg.interpolation == "RAMP":
            density_interpolation = composer.ramp_interpolation_numba
            dC_drho_func = derivatives.dC_drho_ramp
        else:
            raise ValueError("should be SIMP or RAMP")

        dC_drho_full = np.zeros_like(rho)
        dC_drho_ave = np.zeros_like(rho[tsk.design_elements])
        rho_filtered = np.zeros_like(rho)
        rho_projected = np.zeros_like(rho)
        dH = np.empty_like(rho)
        grad_filtered = np.empty_like(rho)
        dC_drho_projected = np.empty_like(rho)
        force_list = tsk.force if isinstance(tsk.force, list) else [tsk.force]
        for iter in range(cfg.max_iters):
            print(f"iteration: {iter+1}/{cfg.max_iters}")
            p, vol_frac, beta, move_limit = (
                self.schedulers.values(iter)[k] for k in ['p', 'vol_frac', 'beta', 'move_limit']
            )
            compliance_avg = 0
            strain_energy_ave = 0

            # --- NLopt MMA ---
            opt = nlopt.opt(nlopt.LD_MMA, len(tsk.design_elements))
            opt.set_lower_bounds(0.0)
            opt.set_upper_bounds(1.0)

            _objective = mma_objective_factory(
                tsk,
                p, vol_frac, beta, move_limit,
                self.helmholz_solver, force_list, density_interpolation, dC_drho_func,
                compliance_avg, strain_energy_ave,
                rho,
                rho_filtered, rho_projected, dC_drho_full, dC_drho_ave, dC_drho_projected, dH, grad_filtered,
                self.recorder
            )
            
            _constraint = mma_constraint_factory(
                tsk,
                self.helmholz_solver,
                rho, rho_filtered, rho_projected,
                beta, cfg.beta_eta, elements_volume, vol_frac, self.recorder
            )

            opt.set_min_objective(_objective)
            opt.add_inequality_constraint(_constraint, 1e-6)

            opt.set_maxeval(30)
            x_new = opt.optimize(rho[tsk.design_elements].copy())
            rho_prev[:] = rho[:]
            rho[tsk.design_elements] = x_new
            
            if iter % (cfg.max_iters // self.cfg.record_times) == 0 or iter == 1:
            # if True:
                print(f"Saving at iteration {iter}")
                self.recorder.print()
                # self.recorder_params.print()
                self.recorder.export_progress()
                
                visualization.save_info_on_mesh(
                    tsk,
                    rho_projected, rho_prev,
                    cfg.vtu_path(iter),
                    cfg.image_path(iter),
                    f"Iteration : {iter}"
                )
                visualization.export_submesh(
                    tsk, rho_projected, 0.5, f"{cfg.dst_path}/cubic_top.vtk"
                )
                np.savez_compressed(
                    f"{cfg.dst_path}/data/{str(iter).zfill(6)}-rho.npz",
                    rho_design_elements=rho[tsk.design_elements],
                    # compliance=compliance
                )

        visualization.rho_histo_plot(
            rho_projected[tsk.design_elements],
            f"{self.cfg.dst_path}/rho-histo/last.jpg"
        )

        visualization.export_submesh(
            tsk, rho_projected, 0.5, f"{cfg.dst_path}/cubic_top.vtk"
        )
    
    
if __name__ == '__main__':
    import argparse
    from sktopt.mesh import toy_problem

    parser = argparse.ArgumentParser(
        description=''
    )

    parser.add_argument(
        '--interpolation', '-I', type=str, default="RAMP", help=''
    )
    parser.add_argument(
        '--max_iters', '-NI', type=int, default=200, help=''
    )
    parser.add_argument(
        '--filter_radius', '-DR', type=float, default=0.05, help=''
    )
    parser.add_argument(
        '--move_limit_init', '-MLI', type=float, default=0.8, help=''
    )
    parser.add_argument(
        '--move_limit', '-ML', type=float, default=0.2, help=''
    )
    parser.add_argument(
        '--move_limit_rate', '-MLR', type=float, default=5, help=''
    )
    parser.add_argument(
        '--eta', '-ET', type=float, default=0.02, help=''
    )
    parser.add_argument(
        '--record_times', '-RT', type=int, default=20, help=''
    )
    parser.add_argument(
        '--dst_path', '-DP', type=str, default="./result/test0", help=''
    )
    parser.add_argument(
        '--vol_frac_init', '-VI', type=float, default=0.8, help=''
    )
    parser.add_argument(
        '--vol_frac', '-V', type=float, default=0.4, help=''
    )
    parser.add_argument(
        '--vol_frac_rate', '-VFT', type=float, default=20.0, help=''
    )
    parser.add_argument(
        '--p_init', '-PI', type=float, default=1.0, help=''
    )
    parser.add_argument(
        '--p', '-P', type=float, default=3.0, help=''
    )
    parser.add_argument(
        '--p_rate', '-PT', type=float, default=20.0, help=''
    )
    parser.add_argument(
        '--beta_init', '-BI', type=float, default=0.1, help=''
    )
    parser.add_argument(
        '--beta', '-B', type=float, default=5.0, help=''
    )
    parser.add_argument(
        '--beta_rate', '-BR', type=float, default=20.0, help=''
    )
    parser.add_argument(
        '--beta_eta', '-BE', type=float, default=0.5, help=''
    )
    parser.add_argument(
        '--mu_p', '-MUP', type=float, default=100.0, help=''
    )
    parser.add_argument(
        '--mu_d', '-MUD', type=float, default=200.0, help=''
    )
    parser.add_argument(
        '--mu_i', '-MUI', type=float, default=10.0, help=''
    )
    parser.add_argument(
        '--lambda_v', '-LV', type=float, default=1.0, help=''
    )
    parser.add_argument(
        '--lambda_decay', '-LD', type=float, default=0.5, help=''
    )
    parser.add_argument(
        '--restart', '-RS', type=misc.str2bool, default=False, help=''
    )
    parser.add_argument(
        '--restart_from', '-RF', type=int, default=-1, help=''
    )
    parser.add_argument(
        '--task', '-T', type=str, default="toy1", help=''
    )
    parser.add_argument(
        '--export_img', '-EI', type=misc.str2bool, default=False, help=''
    )
    args = parser.parse_args()
    

    if args.task == "toy1":
        tsk = toy_problem.toy1()
    elif args.task == "toy1_fine":
        tsk = toy_problem.toy1_fine()
    elif args.task == "toy2":
        tsk = toy_problem.toy2()
    else:
        tsk = toy_problem.toy_msh(args.task)
    # else:
    #     raise ValueError("task is not indicated")
    
    print("load toy problem")
    
    print("generate OC_RAMP_Config")
    cfg = MMA_Config.from_defaults(
        **vars(args)
    )

    print("optimizer")
    optimizer = MMA_Optimizer(cfg, tsk)
    print("parameterize")
    optimizer.parameterize(preprocess=True)
    # optimizer.parameterize(preprocess=False)
    # optimizer.load_parameters()
    print("optimize")
    optimizer.optimize()
    # optimizer.optimize_org()