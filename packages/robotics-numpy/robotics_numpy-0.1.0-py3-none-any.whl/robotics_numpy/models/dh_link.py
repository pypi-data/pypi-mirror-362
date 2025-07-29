"""
DH Link classes for robotics-numpy

This module provides DH (Denavit-Hartenberg) link representations for robot modeling.
Supports both revolute and prismatic joints with standard DH parameters.

The DH parameters are:
- a: link length (distance along x_{i-1} from z_{i-1} to z_i)
- alpha: link twist (angle about x_{i-1} from z_{i-1} to z_i)
- d: link offset (distance along z_i from x_{i-1} to x_i)
- theta: joint angle (angle about z_i from x_{i-1} to x_i)

For revolute joints: theta is the joint variable, d/a/alpha are constants
For prismatic joints: d is the joint variable, theta/a/alpha are constants
"""

import numpy as np
from typing import Optional, Union, List, Tuple
from ..transforms import SE3, rotmat, transl, rotz, rotx

# Type aliases
ArrayLike = Union[float, int, np.ndarray, List[float]]


class DHLink:
    """
    Base class for DH (Denavit-Hartenberg) link representation.

    This class represents a single link in a robot manipulator using
    standard DH parameters. It can represent both revolute and prismatic joints.

    Args:
        d: Link offset (distance along z_i from x_{i-1} to x_i)
        a: Link length (distance along x_{i-1} from z_{i-1} to z_i)
        alpha: Link twist (angle about x_{i-1} from z_{i-1} to z_i)
        theta: Joint angle (angle about z_i from x_{i-1} to x_i)
        joint_type: Type of joint ('R' for revolute, 'P' for prismatic)
        qlim: Joint limits [min, max] in radians (revolute) or meters (prismatic)
        m: Link mass (kg)
        r: Center of mass position [x, y, z] in link frame (m)
        I: Inertia tensor [Ixx, Iyy, Izz, Ixy, Iyz, Ixz] (kg⋅m²)
        Jm: Motor inertia (kg⋅m²)
        G: Gear ratio
        B: Viscous friction coefficient
        Tc: Coulomb friction coefficients [positive, negative]

    Examples:
        >>> # Revolute joint
        >>> link1 = DHLink(d=0.1, a=0.2, alpha=np.pi/2, theta=0, joint_type='R')
        >>>
        >>> # Prismatic joint
        >>> link2 = DHLink(d=0, a=0, alpha=0, theta=np.pi/2, joint_type='P')
        >>>
        >>> # With joint limits
        >>> link3 = DHLink(d=0.1, a=0, alpha=0, theta=0, joint_type='R',
        ...                 qlim=[-np.pi, np.pi])
    """

    def __init__(
        self,
        d: float = 0.0,
        a: float = 0.0,
        alpha: float = 0.0,
        theta: float = 0.0,
        joint_type: str = 'R',
        qlim: Optional[List[float]] = None,
        m: Optional[float] = None,
        r: Optional[List[float]] = None,
        I: Optional[List[float]] = None,
        Jm: Optional[float] = None,
        G: Optional[float] = None,
        B: Optional[float] = None,
        Tc: Optional[List[float]] = None,
    ):
        # DH parameters
        self.d = float(d)
        self.a = float(a)
        self.alpha = float(alpha)
        self.theta = float(theta)

        # Joint type validation
        if joint_type not in ['R', 'P', 'revolute', 'prismatic']:
            raise ValueError("joint_type must be 'R', 'P', 'revolute', or 'prismatic'")

        self.joint_type = joint_type.upper()[0]  # Normalize to 'R' or 'P'

        # Joint limits
        if qlim is not None:
            if len(qlim) != 2:
                raise ValueError("qlim must be a 2-element list [min, max]")
            if qlim[0] >= qlim[1]:
                raise ValueError("qlim[0] must be less than qlim[1]")
            self.qlim = [float(qlim[0]), float(qlim[1])]
        else:
            self.qlim = None

        # Dynamic parameters (optional)
        self.m = float(m) if m is not None else None

        if r is not None:
            if len(r) != 3:
                raise ValueError("r (center of mass) must be a 3-element list [x, y, z]")
            self.r = [float(x) for x in r]
        else:
            self.r = None

        if I is not None:
            if len(I) != 6:
                raise ValueError("I (inertia) must be a 6-element list [Ixx, Iyy, Izz, Ixy, Iyz, Ixz]")
            self.I = [float(x) for x in I]
        else:
            self.I = None

        self.Jm = float(Jm) if Jm is not None else None
        self.G = float(G) if G is not None else None
        self.B = float(B) if B is not None else None

        if Tc is not None:
            if len(Tc) != 2:
                raise ValueError("Tc (Coulomb friction) must be a 2-element list [positive, negative]")
            self.Tc = [float(Tc[0]), float(Tc[1])]
        else:
            self.Tc = None

    def is_revolute(self) -> bool:
        """Check if this is a revolute joint."""
        return self.joint_type == 'R'

    def is_prismatic(self) -> bool:
        """Check if this is a prismatic joint."""
        return self.joint_type == 'P'

    def A(self, q: float) -> SE3:
        """
        Compute link transformation matrix for given joint value.

        Computes the homogeneous transformation matrix from link frame {i-1}
        to link frame {i} using standard DH convention.

        The transformation is: T = Tz(d) * Rz(theta) * Tx(a) * Rx(alpha)

        Args:
            q: Joint value (angle in radians for revolute, distance in meters for prismatic)

        Returns:
            SE3 transformation matrix from frame {i-1} to frame {i}

        Examples:
            >>> link = DHLink(d=0.1, a=0.2, alpha=np.pi/2, theta=0, joint_type='R')
            >>> T = link.A(np.pi/4)  # 45 degree rotation
            >>> print(T)
        """
        q = float(q)

        # Determine actual DH parameters based on joint type
        if self.is_revolute():
            d = self.d
            theta = self.theta + q  # Joint variable is added to fixed offset
            a = self.a
            alpha = self.alpha
        else:  # Prismatic
            d = self.d + q  # Joint variable is added to fixed offset
            theta = self.theta
            a = self.a
            alpha = self.alpha

        # Check joint limits if specified
        if self.qlim is not None:
            if not (self.qlim[0] <= q <= self.qlim[1]):
                print(f"Warning: Joint value {q:.3f} outside limits {self.qlim}")

        # Build transformation using DH convention: Tz(d) * Rz(theta) * Tx(a) * Rx(alpha)
        T = SE3.Trans(0, 0, d) * SE3.Rz(theta) * SE3.Trans(a, 0, 0) * SE3.Rx(alpha)

        return T

    def copy(self) -> 'DHLink':
        """Create a copy of this DH link."""
        return DHLink(
            d=self.d,
            a=self.a,
            alpha=self.alpha,
            theta=self.theta,
            joint_type=self.joint_type,
            qlim=self.qlim.copy() if self.qlim else None,
            m=self.m,
            r=self.r.copy() if self.r else None,
            I=self.I.copy() if self.I else None,
            Jm=self.Jm,
            G=self.G,
            B=self.B,
            Tc=self.Tc.copy() if self.Tc else None,
        )

    def __str__(self) -> str:
        """String representation of DH link."""
        joint_name = "Revolute" if self.is_revolute() else "Prismatic"

        # Format DH parameters
        params = f"d={self.d:.3f}, a={self.a:.3f}, α={self.alpha:.3f}, θ={self.theta:.3f}"

        # Add joint limits if present
        limits = ""
        if self.qlim:
            if self.is_revolute():
                limits = f", qlim=[{np.degrees(self.qlim[0]):.1f}°, {np.degrees(self.qlim[1]):.1f}°]"
            else:
                limits = f", qlim=[{self.qlim[0]:.3f}, {self.qlim[1]:.3f}]m"

        # Add mass if present
        mass = f", m={self.m:.2f}kg" if self.m is not None else ""

        return f"{joint_name}DH({params}{limits}{mass})"

    def __repr__(self) -> str:
        """Detailed representation of DH link."""
        return self.__str__()


