"""
Generic robot model for robotics-numpy

This module implements a fully generic robotic arm class using Denavit-Hartenberg
parameters. It allows creating robots with arbitrary number of joints and fully
configurable DH parameters.

The Generic class is useful for:
- Educational purposes and experimentation
- Rapid prototyping of robot designs
- Testing kinematics algorithms
- Creating custom robot configurations
"""

import numpy as np
from typing import Optional, List, Union
from .dh_robot import DHRobot
from .dh_link import RevoluteDH, PrismaticDH

# Constants
pi = np.pi
deg = pi / 180


class Generic(DHRobot):
    """
    A fully generic robotic arm class using Denavit-Hartenberg parameters.

    The class represents a robot arm with arbitrary number of joints and fully configurable
    DH parameters. It inherits from DHRobot and uses standard DH parameters to define the kinematics.

    The robot has the following key features:
    - Configurable number of DOFs (degrees of freedom)
    - Fully customizable DH parameters: a, d, alpha, offset
    - Support for both revolute and prismatic joints
    - Ready-poses defined for:
        - qr: "ready" position (all joints at offset values)
        - qz: "zero" position (all joints at 0)
    - Optional 3D visualization with Plotly

    Examples:
        >>> # Create a 4-DOF robot
        >>> robot = Generic(
        ...     dofs=4,
        ...     a=[0, -0.5, -0.5, -0.5],
        ...     d=[0.5, 0, 0, 0],
        ...     alpha=[pi/2, 0, 0, 0],
        ...     name="Custom4DOF"
        ... )
        >>>
        >>> # Forward kinematics
        >>> T = robot.fkine(robot.qz)
        >>> print(f"End-effector pose: {T}")
        >>>
        >>> # Visualization (requires plotly)
        >>> robot.plotly(robot.qz)
    """

    def __init__(
        self,
        dofs: int,
        a: Optional[List[float]] = None,
        d: Optional[List[float]] = None,
        alpha: Optional[List[float]] = None,
        offset: Optional[List[float]] = None,
        qlim: Optional[List[List[float]]] = None,
        joint_types: Optional[List[str]] = None,
        name: str = "GenericDH",
        **kwargs,
    ):
        """
        Initialize the generic robot with configurable DH parameters.

        Args:
            dofs: Number of degrees of freedom
            a: Link lengths along common normal [dofs elements] (default: 0.1m each)
            d: Link offsets along previous z to common normal [dofs elements] (default: 0.1m each)
            alpha: Link twist angles in radians [dofs elements] (default: 0 each)
            offset: Joint angle offsets in radians [dofs elements] (default: 0 each)
            qlim: Joint limits as [[min, max], ...] [dofs pairs] (default: ±180° each)
            joint_types: Joint types 'R' or 'P' [dofs elements] (default: all 'R')
            name: Name of the robot
            **kwargs: Additional arguments passed to DHRobot

        Raises:
            ValueError: If parameter dimensions don't match dofs
        """
        if not isinstance(dofs, int) or dofs < 1:
            raise ValueError("dofs must be a positive integer")

        self.dofs = dofs

        # Set default values if parameters are not provided
        if a is None:
            a = [0.1] * dofs  # Default link length of 0.1m
        if d is None:
            d = [0.1] * dofs  # Default link offset of 0.1m
        if alpha is None:
            alpha = [0.0] * dofs  # Default twist angle of 0
        if offset is None:
            offset = [0.0] * dofs  # Default joint offset of 0
        if qlim is None:
            qlim = [[-180 * deg, 180 * deg]] * dofs  # Default ±180 degrees
        if joint_types is None:
            joint_types = ["R"] * dofs  # Default to all revolute joints

        # Validate input dimensions
        if len(a) != dofs:
            raise ValueError(f"Length of 'a' ({len(a)}) must equal dofs ({dofs})")
        if len(d) != dofs:
            raise ValueError(f"Length of 'd' ({len(d)}) must equal dofs ({dofs})")
        if len(alpha) != dofs:
            raise ValueError(
                f"Length of 'alpha' ({len(alpha)}) must equal dofs ({dofs})"
            )
        if len(offset) != dofs:
            raise ValueError(
                f"Length of 'offset' ({len(offset)}) must equal dofs ({dofs})"
            )
        if len(qlim) != dofs:
            raise ValueError(f"Length of 'qlim' ({len(qlim)}) must equal dofs ({dofs})")
        if len(joint_types) != dofs:
            raise ValueError(
                f"Length of 'joint_types' ({len(joint_types)}) must equal dofs ({dofs})"
            )

        # Validate joint types
        for i, jtype in enumerate(joint_types):
            if jtype not in ["R", "P"]:
                raise ValueError(f"joint_types[{i}] must be 'R' or 'P', got '{jtype}'")

        # Validate qlim format
        for i, limit in enumerate(qlim):
            if len(limit) != 2:
                raise ValueError(f"qlim[{i}] must have exactly 2 elements [min, max]")
            if limit[0] >= limit[1]:
                raise ValueError(
                    f"qlim[{i}] min ({limit[0]}) must be less than max ({limit[1]})"
                )

        # Store parameters
        self._a = list(a)
        self._d = list(d)
        self._alpha = list(alpha)
        self._offset = list(offset)
        self._qlim = [list(limit) for limit in qlim]
        self._joint_types = list(joint_types)

        # Default dynamic properties (can be customized later)
        r = [
            [0.0, 0.0, 0.0] for _ in range(dofs)
        ]  # Position of COM with respect to link frame
        I = [
            [0.0] * 6 for _ in range(dofs)
        ]  # Inertia tensor [Ixx, Iyy, Izz, Ixy, Iyz, Ixz]
        m = [0.0] * dofs  # mass of link
        Jm = [0.0] * dofs  # actuator inertia
        G = [1.0] * dofs  # gear ratio
        B = [0.0] * dofs  # actuator viscous friction coefficient
        Tc = [
            [0.0, 0.0] for _ in range(dofs)
        ]  # Coulomb friction coefficient for direction [-,+]

        # Create links based on joint types
        links = []
        for i in range(dofs):
            if joint_types[i] == "R":
                # Revolute joint
                link = RevoluteDH(
                    d=d[i],
                    a=a[i],
                    alpha=alpha[i],
                    theta=offset[i],  # theta is the offset for revolute joints
                    r=r[i],
                    I=I[i],
                    m=m[i],
                    Jm=Jm[i],
                    G=G[i],
                    B=B[i],
                    Tc=Tc[i],
                    qlim=qlim[i],
                )
            else:
                # Prismatic joint
                link = PrismaticDH(
                    theta=offset[i],  # For prismatic, offset is the fixed angle
                    a=a[i],
                    alpha=alpha[i],
                    d=0.0,  # d is variable for prismatic joints
                    r=r[i],
                    I=I[i],
                    m=m[i],
                    Jm=Jm[i],
                    G=G[i],
                    B=B[i],
                    Tc=Tc[i],
                    qlim=qlim[i],
                )
            links.append(link)

        # Initialize parent class
        super().__init__(
            links,
            name=name,
            manufacturer="generic",
            keywords=("configurable", "educational", "generic"),
            **kwargs,
        )

        # Ready pose: joint angles at offset values for revolute, 0 for prismatic
        self.qr = np.array(
            [offset[i] if joint_types[i] == "R" else 0.0 for i in range(dofs)]
        )

        # Zero pose: all joint values at 0
        self.qz = np.zeros(dofs)

        # Add configurations
        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

    @property
    def dh_parameters(self) -> dict:
        """Return DH parameters as a dictionary."""
        return {
            "a": self._a.copy(),
            "d": self._d.copy(),
            "alpha": self._alpha.copy(),
            "offset": self._offset.copy(),
            "qlim": [limit.copy() for limit in self._qlim],
            "joint_types": self._joint_types.copy(),
        }

    def set_dynamic_properties(
        self,
        m: Optional[List[float]] = None,
        r: Optional[List[List[float]]] = None,
        I: Optional[List[List[float]]] = None,
        Jm: Optional[List[float]] = None,
        G: Optional[List[float]] = None,
        B: Optional[List[float]] = None,
        Tc: Optional[List[List[float]]] = None,
    ) -> None:
        """
        Set dynamic properties for the robot links.

        Args:
            m: Mass of each link [dofs elements]
            r: Position of COM with respect to link frame [dofs x 3]
            I: Inertia tensor of each link [dofs x 6] as [Ixx, Iyy, Izz, Ixy, Iyz, Ixz]
            Jm: Actuator inertia [dofs elements]
            G: Gear ratio [dofs elements]
            B: Viscous friction coefficient [dofs elements]
            Tc: Coulomb friction coefficient [dofs x 2] as [negative, positive]

        Raises:
            ValueError: If parameter dimensions don't match dofs
        """

        def _validate_and_set(param, param_name, expected_shape, attr_name):
            if param is not None:
                if isinstance(expected_shape, int):
                    if len(param) != expected_shape:
                        raise ValueError(
                            f"{param_name} must have length {expected_shape}"
                        )
                    for i, link in enumerate(self.links):
                        setattr(link, attr_name, param[i])
                else:
                    if len(param) != expected_shape[0]:
                        raise ValueError(
                            f"{param_name} must have {expected_shape[0]} elements"
                        )
                    for i, p in enumerate(param):
                        if len(p) != expected_shape[1]:
                            raise ValueError(
                                f"{param_name}[{i}] must have {expected_shape[1]} elements"
                            )
                        setattr(self.links[i], attr_name, list(p))

        _validate_and_set(m, "m", self.dofs, "m")
        _validate_and_set(r, "r", (self.dofs, 3), "r")
        _validate_and_set(I, "I", (self.dofs, 6), "I")
        _validate_and_set(Jm, "Jm", self.dofs, "Jm")
        _validate_and_set(G, "G", self.dofs, "G")
        _validate_and_set(B, "B", self.dofs, "B")
        _validate_and_set(Tc, "Tc", (self.dofs, 2), "Tc")

    def workspace_radius(self) -> float:
        """
        Estimate maximum workspace radius.

        Returns:
            Maximum reach from base in meters
        """
        # Simple estimate: sum of all link lengths and max extensions
        max_reach = 0.0
        for i, link in enumerate(self.links):
            max_reach += abs(self._a[i])  # Link length
            if link.is_prismatic():
                # Add maximum prismatic extension
                max_reach += max(abs(self._qlim[i][0]), abs(self._qlim[i][1]))
            else:
                # Add link offset for revolute joints
                max_reach += abs(self._d[i])
        return max_reach

    def summary(self) -> str:
        """
        Generate a summary string of the robot configuration.

        Returns:
            Multi-line string describing the robot
        """
        lines = [
            f"Generic Robot: {self.name}",
            f"DOFs: {self.dofs}",
            f"Joint types: {' '.join(self._joint_types)}",
            f"Max reach: {self.workspace_radius():.3f} m",
            "",
            "DH Parameters:",
            "Link |   a    |   d    | alpha  | offset | type |    qlim    ",
            "-----+--------+--------+--------+--------+------+------------",
        ]

        for i in range(self.dofs):
            alpha_deg = self._alpha[i] * 180 / pi
            offset_deg = (
                self._offset[i] * 180 / pi
                if self._joint_types[i] == "R"
                else self._offset[i]
            )
            offset_unit = "°" if self._joint_types[i] == "R" else "m"

            qlim_min = (
                self._qlim[i][0] * 180 / pi
                if self._joint_types[i] == "R"
                else self._qlim[i][0]
            )
            qlim_max = (
                self._qlim[i][1] * 180 / pi
                if self._joint_types[i] == "R"
                else self._qlim[i][1]
            )
            qlim_unit = "°" if self._joint_types[i] == "R" else "m"

            lines.append(
                f" {i:2d}  | {self._a[i]:6.3f} | {self._d[i]:6.3f} | "
                f"{alpha_deg:6.1f} | {offset_deg:6.1f}{offset_unit} | "
                f"  {self._joint_types[i]}   | "
                f"[{qlim_min:5.1f},{qlim_max:5.1f}]{qlim_unit}"
            )

        return "\n".join(lines)

    def demo(self) -> None:
        """
        Demonstrate Generic robot capabilities.
        """
        print("Generic Robot Demonstration")
        print("=" * 50)

        print(f"\n{self.summary()}")

        print(f"\n\nConfigurations:")
        for config_name in ["qr", "qz"]:
            q = getattr(self, config_name)
            T = self.fkine(q)
            print(f"  {config_name}: {q}")
            print(
                f"      End-effector position: [{T.t[0]:.3f}, {T.t[1]:.3f}, {T.t[2]:.3f}]"
            )

        print(f"\nJoint limits check:")
        test_q = np.zeros(self.dofs)
        within_limits = not np.any(self.islimit(test_q))
        print(f"  Zero config within limits: {within_limits}")

    def __str__(self) -> str:
        """String representation of the robot."""
        return self.summary()

    def __repr__(self) -> str:
        """Detailed representation of the robot."""
        return f"Generic(dofs={self.dofs}, name='{self.name}')"

    def plotly(
        self,
        q: Optional[List[float]] = None,
        frame_size: float = 0.1,  # Size of coordinate frames in meters
        is_show: bool = True,  # Whether to display the plot immediately
        show_z_axis: bool = True,
        show_all_axes: bool = False,
        **kwargs,
    ) -> "plotly.graph_objects.Figure":
        """
        Visualize the robot using Plotly (if available).

        Args:
            q: Joint configuration to visualize (default: qz)
            **kwargs: Additional arguments for visualization

        Raises:
            ImportError: If Plotly is not installed
        """
        try:
            import plotly.graph_objects as go
            import plotly.express as px
        except ImportError:
            raise ImportError(
                "Plotly is required for visualization. Install with: pip install plotly"
            )

        if q is None:
            q = self.qz

        # Compute forward kinematics for all links
        link_poses = []
        for i in range(self.n + 1):  # Include base
            if i == 0:
                T = self.base  # Base frame
            else:
                T = self.fkine(q, end=i - 1)
            link_poses.append(T)

        # Extract positions for plotting
        positions = np.array([T.t for T in link_poses])

        # Create 3D plot
        fig = go.Figure()

        # Plot robot links
        fig.add_trace(
            go.Scatter3d(
                x=positions[:, 0],
                y=positions[:, 1],
                z=positions[:, 2],
                mode="lines",
                name=f"{self.name} Links",
                line=dict(width=15, color="#E1706E"),
            )
        )

        # Add coordinate frames at each joint
        colors = ["#F84752", "#BBDA55", "#8EC1E1"]  # X, Y, Z axis colors
        directions = ["X", "Y", "Z"]
        arrow_length = frame_size * 0.2  # Length of the cone arrowhead

        for i, T in enumerate(link_poses):
            origin = T.t
            for axis_idx in range(3):  # X, Y, Z axes
                if (axis_idx < 2 and show_all_axes) or (axis_idx == 2 and show_z_axis):
                    direction = T.R[:, axis_idx] / np.linalg.norm(T.R[:, axis_idx])
                    end_point = origin + frame_size * direction

                    # Determine color for Z-axis of the last frame
                    if axis_idx == 2 and i == len(link_poses) - 1:  # Last frame Z-axis
                        axis_color = "#800080"  # Purple for end-effector Z-axis
                    else:
                        axis_color = colors[axis_idx]

                    # Add axis line
                    fig.add_trace(
                        go.Scatter3d(
                            x=[origin[0], end_point[0]],
                            y=[origin[1], end_point[1]],
                            z=[origin[2], end_point[2]],
                            mode="lines",
                            name=f"Frame {i} {directions[axis_idx]}",
                            line=dict(width=5, color=axis_color),
                        )
                    )

                    # Add cone (arrowhead)
                    fig.add_trace(
                        go.Cone(
                            x=[end_point[0]],
                            y=[end_point[1]],
                            z=[end_point[2]],
                            u=[direction[0]],
                            v=[direction[1]],
                            w=[direction[2]],
                            sizemode="absolute",
                            sizeref=arrow_length,
                            showscale=False,
                            colorscale=[[0, axis_color], [1, axis_color]],
                            cmin=0,
                            cmax=1,
                        )
                    )

        # Print configuration info
        print(f"\nRobot Configuration:")
        print(f"Joint angles: {np.array(q)}")
        print(f"End-effector position: {link_poses[-1].t}")
        rpy_rad = link_poses[-1].rpy()
        rpy_deg = np.array(rpy_rad) * 180 / np.pi
        print(f"End-effector orientation (RPY): {rpy_deg} degrees")

        # Set maximum and minimum limits for axes
        max_range = np.max(np.abs(positions))
        min_range = -max_range
        fig.update_layout(
            scene=dict(
                xaxis=dict(
                    nticks=10,
                    range=[-1.2 * max_range, 1.2 * max_range],
                    title="X (m)",
                ),
                yaxis=dict(
                    nticks=10,
                    range=[-1.2 * max_range, 1.2 * max_range],
                    title="Y (m)",
                ),
                zaxis=dict(
                    nticks=10,
                    range=[-1 * max_range, 1.2 * max_range],
                    title="Z (m)",
                ),
            )
        )

        # Update layout
        fig.update_layout(
            title=f"{self.name} Robot Visualization",
            scene=dict(
                xaxis_title="X (m)",
                yaxis_title="Y (m)",
                zaxis_title="Z (m)",
                aspectmode="cube",
            ),
            showlegend=False,
            width=800,
            height=600,
        )

        if is_show:
            fig.show()

        return fig


