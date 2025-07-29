"""
SE(3) and SO(3) classes for robotics-numpy

This module provides object-oriented interfaces for 3D transformations:
- SE3: Special Euclidean group SE(3) for rigid body transformations
- SO3: Special Orthogonal group SO(3) for rotations

These classes provide intuitive APIs while maintaining high performance through NumPy.
"""

from typing import List, Optional, Tuple, Union

import numpy as np

from .homogeneous import (
    extract_rotation,
    extract_translation,
    homogeneous_inverse,
    is_homogeneous,
    rotmat,
    transform_point,
    transform_points,
    transl,
)
from .rotations import (
    eul2r,
    is_rotation_matrix,
    quat2r,
    r2eul,
    r2quat,
    r2rpy,
    rotx,
    roty,
    rotz,
    rpy2r,
)

# Type aliases
ArrayLike = Union[float, int, np.ndarray, List[float]]
Vector3 = Union[np.ndarray, List[float]]
Matrix3x3 = np.ndarray
Matrix4x4 = np.ndarray


class SO3:
    """
    Special Orthogonal group SO(3) - 3D rotations.

    Represents rotations in 3D space using rotation matrices.
    Provides convenient methods for creation, composition, and conversion.

    Examples:
        >>> R1 = SO3.Rx(np.pi/2)          # Rotation about X-axis
        >>> R2 = SO3.RPY(0.1, 0.2, 0.3)   # From roll-pitch-yaw
        >>> R3 = R1 * R2                   # Composition
        >>> rpy = R3.rpy()                 # Extract RPY angles
    """

    def __init__(self, matrix: Optional[Matrix3x3] = None):
        """
        Initialize SO(3) rotation.

        Args:
            matrix: 3x3 rotation matrix (default: identity)

        Examples:
            >>> R1 = SO3()                    # Identity rotation
            >>> R2 = SO3(np.eye(3))          # From matrix
            >>> R3 = SO3.Rx(np.pi/4)         # Factory method
        """
        if matrix is None:
            self._matrix = np.eye(3)
        else:
            matrix = np.asarray(matrix)
            if not is_rotation_matrix(matrix):
                raise ValueError("Input is not a valid rotation matrix")
            self._matrix = matrix.copy()

    @property
    def matrix(self) -> Matrix3x3:
        """Get the rotation matrix."""
        return self._matrix.copy()

    @property
    def R(self) -> Matrix3x3:
        """Alias for matrix property."""
        return self.matrix

    # Factory methods for common rotations
    @classmethod
    def Rx(cls, angle: float) -> 'SO3':
        """Create rotation about X-axis."""
        return cls(rotx(angle))

    @classmethod
    def Ry(cls, angle: float) -> 'SO3':
        """Create rotation about Y-axis."""
        return cls(roty(angle))

    @classmethod
    def Rz(cls, angle: float) -> 'SO3':
        """Create rotation about Z-axis."""
        return cls(rotz(angle))

    @classmethod
    def RPY(cls, roll: float, pitch: float, yaw: float) -> 'SO3':
        """Create rotation from roll-pitch-yaw angles."""
        return cls(rpy2r(roll, pitch, yaw))

    @classmethod
    def Eul(cls, phi: float, theta: float, psi: float, convention: str = 'ZYZ') -> 'SO3':
        """Create rotation from Euler angles."""
        return cls(eul2r(phi, theta, psi, convention))

    @classmethod
    def Quaternion(cls, q: ArrayLike) -> 'SO3':
        """Create rotation from quaternion [w, x, y, z]."""
        return cls(quat2r(np.asarray(q)))

    @classmethod
    def Random(cls) -> 'SO3':
        """Create random rotation matrix."""
        # Generate random rotation using quaternion method
        u = np.random.random(3)
        q = np.array([
            np.sqrt(1 - u[0]) * np.sin(2 * np.pi * u[1]),
            np.sqrt(1 - u[0]) * np.cos(2 * np.pi * u[1]),
            np.sqrt(u[0]) * np.sin(2 * np.pi * u[2]),
            np.sqrt(u[0]) * np.cos(2 * np.pi * u[2])
        ])
        return cls.Quaternion(q)

    # Conversion methods
    def rpy(self) -> Tuple[float, float, float]:
        """Extract roll-pitch-yaw angles."""
        return r2rpy(self._matrix)

    def eul(self, convention: str = 'ZYZ') -> Tuple[float, float, float]:
        """Extract Euler angles."""
        return r2eul(self._matrix, convention)

    def quaternion(self) -> np.ndarray:
        """Extract quaternion [w, x, y, z]."""
        return r2quat(self._matrix)

    # Operations
    def inv(self) -> 'SO3':
        """Compute inverse (transpose for rotation matrices)."""
        return SO3(self._matrix.T)

    def __mul__(self, other: 'SO3') -> 'SO3':
        """Compose rotations: self * other."""
        if not isinstance(other, SO3):
            raise TypeError("Can only multiply SO3 with SO3")
        return SO3(self._matrix @ other._matrix)

    def __rmul__(self, other):
        """Right multiplication (not supported for SO3)."""
        raise TypeError("Right multiplication not supported")

    def __pow__(self, n: int) -> 'SO3':
        """Power operation (repeated multiplication)."""
        if not isinstance(n, int):
            raise TypeError("Exponent must be integer")

        if n == 0:
            return SO3()  # Identity
        elif n > 0:
            result = SO3(self._matrix)
            for _ in range(n - 1):
                result = result * self
            return result
        else:
            return (self.inv() ** (-n))

    def rotate(self, vector: Vector3) -> np.ndarray:
        """Rotate a 3D vector."""
        v = np.asarray(vector)
        if v.shape != (3,):
            raise ValueError("Vector must be 3-element")
        return self._matrix @ v

    def __repr__(self) -> str:
        """String representation."""
        return f"SO3(\n{self._matrix})"

    def __str__(self) -> str:
        """Compact string representation."""
        rpy = self.rpy()
        return f"SO3: RPY=({rpy[0]:.3f}, {rpy[1]:.3f}, {rpy[2]:.3f}) rad"