class RevoluteDH(DHLink):
    """
    Revolute DH link - joint variable is theta.

    Convenience class for creating revolute joints where theta is the joint variable.

    Args:
        d: Link offset (constant)
        a: Link length (constant)
        alpha: Link twist (constant)
        theta: Joint angle offset (added to joint variable)
        qlim: Joint angle limits [min, max] in radians
        **kwargs: Additional parameters passed to DHLink

    Examples:
        >>> # Simple revolute joint
        >>> link = RevoluteDH(d=0.1, a=0.2, alpha=np.pi/2)
        >>>
        >>> # With joint limits
        >>> link = RevoluteDH(d=0.1, a=0, alpha=0, qlim=[-np.pi, np.pi])
    """

    def __init__(
        self,
        d: float = 0.0,
        a: float = 0.0,
        alpha: float = 0.0,
        theta: float = 0.0,
        qlim: Optional[List[float]] = None,
        **kwargs
    ):
        super().__init__(
            d=d,
            a=a,
            alpha=alpha,
            theta=theta,
            joint_type='R',
            qlim=qlim,
            **kwargs
        )


class PrismaticDH(DHLink):
    """
    Prismatic DH link - joint variable is d.

    Convenience class for creating prismatic joints where d is the joint variable.

    Args:
        theta: Joint angle (constant)
        a: Link length (constant)
        alpha: Link twist (constant)
        d: Link offset (added to joint variable)
        qlim: Joint displacement limits [min, max] in meters
        **kwargs: Additional parameters passed to DHLink

    Examples:
        >>> # Simple prismatic joint
        >>> link = PrismaticDH(theta=0, a=0, alpha=0)
        >>>
        >>> # With joint limits
        >>> link = PrismaticDH(theta=np.pi/2, a=0, alpha=0, qlim=[0, 0.5])
    """

    def __init__(
        self,
        theta: float = 0.0,
        a: float = 0.0,
        alpha: float = 0.0,
        d: float = 0.0,
        qlim: Optional[List[float]] = None,
        **kwargs
    ):
        super().__init__(
            d=d,
            a=a,
            alpha=alpha,
            theta=theta,
            joint_type='P',
            qlim=qlim,
            **kwargs
        )


