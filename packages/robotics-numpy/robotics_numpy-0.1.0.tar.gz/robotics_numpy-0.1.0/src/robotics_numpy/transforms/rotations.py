"""
Rotation transformations for robotics-numpy

This module provides efficient rotation matrix operations using only NumPy.
All functions are designed to work with both single rotations and batches.

Conventions:
- Rotation matrices are 3x3 NumPy arrays
- Euler angles follow ZYX convention (yaw-pitch-roll)
- Quaternions are [w, x, y, z] (scalar first)
- All angles are in radians
"""

from typing import Tuple, Union

import numpy as np

# Type aliases
ArrayLike = Union[float, int, np.ndarray]
RotationMatrix = np.ndarray  # 3x3 rotation matrix
Quaternion = np.ndarray      # [w, x, y, z] quaternion


def rotx(angle: ArrayLike) -> RotationMatrix:
    """
    Create rotation matrix about X-axis.

    Args:
        angle: Rotation angle in radians

    Returns:
        3x3 rotation matrix

    Examples:
        >>> R = rotx(np.pi/2)  # 90 degree rotation about X
        >>> R = rotx([0, np.pi/4, np.pi/2])  # Batch operation
    """
    angle = np.asarray(angle)
    c = np.cos(angle)
    s = np.sin(angle)

    if angle.ndim == 0:
        # Single rotation
        return np.array([
            [1, 0, 0],
            [0, c, -s],
            [0, s, c]
        ])
    else:
        # Batch rotations
        batch_size = angle.shape[0]
        R = np.zeros((batch_size, 3, 3))
        R[:, 0, 0] = 1
        R[:, 1, 1] = c
        R[:, 1, 2] = -s
        R[:, 2, 1] = s
        R[:, 2, 2] = c
        return R


def roty(angle: ArrayLike) -> RotationMatrix:
    """
    Create rotation matrix about Y-axis.

    Args:
        angle: Rotation angle in radians

    Returns:
        3x3 rotation matrix
    """
    angle = np.asarray(angle)
    c = np.cos(angle)
    s = np.sin(angle)

    if angle.ndim == 0:
        return np.array([
            [c, 0, s],
            [0, 1, 0],
            [-s, 0, c]
        ])
    else:
        batch_size = angle.shape[0]
        R = np.zeros((batch_size, 3, 3))
        R[:, 0, 0] = c
        R[:, 0, 2] = s
        R[:, 1, 1] = 1
        R[:, 2, 0] = -s
        R[:, 2, 2] = c
        return R


def rotz(angle: ArrayLike) -> RotationMatrix:
    """
    Create rotation matrix about Z-axis.

    Args:
        angle: Rotation angle in radians

    Returns:
        3x3 rotation matrix
    """
    angle = np.asarray(angle)
    c = np.cos(angle)
    s = np.sin(angle)

    if angle.ndim == 0:
        return np.array([
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1]
        ])
    else:
        batch_size = angle.shape[0]
        R = np.zeros((batch_size, 3, 3))
        R[:, 0, 0] = c
        R[:, 0, 1] = -s
        R[:, 1, 0] = s
        R[:, 1, 1] = c
        R[:, 2, 2] = 1
        return R


def rpy2r(roll: float, pitch: float, yaw: float) -> RotationMatrix:
    """
    Convert roll-pitch-yaw angles to rotation matrix.

    Applies rotations in order: Rz(yaw) * Ry(pitch) * Rx(roll)

    Args:
        roll: Rotation about X-axis (radians)
        pitch: Rotation about Y-axis (radians)
        yaw: Rotation about Z-axis (radians)

    Returns:
        3x3 rotation matrix

    Examples:
        >>> R = rpy2r(0.1, 0.2, 0.3)  # Small rotations
        >>> R = rpy2r(0, 0, np.pi/2)  # 90 deg yaw
    """
    return rotz(yaw) @ roty(pitch) @ rotx(roll)


