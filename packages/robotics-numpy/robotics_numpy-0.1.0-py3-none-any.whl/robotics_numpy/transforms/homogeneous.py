"""
Homogeneous transformation matrices for robotics-numpy

This module provides efficient SE(3) homogeneous transformation operations using only NumPy.
All functions are designed to work with both single transformations and batches.

Conventions:
- Homogeneous transformation matrices are 4x4 NumPy arrays
- Position vectors are 3-element arrays [x, y, z]
- Rotation matrices are 3x3 arrays
- SE(3) format: [[R, t], [0, 1]] where R is 3x3 rotation, t is 3x1 translation
"""

from typing import Optional, Union

import numpy as np

from .rotations import is_rotation_matrix, rotx, roty, rotz

# Type aliases
ArrayLike = Union[float, int, np.ndarray]
Vector3 = np.ndarray      # 3-element position vector
Matrix4x4 = np.ndarray    # 4x4 homogeneous transformation matrix
Matrix3x3 = np.ndarray    # 3x3 rotation matrix


def transl(x: ArrayLike, y: Optional[ArrayLike] = None, z: Optional[ArrayLike] = None) -> Matrix4x4:
    """
    Create pure translation transformation matrix.

    Args:
        x: X translation or 3-element vector [x, y, z]
        y: Y translation (if x is scalar)
        z: Z translation (if x is scalar)

    Returns:
        4x4 homogeneous transformation matrix

    Examples:
        >>> T1 = transl(1, 2, 3)        # Translation by [1, 2, 3]
        >>> T2 = transl([1, 2, 3])      # Same as above
        >>> T3 = transl(np.array([1, 2, 3]))  # NumPy array input
    """
    if y is None and z is None:
        # Single argument case - expect 3-element vector
        pos = np.asarray(x)
        if pos.shape == (3,):
            x, y, z = pos
        else:
            raise ValueError("Single argument must be 3-element vector")
    elif y is not None and z is not None:
        # Three scalar arguments
        x, y, z = float(x), float(y), float(z)
    else:
        raise ValueError("Must provide either 1 or 3 arguments")

    T = np.eye(4)
    T[0, 3] = x
    T[1, 3] = y
    T[2, 3] = z
    return T


def rotmat(R: Matrix3x3, t: Optional[Vector3] = None) -> Matrix4x4:
    """
    Create homogeneous transformation from rotation matrix and optional translation.

    Args:
        R: 3x3 rotation matrix
        t: 3-element translation vector (default: zero)

    Returns:
        4x4 homogeneous transformation matrix

    Examples:
        >>> R = rotx(np.pi/2)
        >>> T1 = rotmat(R)                    # Pure rotation
        >>> T2 = rotmat(R, [1, 2, 3])        # Rotation + translation
    """
    R = np.asarray(R)
    if R.shape != (3, 3):
        raise ValueError("Rotation matrix must be 3x3")

    if not is_rotation_matrix(R):
        raise ValueError("Input is not a valid rotation matrix")

    T = np.eye(4)
    T[:3, :3] = R

    if t is not None:
        t = np.asarray(t)
        if t.shape != (3,):
            raise ValueError("Translation vector must be 3-element")
        T[:3, 3] = t

    return T


def SE3_from_matrix(T: Matrix4x4) -> Matrix4x4:
    """
    Validate and return SE(3) transformation matrix.

    Args:
        T: 4x4 matrix to validate

    Returns:
        4x4 SE(3) transformation matrix

    Raises:
        ValueError: If T is not a valid SE(3) matrix

    Examples:
        >>> T = np.eye(4)
        >>> T_valid = SE3_from_matrix(T)
    """
    T = np.asarray(T)
    if not is_homogeneous(T):
        raise ValueError("Input is not a valid SE(3) transformation matrix")
    return T


def homogeneous_inverse(T: Matrix4x4) -> Matrix4x4:
    """
    Compute inverse of homogeneous transformation matrix efficiently.

    For SE(3) matrix T = [[R, t], [0, 1]], the inverse is [[R^T, -R^T*t], [0, 1]]

    Args:
        T: 4x4 homogeneous transformation matrix

    Returns:
        Inverse transformation matrix

    Examples:
        >>> T = transl(1, 2, 3) @ rotmat(rotx(np.pi/4))
        >>> T_inv = homogeneous_inverse(T)
        >>> np.allclose(T @ T_inv, np.eye(4))  # Should be True
    """
    if not is_homogeneous(T):
        raise ValueError("Input is not a valid SE(3) transformation matrix")

    R = T[:3, :3]
    t = T[:3, 3]

    T_inv = np.eye(4)
    T_inv[:3, :3] = R.T
    T_inv[:3, 3] = -R.T @ t

    return T_inv


