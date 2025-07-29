"""
Jacobian computation for robotics-numpy

This module provides functions for computing manipulator Jacobians and manipulability.
Jacobians relate joint velocities to end-effector velocities, and are essential for
velocity control, singularity analysis, and manipulability evaluation.
"""

import numpy as np
from typing import Optional, Union, List, Tuple, Literal
from ..transforms import SE3

# Type aliases
ArrayLike = Union[float, int, np.ndarray, List[float]]
JointConfig = Union[List[float], np.ndarray]


def tr2jac(T: np.ndarray) -> np.ndarray:
    """
    Transform from end-effector to world frame Jacobian conversion.

    This transforms a Jacobian matrix from the end-effector frame to the world frame.

    Args:
        T: Homogeneous transformation matrix (4x4)

    Returns:
        6x6 Jacobian transformation matrix

    Notes:
        For a Jacobian Je in end-effector frame, the equivalent Jacobian J0 in world frame
        is J0 = tr2jac(T) @ Je
    """
    R = T[:3, :3]

    # Construct the 6x6 Jacobian transformation matrix
    Jmat = np.zeros((6, 6))
    Jmat[:3, :3] = R
    Jmat[3:, 3:] = R

    return Jmat


def jacobe(
    robot, q: JointConfig, end: Optional[int] = None, start: int = 0
) -> np.ndarray:
    """
    Manipulator Jacobian in end-effector frame

    Args:
        robot: DHRobot instance
        q: Joint coordinate vector
        end: End link index (default: end-effector)
        start: Start link index (default: 0)

    Returns:
        The manipulator Jacobian in the end-effector frame (6xn)

    Notes:
        - The end-effector Jacobian gives the relationship between joint velocities
          and end-effector spatial velocity expressed in the end-effector frame.
    """
    q = np.asarray(q, dtype=float)
    n = robot.n

    if end is None:
        end = n - 1

    if not (0 <= start <= end < n):
        raise ValueError(f"Invalid link range: start={start}, end={end}, n={n}")

    # Create Jacobian matrix and initialize
    J = np.zeros((6, end - start + 1))

    # Get link transforms up to the end link
    Tall = robot.fkine_all(q)

    # End-effector transform
    Te = Tall[end]

    # Tool offset for computing the Jacobian at tool tip (if any)
    Tt = robot.tool.matrix

    # Calculate the Jacobian
    for j in range(start, end + 1):
        # Joint transform
        if j > 0:
            Tj = Tall[j - 1]
        else:
            Tj = robot.base

        # Joint type and axis
        if robot.joint_types[j] == "R":  # Revolute joint
            # Revolute joint axis is the z-axis of the joint frame
            axis = Tj.matrix[:3, 2]  # z-axis of the joint frame
        else:  # Prismatic joint
            # Prismatic joint axis is the z-axis of the joint frame
            axis = Tj.matrix[:3, 2]  # z-axis of the joint frame

        # Position of the joint
        joint_pos = Tj.t

        # Position of the end-effector considering tool transform
        if np.any(Tt[:3, 3] != 0):
            # If there's a tool offset, use it
            ee_pos = Te.t + Te.R @ Tt[:3, 3]
        else:
            ee_pos = Te.t

        # Displacement from joint to end-effector
        r = ee_pos - joint_pos

        col = j - start

        if robot.joint_types[j] == "R":  # Revolute joint
            # Angular velocity component (rotational joints)
            J[3:, col] = axis

            # Linear velocity component (cross product)
            J[:3, col] = np.cross(axis, r)
        else:  # Prismatic joint
            # Linear velocity component (prismatic joints)
            J[:3, col] = axis

            # Prismatic joints don't contribute to angular velocity
            J[3:, col] = 0

    # The Jacobian as computed is in the world frame
    # Convert to end-effector frame
    Tr = np.eye(6)
    Tr[:3, :3] = Te.R.T
    Tr[3:, 3:] = Te.R.T

    return Tr @ J


def jacob0(
    robot,
    q: JointConfig = None,
    T=None,
    half: Optional[str] = None,
    start: int = 0,
    end: Optional[int] = None,
) -> np.ndarray:
    """
    Manipulator Jacobian in world frame

    Args:
        robot: DHRobot instance
        q: Joint coordinate vector
        T: Forward kinematics if known (SE3 matrix)
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

    q = np.asarray(q, dtype=float)

    # Compute forward kinematics if not provided
    if T is None:
        T = robot.fkine(q, end=end, start=start)

    # Compute Jacobian in end-effector frame
    Je = jacobe(robot, q, end=end, start=start)

    # Transform to world frame
    J0 = tr2jac(T.matrix) @ Je

    # Return top or bottom half if requested
    if half is not None:
        if half == "trans":
            J0 = J0[:3, :]
        elif half == "rot":
            J0 = J0[3:, :]
        else:
            raise ValueError("half must be 'trans' or 'rot'")

    return J0


def manipulability(
    robot,
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
        robot: DHRobot instance
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
    # Need either joint configuration or Jacobian
    if q is None and J is None:
        raise ValueError("Either q or J must be provided")

    # Compute Jacobian if not provided
    if J is None:
        J = jacob0(robot, q, end=end, start=start)

    # Select axes to use
    if isinstance(axes, str):
        if axes == "all":
            J_used = J
        elif axes == "trans":
            J_used = J[:3, :]
        elif axes == "rot":
            J_used = J[3:, :]
        else:
            raise ValueError("axes must be 'all', 'trans', 'rot', or a boolean list")
    elif isinstance(axes, list) and all(isinstance(x, bool) for x in axes):
        if len(axes) != 6:
            raise ValueError("Boolean list for axes must have 6 elements")
        # Select rows based on boolean mask
        J_used = J[np.array(axes), :]
    else:
        raise ValueError("axes must be 'all', 'trans', 'rot', or a boolean list")

    # Compute manipulability based on selected method
    if method == "yoshikawa":
        # Yoshikawa's measure - square root of determinant of J*J^T
        m = np.sqrt(np.linalg.det(J_used @ J_used.T))

    elif method == "invcondition":
        # Inverse condition number - ratio of minimum to maximum singular value
        s = np.linalg.svd(J_used, compute_uv=False)
        if np.max(s) == 0:
            m = 0  # At singularity
        else:
            m = np.min(s) / np.max(s)

    elif method == "minsingular":
        # Minimum singular value - distance from singularity
        s = np.linalg.svd(J_used, compute_uv=False)
        m = np.min(s)

    elif method == "asada":
        # Asada's method - uses robot dynamics (requires mass/inertia data)
        # Not fully implemented without robot dynamics
        raise NotImplementedError(
            "Asada's method requires robot dynamics implementation"
        )

    else:
        raise ValueError(
            "Unknown method. Use 'yoshikawa', 'invcondition', or 'minsingular'"
        )

    return m


# Velocity ellipsoid functions
def joint_velocity_ellipsoid(
    J: np.ndarray, dq_max: np.ndarray = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute joint velocity ellipsoid axes.

    Args:
        J: Jacobian matrix (6xn)
        dq_max: Maximum joint velocities (n-vector)

    Returns:
        Tuple of (eigenvalues, eigenvectors) representing the ellipsoid
    """
    if dq_max is None:
        # Unit joint velocity sphere
        M = J @ J.T
    else:
        # Normalize by maximum joint velocities
        dq_max = np.asarray(dq_max)
        Wq = np.diag(1.0 / dq_max**2)
        M = J @ Wq @ J.T

    # Eigendecomposition gives ellipsoid axes
    eigvals, eigvecs = np.linalg.eigh(M)

    return eigvals, eigvecs
