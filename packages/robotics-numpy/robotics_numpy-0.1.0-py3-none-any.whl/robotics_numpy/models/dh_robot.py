"""
DHRobot class for robotics-numpy

This module provides the DHRobot class for robot manipulator modeling using
Denavit-Hartenberg parameters. Includes forward kinematics computation and
robot configuration management.
"""

import numpy as np
from typing import List, Optional, Union, Dict, Any, Tuple
from .dh_link import DHLink, dh_check_parameters
from ..transforms import SE3
from ..kinematics.jacobian import (
    jacob0 as compute_jacob0,
    manipulability as compute_manipulability,
)
# from ..kinematics.forward import fkine_dh  # Moved to avoid circular import

# Type aliases
ArrayLike = Union[float, int, np.ndarray, List[float]]
JointConfig = Union[List[float], np.ndarray]


class DHRobot:
    """
    Robot manipulator model using Denavit-Hartenberg parameters.

    This class represents a serial-link robot manipulator using DH parameters.
    It provides forward kinematics computation and robot configuration management.

    Args:
        links: List of DH links defining the robot
        name: Robot name/model
        manufacturer: Robot manufacturer
        base: Base transformation (default: identity)
        tool: Tool transformation (default: identity)
        gravity: Gravity vector [x, y, z] in m/s² (default: [0, 0, -9.81])
        keywords: Keywords describing robot features

    Examples:
        >>> # Create a simple 2-DOF arm
        >>> links = [
        ...     RevoluteDH(d=0.1, a=0.2, alpha=0),
        ...     RevoluteDH(d=0, a=0.3, alpha=0)
        ... ]
        >>> robot = DHRobot(links, name="2DOF Arm")
        >>>
        >>> # Forward kinematics
        >>> q = [0, np.pi/4]
        >>> T = robot.fkine(q)
        >>> print(T)
    """

    def __init__(
        self,
        links: List[DHLink],
        name: str = "DHRobot",
        manufacturer: str = "",
        base: Optional[SE3] = None,
        tool: Optional[SE3] = None,
        gravity: Optional[List[float]] = None,
        keywords: Tuple[str, ...] = (),
    ):
        # Validate links
        if not isinstance(links, list):
            raise TypeError("links must be a list of DHLink objects")

        if not links:
            raise ValueError("Robot must have at least one link")

        dh_check_parameters(links)

        self._links = links.copy()
        self.name = str(name)
        self.manufacturer = str(manufacturer)
        self.keywords = tuple(keywords)

        # Base and tool transformations
        self.base = base if base is not None else SE3()
        self.tool = tool if tool is not None else SE3()

        # Gravity vector
        if gravity is None:
            self.gravity = [0.0, 0.0, -9.81]
        else:
            if len(gravity) != 3:
                raise ValueError("gravity must be a 3-element vector")
            self.gravity = [float(g) for g in gravity]

        # Joint configurations storage
        self._configurations: Dict[str, np.ndarray] = {}

        # Cache for performance
        self._n = len(self._links)
        self._joint_types = [link.joint_type for link in self._links]

    @property
    def n(self) -> int:
        """Number of joints."""
        return self._n

    @property
    def links(self) -> List[DHLink]:
        """List of DH links (read-only)."""
        return self._links.copy()

    @property
    def joint_types(self) -> List[str]:
        """Joint types as list of 'R' or 'P'."""
        return self._joint_types.copy()

    @property
    def qlim(self) -> np.ndarray:
        """
        Joint limits as 2xn array.

        Returns:
            Joint limits where each column is [min, max] for one joint
        """
        limits = np.zeros((2, self.n))
        for i, link in enumerate(self._links):
            print(f"Link {i}: qlim={link.qlim}, is_revolute={link.is_revolute()}")
            if link.qlim is not None:
                print(f"Assigning qlim for Link {i}: {link.qlim}")
                limits[:, i] = link.qlim
            else:
                # Default limits
                if link.is_revolute():
                    print(f"Default revolute qlim for Link {i}: [-np.pi, np.pi]")
                    limits[:, i] = [-np.pi, np.pi]
                else:
                    limits[:, i] = [-1.0, 1.0]
                    print(f"Default prismatic qlim for Link {i}: [-1.0, 1.0]")
        return limits

    def islimit(self, q: JointConfig) -> np.ndarray:
        """
        Check if joint configuration is within limits.

        Args:
            q: Joint configuration

        Returns:
            Boolean array indicating which joints are at limits
        """
        q = self._validate_q(q)
        limits = self.qlim

        # Check both upper and lower limits
        at_lower = np.abs(q - limits[:, 0]) < 1e-6
        at_upper = np.abs(q - limits[:, 1]) < 1e-6

        return at_lower | at_upper

    def isspherical(self) -> bool:
        """Check if robot has spherical wrist (last 3 joints intersect)."""
        if self.n < 3:
            return False

        # Check if last 3 joint axes intersect at a point
        # This is a simplified check - assumes standard spherical wrist geometry
        last_3_links = self._links[-3:]

        # Spherical wrist typically has a=0 for last 3 links and specific alpha values
        has_zero_a = all(abs(link.a) < 1e-6 for link in last_3_links)
        has_correct_alphas = (
            abs(abs(last_3_links[0].alpha) - np.pi / 2) < 1e-3
            and abs(abs(last_3_links[1].alpha) - np.pi / 2) < 1e-3
            and abs(last_3_links[2].alpha) < 1e-3
        )

        return has_zero_a and has_correct_alphas

    def fkine(self, q: JointConfig, end: Optional[int] = None, start: int = 0) -> SE3:
        """
        Forward kinematics using DH parameters.

        Computes the forward kinematics from the base frame to the end-effector
        frame (or specified intermediate frame).

        Args:
            q: Joint configuration (n joint values)
            end: End link index (default: end-effector)
            start: Start link index (default: 0)

        Returns:
            SE3 transformation from base to end-effector (or specified frame)

        Examples:
            >>> robot = DHRobot(links)
            >>> T = robot.fkine([0, 0, 0, 0, 0, 0])  # All joints at zero
            >>> T = robot.fkine([0, 0, 0], end=2)    # First 3 links only
        """
        q = self._validate_q(q)

        if end is None:
            end = self.n - 1

        if not (0 <= start <= end < self.n):
            raise ValueError(
                f"Invalid link range: start={start}, end={end}, n={self.n}"
            )

        # If only partial chain requested, adjust q
        if start > 0 or end < self.n - 1:
            q = q[start : end + 1]

        # Compute forward kinematics using DH algorithm
        T = self._fkine_dh(self._links[start : end + 1], q)

        # Apply base and tool transformations if computing full chain
        if start == 0:
            T = self.base * T
        if end == self.n - 1:
            T = T * self.tool

        return T

    def fkine_all(self, q: JointConfig) -> List[SE3]:
        """
        Forward kinematics for all intermediate frames.

        Computes transformations from base to each link frame.

        Args:
            q: Joint configuration

        Returns:
            List of SE3 transformations, one for each link frame

        Examples:
            >>> robot = DHRobot(links)
            >>> transforms = robot.fkine_all([0, 0, 0, 0, 0, 0])
            >>> print(f"End-effector pose: {transforms[-1]}")
        """
        q = self._validate_q(q)

        transforms = []
        T = self.base

        for i in range(self.n):
            T = T * self._links[i].A(q[i])
            transforms.append(T)

        # Apply tool transformation to last frame
        transforms[-1] = transforms[-1] * self.tool

        return transforms

    def _fkine_dh(self, links, q):
        """Internal forward kinematics computation."""
        return _fkine_dh_single(links, q)

    def jacob0(
        self,
        q: JointConfig = None,
        T=None,
        half: Optional[str] = None,
        start: int = 0,
        end: Optional[int] = None,
    ) -> np.ndarray:
        """
        Manipulator Jacobian in world frame

        Args:
            q: Joint coordinate vector
            T: Forward kinematics if known, SE3 matrix
            half: Return half Jacobian: 'trans' or 'rot'
            start: Start link index (default: 0)
            end: End link index (default: end-effector)

        Returns:
            The manipulator Jacobian in the world frame (6xn)

        Notes:
            - End-effector spatial velocity v = (vx, vy, vz, wx, wy, wz)^T
              is related to joint velocity by v = J0(q) * dq
            - This is the geometric Jacobian as described in texts by
              Corke, Spong et al., Siciliano et al.
        """
        if q is None:
            raise ValueError("Joint configuration q must be provided")

        q = self._validate_q(q)

        # Call the implementation from the jacobian module
        return compute_jacob0(self, q, T, half, start, end)

    def manipulability(
        self,
        q: Optional[JointConfig] = None,
        J: Optional[np.ndarray] = None,
        end: Optional[int] = None,
        start: int = 0,
        method: str = "yoshikawa",
        axes: Union[str, List[bool]] = "all",
        **kwargs,
    ) -> float:
        """
        Manipulability measure

        Computes the manipulability index for the robot at the joint configuration q.
        It indicates dexterity, that is, how well conditioned the robot is for motion
        with respect to the 6 degrees of Cartesian motion. The value is zero if the
        robot is at a singularity.

        Args:
            q: Joint coordinates (one of J or q required)
            J: Jacobian in base frame if already computed (one of J or q required)
            end: End link index (default: end-effector)
            start: Start link index (default: 0)
            method: Method to use ('yoshikawa', 'asada', 'minsingular', 'invcondition')
            axes: Task space axes to consider: 'all', 'trans', 'rot', or a boolean list

        Returns:
            Manipulability index

        Notes:
            Supported measures:
            - 'yoshikawa': Volume of the velocity ellipsoid, distance from singularity
            - 'invcondition': Inverse condition number of Jacobian, isotropy of velocity ellipsoid
            - 'minsingular': Minimum singular value of the Jacobian, distance from singularity
            - 'asada': Isotropy of the task-space acceleration ellipsoid (requires inertial parameters)

            The 'all' axes option includes rotational and translational dexterity, but this
            involves adding different units. It can be more useful to look at the translational
            and rotational manipulability separately.
        """
        if q is not None:
            q = self._validate_q(q)

        # Call the implementation from the jacobian module
        return compute_manipulability(self, q, J, end, start, method, axes, **kwargs)

    def addconfiguration(self, name: str, q: JointConfig) -> None:
        """
        Add a named joint configuration.

        Args:
            name: Configuration name
            q: Joint configuration

        Examples:
            >>> robot.addconfiguration("home", [0, 0, 0, 0, 0, 0])
            >>> robot.addconfiguration("ready", robot.qr)
        """
        q = self._validate_q(q)
        self._configurations[name] = q.copy()

        # Also set as attribute for convenience
        setattr(self, name, q.copy())

    def configurations(self) -> List[str]:
        """List all configuration names."""
        return list(self._configurations.keys())

    def getconfig(self, name: str) -> np.ndarray:
        """
        Get a named configuration.

        Args:
            name: Configuration name

        Returns:
            Joint configuration array

        Raises:
            KeyError: If configuration doesn't exist
        """
        if name not in self._configurations:
            raise KeyError(f"Configuration '{name}' not found")
        return self._configurations[name].copy()

    def teach(self, q: Optional[JointConfig] = None) -> None:
        """
        Simple teach interface - print current pose.

        Args:
            q: Joint configuration (default: all zeros)
        """
        if q is None:
            q = np.zeros(self.n)
        else:
            q = self._validate_q(q)

        T = self.fkine(q)
        print(f"Joint configuration: {q}")
        print(f"End-effector pose:\n{T}")
        print(f"Position: {T.t}")
        print(f"RPY angles: {np.degrees(T.rpy())} degrees")

    def _validate_q(self, q: JointConfig) -> np.ndarray:
        """Validate and convert joint configuration to numpy array."""
        q = np.asarray(q, dtype=float)

        if q.shape == ():
            q = np.array([q])  # Handle scalar input

        if q.shape != (self.n,):
            raise ValueError(f"q must have {self.n} elements, got {q.shape}")

        return q

    def __len__(self) -> int:
        """Number of joints."""
        return self.n

    def __getitem__(self, index: int) -> DHLink:
        """Get link by index."""
        return self._links[index]

    def __str__(self) -> str:
        """String representation of robot."""
        joint_str = "".join(link.joint_type for link in self._links)

        header = f"{self.name}"
        if self.manufacturer:
            header += f" (by {self.manufacturer})"

        header += f", {self.n} joints ({joint_str})"

        if self.keywords:
            header += f", {', '.join(self.keywords)}"

        # Create table of DH parameters
        lines = [header, ""]

        # Table header
        lines.append(
            "┌─────┬──────────┬─────────┬─────────┬─────────┬─────────────────┐"
        )
        lines.append(
            "│link │   link   │ joint   │    θ    │    d    │        a        │"
        )
        lines.append(
            "├─────┼──────────┼─────────┼─────────┼─────────┼─────────────────┤"
        )

        # Table rows
        for i, link in enumerate(self._links):
            joint_type = "R" if link.is_revolute() else "P"

            # Format values
            theta_str = f"{link.theta:7.3f}" if not link.is_revolute() else f"q{i}"
            d_str = f"{link.d:7.3f}" if not link.is_prismatic() else f"q{i}"
            a_str = f"{link.a:7.3f}"
            alpha_str = f"{link.alpha:7.3f}"

            lines.append(
                f"│{i:4d} │ link{i:<4d} │   {joint_type:>1s}     │{theta_str:>8s} │"
                f"{d_str:>8s} │{a_str:>8s} α={alpha_str:>6s}│"
            )

        lines.append(
            "└─────┴──────────┴─────────┴─────────┴─────────┴─────────────────┘"
        )

        # Add configurations if any
        if self._configurations:
            lines.append("")
            lines.append("Named configurations:")
            for name, config in self._configurations.items():
                config_str = ", ".join(f"{val:6.2f}" for val in config)
                lines.append(f"  {name}: [{config_str}]")

        return "\n".join(lines)

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"DHRobot(name='{self.name}', n={self.n}, joints='{self.joint_types}')"