def create_generic_robot(
    dofs: int, link_lengths: Optional[List[float]] = None, **kwargs
) -> Generic:
    """
    Factory function to create a generic robot with sensible defaults.

    Args:
        dofs: Number of degrees of freedom
        link_lengths: Link lengths (default: equal lengths for anthropomorphic arm)
        **kwargs: Additional arguments passed to Generic constructor

    Returns:
        Generic robot instance

    Examples:
        >>> # Simple 3-DOF arm with equal link lengths
        >>> robot = create_generic_robot(3, link_lengths=[0.3, 0.3, 0.2])
        >>>
        >>> # 6-DOF arm with anthropomorphic proportions
        >>> robot = create_generic_robot(6)
    """
    if link_lengths is None:
        if dofs <= 3:
            # Short arm
            link_lengths = [0.3] * dofs
        else:
            # Longer arm with varied link lengths
            link_lengths = [0.1, 0.4, 0.3] + [0.1] * (dofs - 3)

    # Create anthropomorphic joint configuration
    if dofs >= 6:
        # 6-DOF with spherical wrist, extend pattern for more DOFs
        alpha = [pi / 2, 0, pi / 2, -pi / 2, pi / 2, 0]
        d = [0.2, 0, 0, 0.4, 0, 0.1]

        # Extend for more than 6 DOFs
        if dofs > 6:
            # Add more joints with alternating alpha values
            for i in range(6, dofs):
                alpha.append(pi / 2 if i % 2 == 0 else 0)
                d.append(0.1 if i % 2 == 0 else 0)
    elif dofs >= 3:
        # Planar arm
        alpha = [0] * dofs
        d = [0.1] + [0] * (dofs - 1)
    else:
        # Simple 2-DOF
        alpha = [0] * dofs
        d = [0] * dofs

    return Generic(
        dofs=dofs, a=link_lengths, alpha=alpha, d=d, name=f"Generic{dofs}DOF", **kwargs
    )


if __name__ == "__main__":  # pragma: no cover
    # Demo when run as script
    print("Creating various generic robots...\n")

    # Simple 3-DOF robot
    robot3 = create_generic_robot(3, name="Simple3DOF")
    robot3.demo()

    print("\n" + "=" * 60 + "\n")

    # 6-DOF robot with custom parameters
    robot6 = Generic(
        dofs=6,
        a=[0, 0.4, 0.3, 0, 0, 0],
        d=[0.2, 0, 0, 0.4, 0, 0.1],
        alpha=[pi / 2, 0, pi / 2, -pi / 2, pi / 2, 0],
        name="Custom6DOF",
    )
    robot6.demo()
