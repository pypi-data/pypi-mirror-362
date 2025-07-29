"""
Kinematics module for robotics-numpy

This module provides robot kinematics functionality including:
- Forward kinematics using DH parameters
- Inverse kinematics (numerical and analytical methods)
- Jacobian computation (geometric and analytical)
- Velocity and acceleration kinematics

The module is designed to be lightweight and fast, using only NumPy.
"""

from .forward import (
    fkine_dh,
    fkine_dh_all,
    fkine_dh_partial,
    fkine_dh_batch,
    link_poses,
    joint_axes,
    validate_joint_config,
    fkine_performance_test,
    fkine_6dof,
    fkine_planar,
)

# Inverse kinematics will be implemented in Phase 2.1
# from .inverse import (
#     ikine_lm,
#     ikine_newton,
#     ikine_numerical,
# )

# Jacobian computation implemented in Phase 2.2
from .jacobian import (
    tr2jac,
    jacobe,
    jacob0,
    manipulability,
    joint_velocity_ellipsoid,
)

__all__ = [
    # Forward kinematics
    "fkine_dh",
    "fkine_dh_all",
    "fkine_dh_partial",
    "fkine_dh_batch",
    "link_poses",
    "joint_axes",
    "validate_joint_config",
    "fkine_performance_test",
    "fkine_6dof",
    "fkine_planar",
    # Coming in Phase 2.1
    # "ikine_lm",
    # "ikine_newton",
    # "ikine_numerical",
    # Jacobian computation
    "tr2jac",
    "jacobe",
    "jacob0",
    "manipulability",
    "joint_velocity_ellipsoid",
]

# Version for Phase 2
_KINEMATICS_VERSION = "0.2.0-dev"


def about_kinematics() -> None:
    """Print information about kinematics module."""
    print("Robotics NumPy - Kinematics Module")
    print("==================================")
    print()
    print("Features implemented:")
    print("  ✅ Forward kinematics using DH parameters")
    print("  ✅ Batch forward kinematics computation")
    print("  ✅ Partial chain kinematics")
    print("  ✅ Link pose computation")
    print("  ✅ Joint axis computation")
    print("  ✅ Configuration validation")
    print("  ✅ Performance testing utilities")
    print()
    print("Coming soon in Phase 2:")
    print("  🚧 Numerical inverse kinematics (LM, Newton-Raphson)")
    print("  🚧 Analytical inverse kinematics for specific robots")
    print("  ✅ Geometric and analytical Jacobian computation")
    print("  🚧 Velocity and acceleration kinematics")
    print("  🚧 Singularity analysis")
    print()
    print("Usage examples:")
    print("  >>> from robotics_numpy.kinematics import fkine_dh")
    print("  >>> from robotics_numpy.models import Stanford")
    print("  >>> robot = Stanford()")
    print("  >>> T = robot.fkine([0, 0, 0, 0, 0, 0])")
    print("  >>> poses = robot.fkine_all([0, 0, 0, 0, 0, 0])")
    print("  >>> J = robot.jacob0([0, 0, 0, 0, 0, 0])")
    print("  >>> m = robot.manipulability([0, 0, 0, 0, 0, 0])")