class SE3:
    """
    Special Euclidean group SE(3) - rigid body transformations.

    Represents rigid body transformations (rotation + translation) in 3D space
    using 4x4 homogeneous transformation matrices.

    Examples:
        >>> T1 = SE3.Trans(1, 2, 3)           # Pure translation
        >>> T2 = SE3.Rx(np.pi/2)             # Pure rotation
        >>> T3 = T1 * T2                      # Composition
        >>> p_new = T3 * [0, 0, 0]           # Transform point
    """

    def __init__(self, matrix: Optional[Matrix4x4] = None):
        """
        Initialize SE(3) transformation.

        Args:
            matrix: 4x4 homogeneous transformation matrix (default: identity)

        Examples:
            >>> T1 = SE3()                    # Identity transformation
            >>> T2 = SE3(np.eye(4))          # From matrix
            >>> T3 = SE3.Trans(1, 2, 3)      # Factory method
        """
        if matrix is None:
            self._matrix = np.eye(4)
        else:
            matrix = np.asarray(matrix)
            if not is_homogeneous(matrix):
                raise ValueError("Input is not a valid SE(3) transformation matrix")
            self._matrix = matrix.copy()

    @property
    def matrix(self) -> Matrix4x4:
        """Get the transformation matrix."""
        return self._matrix.copy()

    @property
    def T(self) -> Matrix4x4:
        """Alias for matrix property."""
        return self.matrix

    @property
    def R(self) -> Matrix3x3:
        """Get rotation part as 3x3 matrix."""
        return extract_rotation(self._matrix)

    @property
    def t(self) -> np.ndarray:
        """Get translation part as 3-element vector."""
        return extract_translation(self._matrix)

    @property
    def rotation(self) -> SO3:
        """Get rotation part as SO3 object."""
        return SO3(self.R)

    @property
    def translation(self) -> np.ndarray:
        """Alias for t property."""
        return self.t

    # Factory methods
    @classmethod
    def Trans(cls, x: ArrayLike, y: Optional[float] = None, z: Optional[float] = None) -> 'SE3':
        """Create pure translation transformation."""
        return cls(transl(x, y, z))

    @classmethod
    def Rx(cls, angle: float) -> 'SE3':
        """Create rotation about X-axis."""
        return cls(rotmat(rotx(angle)))

    @classmethod
    def Ry(cls, angle: float) -> 'SE3':
        """Create rotation about Y-axis."""
        return cls(rotmat(roty(angle)))

    @classmethod
    def Rz(cls, angle: float) -> 'SE3':
        """Create rotation about Z-axis."""
        return cls(rotmat(rotz(angle)))

    @classmethod
    def RPY(cls, roll: float, pitch: float, yaw: float,
           t: Optional[Vector3] = None) -> 'SE3':
        """Create transformation from roll-pitch-yaw angles and optional translation."""
        R = rpy2r(roll, pitch, yaw)
        return cls(rotmat(R, t))

    @classmethod
    def Eul(cls, phi: float, theta: float, psi: float,
           t: Optional[Vector3] = None, convention: str = 'ZYZ') -> 'SE3':
        """Create transformation from Euler angles and optional translation."""
        R = eul2r(phi, theta, psi, convention)
        return cls(rotmat(R, t))

    @classmethod
    def Rt(cls, R: Union[Matrix3x3, SO3], t: Vector3) -> 'SE3':
        """Create transformation from rotation and translation."""
        if isinstance(R, SO3):
            R = R.matrix
        return cls(rotmat(R, t))

    @classmethod
    def Random(cls) -> 'SE3':
        """Create random SE(3) transformation."""
        R = SO3.Random()
        t = np.random.random(3) * 10 - 5  # Random translation in [-5, 5]
        return cls.Rt(R, t)

    # Conversion methods
    def rpy(self) -> Tuple[float, float, float]:
        """Extract roll-pitch-yaw angles of rotation part."""
        return r2rpy(self.R)

    def eul(self, convention: str = 'ZYZ') -> Tuple[float, float, float]:
        """Extract Euler angles of rotation part."""
        return r2eul(self.R, convention)

    # Operations
    def inv(self) -> 'SE3':
        """Compute inverse transformation."""
        return SE3(homogeneous_inverse(self._matrix))

    def __mul__(self, other: Union['SE3', Vector3, np.ndarray]) -> Union['SE3', np.ndarray]:
        """
        Multiply with SE3 (composition) or transform points.

        Args:
            other: SE3 transformation or 3D point(s)

        Returns:
            SE3 for composition, ndarray for point transformation
        """
        if isinstance(other, SE3):
            # SE3 composition
            return SE3(self._matrix @ other._matrix)
        else:
            # Point transformation
            other = np.asarray(other)
            if other.shape == (3,):
                # Single point
                return transform_point(self._matrix, other)
            elif other.ndim == 2 and other.shape[1] == 3:
                # Multiple points
                return transform_points(self._matrix, other)
            else:
                raise ValueError("Can only transform 3D points or point arrays")

    def __rmul__(self, other):
        """Right multiplication (not supported for SE3)."""
        raise TypeError("Right multiplication not supported")

    def __pow__(self, n: int) -> 'SE3':
        """Power operation (repeated multiplication)."""
        if not isinstance(n, int):
            raise TypeError("Exponent must be integer")

        if n == 0:
            return SE3()  # Identity
        elif n > 0:
            result = SE3(self._matrix)
            for _ in range(n - 1):
                result = result * self
            return result
        else:
            return (self.inv() ** (-n))

    def translate(self, t: Vector3) -> 'SE3':
        """Apply additional translation."""
        return SE3.Trans(t) * self

    def rotate(self, R: Union[Matrix3x3, SO3]) -> 'SE3':
        """Apply additional rotation."""
        if isinstance(R, SO3):
            R = R.matrix
        return SE3(rotmat(R)) * self

    def distance(self, other: 'SE3') -> float:
        """Compute distance to another SE3 transformation."""
        if not isinstance(other, SE3):
            raise TypeError("Can only compute distance to another SE3")

        # Euclidean distance between translations
        dt = np.linalg.norm(self.t - other.t)

        # Angular distance between rotations
        R_diff = self.R.T @ other.R
        trace = np.trace(R_diff)
        dR = np.arccos(np.clip((trace - 1) / 2, -1, 1))

        return dt + dR  # Simple combination

    def __repr__(self) -> str:
        """String representation."""
        return f"SE3(\n{self._matrix})"

    def __str__(self) -> str:
        """Compact string representation."""
        t = self.t
        rpy = self.rpy()
        return (f"SE3: t=({t[0]:.3f}, {t[1]:.3f}, {t[2]:.3f}), "
                f"RPY=({rpy[0]:.3f}, {rpy[1]:.3f}, {rpy[2]:.3f})")


# Convenience functions
def SE3_identity() -> SE3:
    """Create identity SE(3) transformation."""
    return SE3()

def SO3_identity() -> SO3:
    """Create identity SO(3) rotation."""
    return SO3()
