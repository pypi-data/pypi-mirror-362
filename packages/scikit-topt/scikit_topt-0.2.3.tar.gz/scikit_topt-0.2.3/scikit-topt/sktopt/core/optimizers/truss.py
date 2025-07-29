from typing import Literal
from dataclasses import dataclass
import numpy as np
import skfem
import sktopt
from sktopt.core import misc
from sktopt.core.optimizers import common
from sktopt.tools.logconf import mylogger
logger = mylogger(__name__)


@dataclass
class TrussProjection_Config(common.DensityMethodLagrangianConfig):
    interpolation: Literal["SIMP"] = "SIMP"
    mu_p: float = 300.0
    lambda_v: float = 10.0
    lambda_decay: float = 0.90



def compute_element_centers(mesh: skfem.MeshTet | skfem.MeshHex) -> np.ndarray:
    """各要素の重心を返す (n_elements, 3)"""
    t = mesh.t
    p = mesh.p.T
    return np.mean(p[t], axis=1)


def point_to_segment_distance_3d(p, a, b):
    """点pと線分abの最短距離を返す"""
    ab = b - a
    t = np.dot(p - a, ab) / np.dot(ab, ab)
    t = np.clip(t, 0.0, 1.0)
    closest = a + t * ab
    return np.linalg.norm(p - closest)


def project_trusses_to_elements(
    tsk: sktopt.mesh.TaskConfig,
    node_positions: np.ndarray,     # (n_nodes, 3)
    members: np.ndarray,            # (n_members, 2)
    x_e: np.ndarray,                # (n_members,)
    A_e: np.ndarray,                # (n_members,)
    sigma: float = 0.1
) -> np.ndarray:
    """
    トラス情報からscikit-femメッシュの要素密度を構築
    """
    centers = compute_element_centers(tsk.mesh[tsk.design_elements])  # (n_elements, 3)
    rho = np.zeros(len(tsk.design_elements))

    for k, (i, j) in enumerate(members):
        p1, p2 = node_positions[i], node_positions[j]
        weight = x_e[k] * A_e[k]
        for e, c in enumerate(centers):
            d = point_to_segment_distance_3d(c, p1, p2)
            phi = np.exp(-(d / sigma)**2)
            rho[e] += weight * phi

    return rho


class TrussProjection_Optimizer(common.DensityMethod):
    def __init__(
        self,
        cfg: TrussProjection_Config,
        tsk: sktopt.mesh.TaskConfig,
    ):
        assert cfg.lambda_lower < cfg.lambda_upper
        super().__init__(cfg, tsk)
        
        self.recorder = self.add_recorder(tsk)
        ylog_dC = True if cfg.percentile > 0.0 else False
        ylog_lambda_v = True if cfg.lambda_lower > 0.0 else False
        self.recorder.add("-dC", plot_type="min-max-mean-std", ylog=ylog_dC)
        self.recorder.add(
            "lambda_v", ylog=ylog_lambda_v
        )
        self.lambda_v = cfg.lambda_v
        