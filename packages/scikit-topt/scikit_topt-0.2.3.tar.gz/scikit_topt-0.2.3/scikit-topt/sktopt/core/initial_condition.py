
def estimate_f0_from_target_strain(
    E0: float, L0: float, A0: float,
    F_real: float, epsilon_target: float
):
    """
    Estimate a suitable force scale F0 based on a target strain.

    Parameters:
        E0 : float
            Representative Young's modulus [Pa].
        L0 : float
            Representative length scale [m].
        A0 : float
            Representative cross-sectional area [m²].
        F_real : float
            Actual applied force [N].
        epsilon_target : float
            Desired strain (e.g., 0.001 for 0.1%).

    Returns:
        float
            Estimated force scale F0 [N] that would produce the target strain.
    """
    return F_real / (epsilon_target * A0 * E0 / L0)


def auto_adjust_f0_from_displacement(
    F0_init: float, u_max: float, u_target: float
):
    """
    Adjust the initial force scale F0 after solving FEM,
    based on the observed maximum displacement.

    Parameters:
        F0_init : float
            Initial force scale.
        u_max : float
            Maximum displacement obtained from FEM (nondimensional).
        u_target : float
            Target maximum displacement (e.g., 0.001 for 1 mm if L0 = 1 m).

    Returns:
        float
            Adjusted F0 that would produce the target displacement.
    """
    if u_max == 0:
        raise ValueError("u_max must be non-zero to adjust F0.")
    return F0_init * (u_max / u_target)