# Utility functions for robot creation
def create_simple_arm(n_joints: int = 6, link_length: float = 0.3) -> DHRobot:
    """
    Create a simple n-DOF revolute arm for testing.

    Args:
        n_joints: Number of joints (default: 6)
        link_length: Length of each link (default: 0.3m)

    Returns:
        DHRobot with simple DH parameters
    """
    from .dh_link import RevoluteDH

    links = []
    for i in range(n_joints):
        if i == 0:
            # Base joint
            link = RevoluteDH(d=0.3, a=0, alpha=np.pi / 2, qlim=[-np.pi, np.pi])
        elif i == n_joints - 1:
            # Last joint
            link = RevoluteDH(d=0, a=0, alpha=0, qlim=[-np.pi, np.pi])
        else:
            # Intermediate joints
            alpha = np.pi / 2 if i % 2 == 1 else 0
            link = RevoluteDH(d=0, a=link_length, alpha=alpha, qlim=[-np.pi, np.pi])

        links.append(link)

    robot = DHRobot(links, name=f"Simple {n_joints}DOF Arm")

    # Add some standard configurations
    robot.addconfiguration("qz", np.zeros(n_joints))
    robot.addconfiguration("qr", np.zeros(n_joints))  # Ready position

    return robot


def create_planar_arm(
    n_joints: int = 3, link_lengths: Optional[List[float]] = None
) -> DHRobot:
    """
    Create a planar n-DOF arm (all joints parallel, in same plane).

    Args:
        n_joints: Number of joints (default: 3)
        link_lengths: Length of each link (default: equal lengths)

    Returns:
        DHRobot representing planar arm
    """
    from .dh_link import RevoluteDH

    if link_lengths is None:
        link_lengths = [0.3] * n_joints
    elif len(link_lengths) != n_joints:
        raise ValueError(f"link_lengths must have {n_joints} elements")

    links = []
    for i in range(n_joints):
        link = RevoluteDH(
            d=0,
            a=link_lengths[i],
            alpha=0,  # All joints parallel
            theta=0,
            qlim=[-np.pi, np.pi],
        )
        links.append(link)

    robot = DHRobot(links, name=f"Planar {n_joints}DOF Arm")

    # Add configurations
    robot.addconfiguration("qz", np.zeros(n_joints))
    robot.addconfiguration("qstraight", np.zeros(n_joints))
    if n_joints >= 3:
        robot.addconfiguration(
            "qfold", np.array([0, np.pi / 2, -np.pi / 2] + [0] * (n_joints - 3))
        )
    else:
        robot.addconfiguration("qfold", np.zeros(n_joints))

    return robot


def _fkine_dh_single(links, q):
    """
    Internal forward kinematics using DH parameters.

    This avoids circular imports by keeping FK computation within the robot model.
    """
    from ..transforms import SE3

    q = np.asarray(q, dtype=float)

    if len(q) != len(links):
        raise ValueError(
            f"Joint configuration length ({len(q)}) must match number of links ({len(links)})"
        )

    # Start with identity transformation
    T = SE3()

    # Multiply transformation matrices for each link
    for i, (link, qi) in enumerate(zip(links, q)):
        try:
            T_link = link.A(qi)
            T = T * T_link
        except Exception as e:
            raise RuntimeError(f"Error computing transformation for link {i}: {e}")

    return T