def is_homogeneous(T: np.ndarray, tol: float = 1e-6) -> bool:
    """
    Check if matrix is a valid SE(3) homogeneous transformation matrix.

    Args:
        T: Matrix to check
        tol: Tolerance for numerical checks

    Returns:
        True if T is a valid SE(3) matrix

    Examples:
        >>> T = np.eye(4)
        >>> is_homogeneous(T)  # True
        >>> is_homogeneous(np.ones((4, 4)))  # False
    """
    if T.shape != (4, 4):
        return False

    # Check bottom row is [0, 0, 0, 1]
    expected_bottom = np.array([0, 0, 0, 1])
    if not np.allclose(T[3, :], expected_bottom, atol=tol):
        return False

    # Check if rotation part is valid
    R = T[:3, :3]
    if not is_rotation_matrix(R, tol):
        return False

    return True


def extract_rotation(T: Matrix4x4) -> Matrix3x3:
    """
    Extract 3x3 rotation matrix from homogeneous transformation.

    Args:
        T: 4x4 homogeneous transformation matrix

    Returns:
        3x3 rotation matrix

    Examples:
        >>> T = rotmat(rotx(np.pi/4), [1, 2, 3])
        >>> R = extract_rotation(T)
    """
    if not is_homogeneous(T):
        raise ValueError("Input is not a valid SE(3) transformation matrix")
    return T[:3, :3].copy()


def extract_translation(T: Matrix4x4) -> Vector3:
    """
    Extract translation vector from homogeneous transformation.

    Args:
        T: 4x4 homogeneous transformation matrix

    Returns:
        3-element translation vector

    Examples:
        >>> T = rotmat(rotx(np.pi/4), [1, 2, 3])
        >>> t = extract_translation(T)  # Returns [1, 2, 3]
    """
    if not is_homogeneous(T):
        raise ValueError("Input is not a valid SE(3) transformation matrix")
    return T[:3, 3].copy()


def transform_point(T: Matrix4x4, p: Vector3) -> Vector3:
    """
    Transform a 3D point using homogeneous transformation.

    Args:
        T: 4x4 homogeneous transformation matrix
        p: 3-element point coordinates

    Returns:
        Transformed 3D point

    Examples:
        >>> T = transl(1, 0, 0)  # Translation by [1, 0, 0]
        >>> p_new = transform_point(T, [0, 0, 0])  # Returns [1, 0, 0]
    """
    if not is_homogeneous(T):
        raise ValueError("Input is not a valid SE(3) transformation matrix")

    p = np.asarray(p)
    if p.shape != (3,):
        raise ValueError("Point must be 3-element vector")

    # Convert to homogeneous coordinates and transform
    p_homo = np.append(p, 1)
    p_transformed = T @ p_homo
    return p_transformed[:3]


def transform_points(T: Matrix4x4, points: np.ndarray) -> np.ndarray:
    """
    Transform multiple 3D points using homogeneous transformation.

    Args:
        T: 4x4 homogeneous transformation matrix
        points: Nx3 array of points

    Returns:
        Nx3 array of transformed points

    Examples:
        >>> T = rotx(np.pi/2)
        >>> points = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        >>> transformed = transform_points(T, points)
    """
    if not is_homogeneous(T):
        raise ValueError("Input is not a valid SE(3) transformation matrix")

    points = np.asarray(points)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("Points must be Nx3 array")

    # Add homogeneous coordinate
    ones = np.ones((points.shape[0], 1))
    points_homo = np.hstack([points, ones])

    # Transform all points
    transformed_homo = (T @ points_homo.T).T
    return transformed_homo[:, :3]


# Convenience functions for common transformations
def SE3_translation(x: ArrayLike, y: Optional[ArrayLike] = None, z: Optional[ArrayLike] = None) -> Matrix4x4:
    """Alias for transl()."""
    return transl(x, y, z)


def SE3_rotation_x(angle: float) -> Matrix4x4:
    """Create SE(3) transformation for rotation about X-axis."""
    return rotmat(rotx(angle))


def SE3_rotation_y(angle: float) -> Matrix4x4:
    """Create SE(3) transformation for rotation about Y-axis."""
    return rotmat(roty(angle))


def SE3_rotation_z(angle: float) -> Matrix4x4:
    """Create SE(3) transformation for rotation about Z-axis."""
    return rotmat(rotz(angle))


def SE3_from_rt(R: Matrix3x3, t: Vector3) -> Matrix4x4:
    """Create SE(3) transformation from rotation matrix and translation vector."""
    return rotmat(R, t)


# Constants
IDENTITY_SE3 = np.eye(4)