def r2rpy(R: RotationMatrix) -> Tuple[float, float, float]:
    """
    Convert rotation matrix to roll-pitch-yaw angles.

    Args:
        R: 3x3 rotation matrix

    Returns:
        Tuple of (roll, pitch, yaw) in radians

    Raises:
        ValueError: If R is not a valid rotation matrix

    Examples:
        >>> R = rpy2r(0.1, 0.2, 0.3)
        >>> roll, pitch, yaw = r2rpy(R)
    """
    if not is_rotation_matrix(R):
        raise ValueError("Input is not a valid rotation matrix")

    # Extract angles using ZYX convention
    pitch = np.arcsin(-R[2, 0])

    # Check for gimbal lock
    if np.abs(np.cos(pitch)) < 1e-6:
        # Gimbal lock case
        roll = 0.0
        if pitch > 0:
            yaw = np.arctan2(R[0, 1], R[1, 1])
        else:
            yaw = np.arctan2(-R[0, 1], R[1, 1])
    else:
        roll = np.arctan2(R[2, 1], R[2, 2])
        yaw = np.arctan2(R[1, 0], R[0, 0])

    return roll, pitch, yaw


def eul2r(phi: float, theta: float, psi: float,
          convention: str = 'ZYZ') -> RotationMatrix:
    """
    Convert Euler angles to rotation matrix.

    Args:
        phi: First rotation angle (radians)
        theta: Second rotation angle (radians)
        psi: Third rotation angle (radians)
        convention: Euler angle convention ('ZYZ', 'ZYX')

    Returns:
        3x3 rotation matrix

    Examples:
        >>> R = eul2r(0.1, 0.2, 0.3, 'ZYZ')
    """
    if convention == 'ZYZ':
        return rotz(phi) @ roty(theta) @ rotz(psi)
    elif convention == 'ZYX':
        return rotz(phi) @ roty(theta) @ rotx(psi)
    else:
        raise ValueError(f"Unsupported convention: {convention}")


def r2eul(R: RotationMatrix, convention: str = 'ZYZ') -> Tuple[float, float, float]:
    """
    Convert rotation matrix to Euler angles.

    Args:
        R: 3x3 rotation matrix
        convention: Euler angle convention ('ZYZ', 'ZYX')

    Returns:
        Tuple of three Euler angles in radians
    """
    if not is_rotation_matrix(R):
        raise ValueError("Input is not a valid rotation matrix")

    if convention == 'ZYZ':
        theta = np.arccos(np.clip(R[2, 2], -1, 1))

        if np.abs(np.sin(theta)) < 1e-6:
            # Singularity case
            phi = 0.0
            if theta < 1e-6:  # theta ≈ 0
                psi = np.arctan2(R[1, 0], R[0, 0])
            else:  # theta ≈ π
                psi = np.arctan2(-R[1, 0], R[0, 0])
        else:
            phi = np.arctan2(R[1, 2], R[0, 2])
            psi = np.arctan2(R[2, 1], -R[2, 0])

        return phi, theta, psi

    elif convention == 'ZYX':
        return r2rpy(R)

    else:
        raise ValueError(f"Unsupported convention: {convention}")


def quat2r(q: Quaternion) -> RotationMatrix:
    """
    Convert quaternion to rotation matrix.

    Args:
        q: Quaternion [w, x, y, z] (scalar first)

    Returns:
        3x3 rotation matrix

    Examples:
        >>> q = [1, 0, 0, 0]  # Identity quaternion
        >>> R = quat2r(q)
    """
    q = np.asarray(q, dtype=float)
    if q.shape != (4,):
        raise ValueError("Quaternion must be a 4-element array")

    # Normalize quaternion
    q = quat_normalize(q)
    w, x, y, z = q

    # Convert to rotation matrix
    R = np.array([
        [1 - 2*(y*y + z*z), 2*(x*y - w*z), 2*(x*z + w*y)],
        [2*(x*y + w*z), 1 - 2*(x*x + z*z), 2*(y*z - w*x)],
        [2*(x*z - w*y), 2*(y*z + w*x), 1 - 2*(x*x + y*y)]
    ])

    return R


