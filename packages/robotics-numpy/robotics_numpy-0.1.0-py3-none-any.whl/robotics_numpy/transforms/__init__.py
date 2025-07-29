"""
Transforms module for robotics-numpy

This module provides 3D transformation utilities including:
- Homogeneous transformation matrices (SE3)
- Rotation matrices (SO3)
- Quaternions
- Euler angles and roll-pitch-yaw
- Pose representations

The module is designed to be lightweight and fast, using only NumPy.
"""

from .homogeneous import (
    SE3_from_matrix,
    homogeneous_inverse,
    is_homogeneous,
    rotmat,
    transform_point,
    transform_points,
    transl,
)
from .pose import SE3, SO3
from .rotations import (
    eul2r,
    is_rotation_matrix,
    quat2r,
    quat_inverse,
    quat_multiply,
    quat_normalize,
    r2eul,
    r2quat,
    r2rpy,
    rotx,
    roty,
    rotz,
    rpy2r,
)

__all__ = [
    # Homogeneous transformations
    "transl",
    "rotmat",
    "SE3_from_matrix",
    "homogeneous_inverse",
    "is_homogeneous",
    "transform_point",
    "transform_points",

    # Rotations
    "rotx",
    "roty",
    "rotz",
    "rpy2r",
    "r2rpy",
    "eul2r",
    "r2eul",
    "quat2r",
    "r2quat",
    "quat_multiply",
    "quat_inverse",
    "quat_normalize",
    "is_rotation_matrix",

    # Pose classes
    "SE3",
    "SO3",
]
