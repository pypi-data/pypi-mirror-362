"""
Robotics NumPy - A lightweight robotics library built on NumPy

A lightweight, high-performance robotics library focusing on:
- Forward and inverse kinematics
- Robot dynamics
- Trajectory planning
- 3D transformations

Only requires NumPy as core dependency, with optional Plotly for visualization.

Examples:
    >>> import robotics_numpy as rn
    >>> # Create a 6-DOF robot arm
    >>> robot = rn.models.create_6dof_arm()
    >>> # Forward kinematics
    >>> T = robot.fkine([0, 0, 0, 0, 0, 0])
    >>> # Inverse kinematics
    >>> q = robot.ikine(T)
"""

__version__ = "0.1.0"
__author__ = "Chaoyue"
__email__ = "chaoyue@example.com"

# Core imports
from . import kinematics, models, transforms

# Optional imports (fail gracefully if dependencies not available)
try:
    from . import visualization
    _HAS_VISUALIZATION = True
    # Ensure visualization is accessible even if not used here
    _ = visualization
except ImportError:
    _HAS_VISUALIZATION = False

# Version info
__all__ = [
    "transforms",
    "kinematics",
    "models",
]

if _HAS_VISUALIZATION:
    __all__.append("visualization")

# Convenience imports for common functionality
from .transforms.homogeneous import (
    SE3_from_matrix,
    rotmat,
    transl,
)
from .transforms.pose import SE3, SO3
from .transforms.rotations import (
    eul2r,
    r2eul,
    r2rpy,
    rotx,
    roty,
    rotz,
    rpy2r,
)

# Add convenience imports to __all__
__all__.extend([
    "SE3",
    "SO3",
    "rotz",
    "roty",
    "rotx",
    "rpy2r",
    "r2rpy",
    "eul2r",
    "r2eul",
    "transl",
    "rotmat",
    "SE3_from_matrix",
])

def about() -> None:
    """Print information about robotics-numpy."""
    print(f"Robotics NumPy {__version__}")
    print("A lightweight robotics library built on NumPy")
    print(f"Author: {__author__}")
    print()
    print("Core modules:")
    print("  ✅ transforms: 3D transformations, rotations, poses")
    print("  ✅ kinematics: Forward kinematics, DH parameters")
    print("  ✅ models: Robot models (Stanford Arm, etc.)")
    print("  🚧 dynamics: Robot dynamics and control (coming in v0.3.0)")
    print("  🚧 trajectory: Trajectory generation and planning (coming in v0.3.0)")
    if _HAS_VISUALIZATION:
        print("  🚧 visualization: 3D plotting (coming in v0.2.0)")
    else:
        print("  🚧 visualization: Not available (install with pip install robotics-numpy[visualization])")
    print()
    print("Quick start:")
    print("  >>> import robotics_numpy as rn")
    print("  >>> robot = rn.models.Stanford()")
    print("  >>> T = robot.fkine([0, 0, 0, 0, 0, 0])")
    print("  >>> print(T)")
    print()
    print("Available models:")
    print("  >>> rn.models.list_models()  # See all available robots")