def r2quat(R: RotationMatrix) -> Quaternion:
    """
    Convert rotation matrix to quaternion.

    Args:
        R: 3x3 rotation matrix

    Returns:
        Quaternion [w, x, y, z]

    Examples:
        >>> R = np.eye(3)  # Identity matrix
        >>> q = r2quat(R)  # Returns [1, 0, 0, 0]
    """
    if not is_rotation_matrix(R):
        raise ValueError("Input is not a valid rotation matrix")

    # Shepperd's method for numerical stability
    trace = np.trace(R)

    if trace > 0:
        s = np.sqrt(trace + 1.0) * 2  # s = 4 * w
        w = 0.25 * s
        x = (R[2, 1] - R[1, 2]) / s
        y = (R[0, 2] - R[2, 0]) / s
        z = (R[1, 0] - R[0, 1]) / s
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        s = np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2  # s = 4 * x
        w = (R[2, 1] - R[1, 2]) / s
        x = 0.25 * s
        y = (R[0, 1] + R[1, 0]) / s
        z = (R[0, 2] + R[2, 0]) / s
    elif R[1, 1] > R[2, 2]:
        s = np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2  # s = 4 * y
        w = (R[0, 2] - R[2, 0]) / s
        x = (R[0, 1] + R[1, 0]) / s
        y = 0.25 * s
        z = (R[1, 2] + R[2, 1]) / s
    else:
        s = np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2  # s = 4 * z
        w = (R[1, 0] - R[0, 1]) / s
        x = (R[0, 2] + R[2, 0]) / s
        y = (R[1, 2] + R[2, 1]) / s
        z = 0.25 * s

    return np.array([w, x, y, z])


def quat_multiply(q1: Quaternion, q2: Quaternion) -> Quaternion:
    """
    Multiply two quaternions.

    Args:
        q1: First quaternion [w, x, y, z]
        q2: Second quaternion [w, x, y, z]

    Returns:
        Product quaternion q1 * q2
    """
    q1 = np.asarray(q1)
    q2 = np.asarray(q2)

    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2

    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 - x1*z2 + y1*w2 + z1*x2
    z = w1*z2 + x1*y2 - y1*x2 + z1*w2

    return np.array([w, x, y, z])


def quat_inverse(q: Quaternion) -> Quaternion:
    """
    Compute quaternion inverse (conjugate for unit quaternions).

    Args:
        q: Quaternion [w, x, y, z]

    Returns:
        Inverse quaternion
    """
    q = np.asarray(q)
    return np.array([q[0], -q[1], -q[2], -q[3]])


def quat_normalize(q: Quaternion) -> Quaternion:
    """
    Normalize quaternion to unit length.

    Args:
        q: Quaternion [w, x, y, z]

    Returns:
        Normalized quaternion
    """
    q = np.asarray(q, dtype=float)
    norm = np.linalg.norm(q)
    if norm < 1e-8:
        raise ValueError("Cannot normalize zero quaternion")
    return q / norm


def is_rotation_matrix(R: np.ndarray, tol: float = 1e-6) -> bool:
    """
    Check if matrix is a valid rotation matrix.

    Args:
        R: Matrix to check
        tol: Tolerance for checks

    Returns:
        True if R is a valid rotation matrix

    Examples:
        >>> R = np.eye(3)
        >>> is_rotation_matrix(R)  # True
        >>> is_rotation_matrix(np.ones((3, 3)))  # False
    """
    if R.shape != (3, 3):
        return False

    # Check if orthogonal: R @ R.T ≈ I
    should_be_identity = R @ R.T
    identity = np.eye(3)
    if not np.allclose(should_be_identity, identity, atol=tol):
        return False

    # Check if determinant is 1 (proper rotation)
    if not np.isclose(np.linalg.det(R), 1.0, atol=tol):
        return False

    return True


# Convenience functions for common rotations
def rx(angle: ArrayLike) -> RotationMatrix:
    """Alias for rotx."""
    return rotx(angle)


def ry(angle: ArrayLike) -> RotationMatrix:
    """Alias for roty."""
    return roty(angle)


def rz(angle: ArrayLike) -> RotationMatrix:
    """Alias for rotz."""
    return rotz(angle)


# Constants
IDENTITY_QUAT = np.array([1.0, 0.0, 0.0, 0.0])
IDENTITY_ROT = np.eye(3)
