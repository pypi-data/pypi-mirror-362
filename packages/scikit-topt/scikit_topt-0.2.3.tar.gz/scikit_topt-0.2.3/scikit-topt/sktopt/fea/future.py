
@njit(parallel=True)
def _assemble_stiffness_matrix_hex8_gauss(
    p_coords, t_conn, element_dofs, E0, Emin, nu, E_elem
):
    n_elements = t_conn.shape[1]
    ndofs = 24  # 8 nodes * 3 dofs

    data = np.zeros(n_elements * ndofs * ndofs)
    row = np.zeros_like(data, dtype=np.int32)
    col = np.zeros_like(data, dtype=np.int32)
    lam = (nu * E0) / ((1.0 + nu) * (1.0 - 2.0 * nu))
    mu = E0 / (2.0 * (1.0 + nu))

    C0 = np.array([
        [lam + 2 * mu, lam, lam, 0, 0, 0],
        [lam, lam + 2 * mu, lam, 0, 0, 0],
        [lam, lam, lam + 2 * mu, 0, 0, 0],
        [0, 0, 0, mu, 0, 0],
        [0, 0, 0, 0, mu, 0],
        [0, 0, 0, 0, 0, mu],
    ])

    # Gauss points and weights for 2x2x2 integration
    gp = np.array([-np.sqrt(1/3), np.sqrt(1/3)])
    weights = np.array([1.0, 1.0])

    for e in prange(n_elements):
        nodes = t_conn[:, e]
        coords = p_coords[:, nodes]  # (3, 8)
        E_eff = E_elem[e]
        C = C0 * (E_eff / E0)
        ke = np.zeros((24, 24))

        for i in range(2):
            for j in range(2):
                for k in range(2):
                    xi, eta, zeta = gp[i], gp[j], gp[k]
                    w = weights[i] * weights[j] * weights[k]

                    # Shape function derivatives wrt natural coordinates
                    dN_nat = np.array([
                        [-(1 - eta) * (1 - zeta),
                         -(1 - xi) * (1 - zeta),
                         -(1 - xi) * (1 - eta)],
                        [(1 - eta) * (1 - zeta),
                         -(1 + xi) * (1 - zeta),
                         -(1 + xi) * (1 - eta)],
                        [(1 + eta) * (1 - zeta),
                         (1 + xi) * (1 - zeta),
                         -(1 + xi) * (1 + eta)],
                        [-(1 + eta) * (1 - zeta),
                         (1 - xi) * (1 - zeta),
                         -(1 - xi) * (1 + eta)],
                        [-(1 - eta) * (1 + zeta),
                         -(1 - xi) * (1 + zeta),
                         (1 - xi) * (1 - eta)],
                        [(1 - eta) * (1 + zeta),
                         -(1 + xi) * (1 + zeta),
                         (1 + xi) * (1 - eta)],
                        [(1 + eta) * (1 + zeta),
                         (1 + xi) * (1 + zeta),
                         (1 + xi) * (1 + eta)],
                        [-(1 + eta) * (1 + zeta),
                         (1 - xi) * (1 + zeta),
                         (1 - xi) * (1 + eta)],
                    ]) / 8.0  # shape (8, 3)
                    J = np.zeros((3, 3))
                    for a in range(8):
                        for i_dim in range(3):
                            for j_dim in range(3):
                                J[i_dim, j_dim] += dN_nat[a, j_dim] * \
                                    coords[i_dim, a]

                    detJ = np.linalg.det(J)
                    invJ = np.linalg.inv(J)
                    dN_global = dN_nat @ invJ.T  # (8, 3)

                    B = np.zeros((6, 24))
                    for a in range(8):
                        dNdx, dNdy, dNdz = dN_global[a]
                        B[0, 3*a + 0] = dNdx
                        B[1, 3*a + 1] = dNdy
                        B[2, 3*a + 2] = dNdz
                        B[3, 3*a + 0] = dNdy
                        B[3, 3*a + 1] = dNdx
                        B[4, 3*a + 1] = dNdz
                        B[4, 3*a + 2] = dNdy
                        B[5, 3*a + 2] = dNdx
                        B[5, 3*a + 0] = dNdz

                    ke += B.T @ C @ B * detJ * w

        dofs = element_dofs[:, e]
        for i in range(24):
            for j in range(24):
                idx = e * 24 * 24 + i * 24 + j
                data[idx] = ke[i, j]
                row[idx] = dofs[i]
                col[idx] = dofs[j]

    return data, (row, col)