def dh_check_parameters(links: List[DHLink]) -> bool:
    """
    Validate DH parameters for a chain of links.

    Args:
        links: List of DH links

    Returns:
        True if parameters are valid

    Raises:
        ValueError: If parameters are invalid
    """
    if not links:
        raise ValueError("Empty link list")

    if not all(isinstance(link, DHLink) for link in links):
        raise ValueError("All elements must be DHLink instances")

    # Check for reasonable parameter ranges
    for i, link in enumerate(links):
        # Check alpha is in reasonable range
        if abs(link.alpha) > 2 * np.pi:
            raise ValueError(f"Link {i}: alpha ({link.alpha}) should be in [-2π, 2π]")

        # Check theta is in reasonable range (for fixed part)
        if abs(link.theta) > 2 * np.pi:
            raise ValueError(f"Link {i}: theta offset ({link.theta}) should be in [-2π, 2π]")

        # Check joint limits are reasonable
        if link.qlim is not None:
            if link.is_revolute():
                if abs(link.qlim[0]) > 4 * np.pi or abs(link.qlim[1]) > 4 * np.pi:
                    print(f"Warning: Link {i} has very large joint limits (>720°)")
            else:  # Prismatic
                if abs(link.qlim[0]) > 10 or abs(link.qlim[1]) > 10:
                    print(f"Warning: Link {i} has very large displacement limits (>10m)")

    return True


# Utility functions for common DH parameter patterns
def create_6dof_revolute_arm(
    lengths: Optional[List[float]] = None,
    offsets: Optional[List[float]] = None
) -> List[DHLink]:
    """
    Create a standard 6-DOF revolute arm with common DH parameters.

    Args:
        lengths: Link lengths [a1, a2, a3, a4, a5, a6] (default: [0, 0.3, 0.3, 0, 0, 0])
        offsets: Link offsets [d1, d2, d3, d4, d5, d6] (default: [0.3, 0, 0, 0.3, 0, 0.1])

    Returns:
        List of 6 DH links representing a typical 6-DOF arm

    Examples:
        >>> links = create_6dof_revolute_arm()
        >>> robot = DHRobot(links)
    """
    if lengths is None:
        lengths = [0, 0.3, 0.3, 0, 0, 0]  # Typical arm lengths
    if offsets is None:
        offsets = [0.3, 0, 0, 0.3, 0, 0.1]  # Typical arm offsets

    if len(lengths) != 6 or len(offsets) != 6:
        raise ValueError("lengths and offsets must have 6 elements each")

    # Standard 6-DOF arm DH parameters
    alphas = [np.pi/2, 0, np.pi/2, -np.pi/2, np.pi/2, 0]
    joint_limits = [
        [-np.pi, np.pi],      # Base rotation
        [-np.pi/2, np.pi/2],  # Shoulder
        [-np.pi, np.pi],      # Elbow
        [-np.pi, np.pi],      # Wrist roll
        [-np.pi/2, np.pi/2],  # Wrist pitch
        [-np.pi, np.pi],      # Wrist yaw
    ]

    links = []
    for i in range(6):
        link = RevoluteDH(
            d=offsets[i],
            a=lengths[i],
            alpha=alphas[i],
            theta=0,
            qlim=joint_limits[i]
        )
        links.append(link)

    return links
