"""
Models module for robotics-numpy

This module provides robot model functionality including:
- DH parameter robot definitions
- Common robot models (Stanford Arm, 6-DOF arms, etc.)
- Robot model validation and manipulation
- Forward kinematics computation

The module is designed to be lightweight and fast, using only NumPy.
"""

from .dh_link import (
    DHLink,
    RevoluteDH,
    PrismaticDH,
    dh_check_parameters,
    create_6dof_revolute_arm,
)

from .dh_robot import (
    DHRobot,
    create_simple_arm,
    create_planar_arm,
)

from .stanford import (
    Stanford,
    create_stanford_arm,
)

from .generic import (
    Generic,
    create_generic_robot,
)

__all__ = [
    # DH Link classes
    "DHLink",
    "RevoluteDH",
    "PrismaticDH",
    "dh_check_parameters",
    "create_6dof_revolute_arm",

    # Robot classes
    "DHRobot",
    "create_simple_arm",
    "create_planar_arm",

    # Specific robot models
    "Stanford",
    "create_stanford_arm",

    # Generic robot models
    "Generic",
    "create_generic_robot",
]

# Version for Phase 2
_MODELS_VERSION = "0.2.0-dev"

# Available robot models
AVAILABLE_MODELS = {
    "stanford": "Stanford Arm (6-DOF with prismatic joint)",
    "simple_arm": "Simple n-DOF revolute arm for testing",
    "planar_arm": "Planar n-DOF arm (all joints parallel)",
    "generic": "Generic robot with configurable DH parameters",
}

def list_models() -> None:
    """Print available robot models."""
    print("Available Robot Models in robotics-numpy:")
    print("=" * 50)
    for name, description in AVAILABLE_MODELS.items():
        print(f"  {name:15s}: {description}")
    print()
    print("Usage examples:")
    print("  >>> from robotics_numpy.models import Stanford, Generic")
    print("  >>> robot = Stanford()")
    print("  >>> T = robot.fkine([0, 0, 0, 0, 0, 0])")
    print("  >>> generic_robot = Generic(dofs=4)")

def about_models() -> None:
    """Print information about models module."""
    print("Robotics NumPy - Models Module")
    print("=============================")
    print()
    print("Features implemented:")
    print("  ✅ DH parameter robot definitions")
    print("  ✅ Forward kinematics computation")
    print("  ✅ Stanford Arm robot model")
    print("  ✅ Simple and planar arm generators")
    print("  ✅ Robot model validation")
    print()
    print("Coming soon:")
    print("  🚧 URDF parsing support")
    print("  🚧 More industrial robot models")
    print("  🚧 Robot visualization")
    print()
    list_models()