def strain_energy_hdcode(
    u,
    element_dofs,
    node_coords,
    rho,
    E0,
    Emin, penal, nu0
):
    """
    Compute element-wise strain energy
    for a 3D tetrahedral mesh using SIMP material interpolation.
    """
    # mesh = basis.mesh
    # Material constants for elasticity matrix
    # lam_factor = lambda E: E / ((1.0 + nu0) * (1.0 - 2.0 * nu0))
    # mu_factor = lambda E: E / (2.0 * (1.0 + nu0))
    def lam_factor(E):
        return E / ((1.0 + nu0) * (1.0 - 2.0 * nu0))

    # number of elements (columns of element_dofs)
    n_elems = element_dofs.shape[1]
    energies = np.zeros(n_elems)
    # Precompute base elasticity matrix for E0
    # (could also compute fresh each time scaled by E_e)
    C0 = lam_factor(E0) * np.array([
        [1 - nu0, nu0, nu0, 0, 0, 0],
        [nu0, 1 - nu0, nu0, 0, 0, 0],
        [nu0, nu0, 1 - nu0, 0, 0, 0],
        [0, 0, 0, (1 - 2*nu0) / 2.0, 0, 0],
        [0, 0, 0, 0, (1 - 2*nu0) / 2.0, 0],
        [0, 0, 0, 0, 0, (1 - 2*nu0) / 2.0]
    ])
    # Loop over each element in the design domain
    for idx in range(n_elems):
        # Global DOF indices for this element and extract their coordinates
        # 12 DOF indices (3 per node for 4 nodes)
        edofs = element_dofs[:, idx]
        # Infer the 4 node indices (each node has 3 DOFs).
        # We assume DOFs are grouped by node.
        node_ids = [int(edofs[3*j] // 3) for j in range(4)]
        # Coordinates of the 4 nodes (3x4 matrix)
        coords = node_coords[:, node_ids]
        # Build matrix M for shape function coefficient solve
        # Each row: [x_i, y_i, z_i, 1] for node i
        M = np.column_stack((coords.T, np.ones(4)))
        # Minv = np.linalg.inv(M)
        # Minv = np.linalg.solve(M, np.eye(3))
        Minv = np.linalg.pinv(M)
        # Gradients of shape functions
        # (each column i gives grad(N_i) = [dN_i/dx, dN_i/dy, dN_i/dz])
        grads = Minv[:3, :]  # 3x4 matrix of gradients
        # Construct B matrix (6x12) for this element
        B = np.zeros((6, 12))
        for j in range(4):
            dNdx, dNdy, dNdz = grads[0, j], grads[1, j], grads[2, j]
            # Fill B for this node j
            B[0, 3*j + 0] = dNdx
            B[1, 3*j + 1] = dNdy
            B[2, 3*j + 2] = dNdz
            B[3, 3*j + 0] = dNdy
            B[3, 3*j + 1] = dNdx
            B[4, 3*j + 1] = dNdz
            B[4, 3*j + 2] = dNdy
            B[5, 3*j + 2] = dNdx
            B[5, 3*j + 0] = dNdz
        # Compute volume of the tetrahedron (abs(det(M))/6)
        vol = abs(np.linalg.det(M)) / 6.0
        # Young's modulus for this element via SIMP
        E_eff = Emin + (rho[idx] ** penal) * (E0 - Emin)
        # Form elasticity matrix C_e
        # (scale base matrix by E_eff/E0 since ν constant)
        C_e = C0 * (E_eff / E0)
        # Element nodal displacements
        u_e = u[edofs]
        # Compute strain = B * u_e
        strain = B.dot(u_e)
        # Strain energy density = 0.5 * strain^T * C_e * strain
        Ue = 0.5 * strain.dot(C_e.dot(strain)) * vol
        energies[idx] = Ue
    return energies


@njit
def strain_energy_hdcode_numba(
    u,
    element_dofs,
    node_coords,  # mesh.p
    rho,
    E0,
    Emin,
    penal,
    nu0
):
    # lam_factor = lambda E: E / ((1.0 + nu0) * (1.0 - 2.0 * nu0))
    def lam_factor(E):
        return E / ((1.0 + nu0) * (1.0 - 2.0 * nu0))

    n_elems = element_dofs.shape[1]
    energies = np.zeros(n_elems)

    # Precompute elasticity matrix C0
    C0 = lam_factor(E0) * np.array([
        [1 - nu0, nu0, nu0, 0, 0, 0],
        [nu0, 1 - nu0, nu0, 0, 0, 0],
        [nu0, nu0, 1 - nu0, 0, 0, 0],
        [0, 0, 0, (1 - 2*nu0) / 2.0, 0, 0],
        [0, 0, 0, 0, (1 - 2*nu0) / 2.0, 0],
        [0, 0, 0, 0,  0, (1 - 2*nu0) / 2.0]
    ])

    for idx in range(n_elems):
        edofs = element_dofs[:, idx]
        node_ids = np.empty(4, dtype=np.int32)
        coords = np.empty((3, 4))

        for j in range(4):
            node_id = int(edofs[3 * j] // 3)
            node_ids[j] = node_id
            for d in range(3):
                coords[d, j] = node_coords[d, node_id]

        # Compute shape function gradients using geometric method
        v1 = coords[:, 1] - coords[:, 0]
        v2 = coords[:, 2] - coords[:, 0]
        v3 = coords[:, 3] - coords[:, 0]
        vol = np.dot(np.cross(v1, v2), v3) / 6.0
        if vol <= 0.0:
            raise ValueError(
                f"Negative or zero volume at element {idx}: {vol}"
            )

        M = np.ones((4, 4))
        for i in range(4):
            for d in range(3):
                M[i, d] = coords[d, i]
        Minv = np.linalg.inv(M)
        grads = Minv[:3, :]  # ∇ϕ

        B = np.zeros((6, 12))
        for j in range(4):
            dNdx, dNdy, dNdz = grads[0, j], grads[1, j], grads[2, j]
            B[0, 3*j + 0] = dNdx
            B[1, 3*j + 1] = dNdy
            B[2, 3*j + 2] = dNdz
            B[3, 3*j + 0] = dNdy
            B[3, 3*j + 1] = dNdx
            B[4, 3*j + 1] = dNdz
            B[4, 3*j + 2] = dNdy
            B[5, 3*j + 2] = dNdx
            B[5, 3*j + 0] = dNdz

        E_eff = Emin + (rho[idx] ** penal) * (E0 - Emin)
        C_e = C0 * (E_eff / E0)
        u_e = u[edofs]
        strain = B @ u_e
        Ue = 0.5 * strain @ (C_e @ strain) * abs(vol)
        energies[idx] = Ue

    return energies


@njit(parallel=True)
def _assemble_stiffness_matrix_numba_tet(
    p_coords, t_conn,
    element_dofs, E0, Emin, nu, E_elem
):
    n_elements = t_conn.shape[1]
    data = np.zeros(n_elements * 144)  # 12x12 per element
    row = np.zeros_like(data, dtype=np.int32)
    col = np.zeros_like(data, dtype=np.int32)

    # Base elasticity matrix (for E=1.0, scaled later by E_eff)
    lam_base, mu_base = lam_mu(E0, nu)
    C0 = np.array([
        [1 - nu, nu, nu, 0, 0, 0],
        [nu, 1 - nu, nu, 0, 0, 0],
        [nu, nu, 1 - nu, 0, 0, 0],
        [0, 0, 0, (1 - 2*nu) / 2.0, 0, 0],
        [0, 0, 0, 0, (1 - 2*nu) / 2.0, 0],
        [0, 0, 0, 0, 0, (1 - 2*nu) / 2.0]
    ])
    C0 *= lam_base

    for e in prange(n_elements):
        nodes = t_conn[:, e]
        coords = p_coords[:, nodes]  # shape (3, 4)

        n0, n1, n2, n3 = t_conn[:, e]
        v1 = p_coords[:, n1] - p_coords[:, n0]
        v2 = p_coords[:, n2] - p_coords[:, n0]
        v3 = p_coords[:, n3] - p_coords[:, n0]
        vol = np.dot(np.cross(v1, v2), v3) / 6.0

        M = np.ones((4, 4))
        for i in range(4):
            M[i, :3] = coords[:, i]
        # vol = abs(np.linalg.det(M)) / 6.0
        Minv = np.linalg.inv(M)
        grads = Minv[:3, :]  # shape (3, 4)

        B = np.zeros((6, 12))
        for j in range(4):
            dNdx, dNdy, dNdz = grads[0, j], grads[1, j], grads[2, j]
            B[0, 3*j] = dNdx
            B[1, 3*j + 1] = dNdy
            B[2, 3*j + 2] = dNdz
            B[3, 3*j] = dNdy
            B[3, 3*j + 1] = dNdx
            B[4, 3*j + 1] = dNdz
            B[4, 3*j + 2] = dNdy
            B[5, 3*j + 2] = dNdx
            B[5, 3*j] = dNdz

        E_eff = E_elem[e]
        C_e = C0 * (E_eff / E0)
        ke = B.T @ C_e @ B * vol

        dofs = element_dofs[:, e]
        for i in range(12):
            for j in range(12):
                idx = e * 144 + i * 12 + j
                data[idx] = ke[i, j]
                row[idx] = dofs[i]
                col[idx] = dofs[j]

    return data, (row, col)


def assemble_stiffness_matrix_numba(
    basis, rho, E0, Emin, pval, nu,
    elem_func: Callable = simp_interpolation_numba
):
    p_coords = basis.mesh.p
    t_conn = basis.mesh.t
    element_dofs = basis.element_dofs
    E_elem = elem_func(rho, E0, Emin, pval)
    if isinstance(basis.mesh, skfem.MeshTet):
        data, rowcol = _assemble_stiffness_matrix_numba_tet(
            p_coords, t_conn, element_dofs, E0, Emin, nu, E_elem
        )
    elif isinstance(basis.mesh, skfem.MeshHex):
        raise NotImplementedError("use tet instead")
        # data, rowcol = _assemble_stiffness_matrix_hex8_gauss(
        #     p_coords, t_conn, element_dofs, E0, Emin, nu, E_elem
        # )
    else:
        raise ValueError("mesh is not tet nor hex")

    ndof = basis.N
    return scipy.sparse.coo_matrix(
        (data, rowcol), shape=(ndof, ndof)
    ).tocsr()