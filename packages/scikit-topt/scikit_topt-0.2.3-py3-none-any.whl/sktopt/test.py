
import numpy as np
from skfem import MeshTet, ElementTetP1, ElementVector, Basis

# 立方体領域を四面体でメッシュ分割（4等分の格子を細分して四面体化）
mesh = MeshTet.init_tensor(*( [np.linspace(0, 1, 5)] * 3 ))  # 5点 ⇒ 4要素分割
mesh = mesh.with_defaults()   # 境界にデフォルトの名前付け（left/rightなど）
# 有限要素の定義：一次四面体のベクトル要素（3次元ベクトル場）
element = ElementVector(ElementTetP1())  # 3Dで自動的に3成分のベクトル要素となる
basis = Basis(mesh, element, intorder=2)  # 積分次数 intorder は2で十分（線形要素なので）

from skfem.helpers import ddot, sym_grad, trace, eye
from skfem.models.elasticity import lame_parameters

# 材料定数の設定（例：ヤング率 E=1000, ポアソン比 nu=0.3）
E, nu = 1e3, 0.3
lam, mu = lame_parameters(E, nu)
# 構成則テンソル C の定義
def C(strain):
    return 2.0 * mu * strain + lam * eye(trace(strain), strain.shape[0])

from skfem import BilinearForm, asm

@BilinearForm
def stiffness(u, v, w):
    # 式: σ(u):ε(v) = [C(sym_grad(u))] : [sym_grad(v)]
    return ddot(C(sym_grad(u)), sym_grad(v))
# 剛性行列の組み立て
K = asm(stiffness, basis)
# 荷重ベクトル（本例ではゼロベクトルに相当）
f = np.zeros(basis.N)  # 自由度数と同じ長さのゼロ配列

