"""
Forward kinematics algorithms for robotics-numpy

This module provides efficient forward kinematics computation for robot manipulators
using DH parameters. Optimized for performance with NumPy vectorization.
"""

import numpy as np
from typing import List, Union, Optional
from ..transforms import SE3
from ..models.dh_link import DHLink

# Type aliases
ArrayLike = Union[float, int, np.ndarray, List[float]]
JointConfig = Union[List[float], np.ndarray]


def fkine_dh(links: List[DHLink], q: JointConfig) -> SE3:
    """
    Forward kinematics using DH parameters.

    Computes the transformation from the base frame to the end-effector frame
    by multiplying individual link transformation matrices.

    Args:
        links: List of DH links
        q: Joint configuration (n joint values)

    Returns:
        SE3 transformation from base to end-effector

    Examples:
        >>> links = [RevoluteDH(d=0.1, a=0.2, alpha=0),
        ...          RevoluteDH(d=0, a=0.3, alpha=0)]
        >>> T = fkine_dh(links, [0, np.pi/4])
        >>> print(T)
    """
    # Import here to avoid circular imports
    from ..models.dh_robot import _fkine_dh_single
    return _fkine_dh_single(links, q)


def fkine_dh_all(links: List[DHLink], q: JointConfig) -> List[SE3]:
    """
    Forward kinematics for all intermediate frames.

    Computes transformations from base to each link frame, useful for
    visualization and intermediate pose calculations.

    Args:
        links: List of DH links
        q: Joint configuration

    Returns:
        List of SE3 transformations, one for each link frame

    Examples:
        >>> links = [RevoluteDH(d=0.1, a=0.2, alpha=0),
        ...          RevoluteDH(d=0, a=0.3, alpha=0)]
        >>> transforms = fkine_dh_all(links, [0, np.pi/4])
        >>> print(f"Link 1 pose: {transforms[0]}")
        >>> print(f"End-effector pose: {transforms[1]}")
    """
    q = np.asarray(q, dtype=float)

    if len(q) != len(links):
        raise ValueError(f"Joint configuration length ({len(q)}) must match number of links ({len(links)})")

    transforms = []
    T = SE3()  # Start with identity

    # Accumulate transformations
    for i, (link, qi) in enumerate(zip(links, q)):
        try:
            T_link = link.A(qi)
            T = T * T_link
            transforms.append(T)
        except Exception as e:
            raise RuntimeError(f"Error computing transformation for link {i}: {e}")

    return transforms


def fkine_dh_partial(links: List[DHLink], q: JointConfig,
                     start: int = 0, end: Optional[int] = None) -> SE3:
    """
    Forward kinematics for a partial chain of links.

    Computes transformation from start link to end link (inclusive).

    Args:
        links: List of DH links
        q: Joint configuration
        start: Starting link index (default: 0)
        end: Ending link index (default: last link)

    Returns:
        SE3 transformation from start to end frame

    Examples:
        >>> # Compute transformation from link 1 to link 3
        >>> T = fkine_dh_partial(links, q, start=1, end=3)
    """
    q = np.asarray(q, dtype=float)

    if len(q) != len(links):
        raise ValueError(f"Joint configuration length ({len(q)}) must match number of links ({len(links)})")

    if end is None:
        end = len(links) - 1

    if not (0 <= start <= end < len(links)):
        raise ValueError(f"Invalid range: start={start}, end={end}, n_links={len(links)}")

    # Extract relevant links and joint values
    partial_links = links[start:end+1]
    partial_q = q[start:end+1]

    return fkine_dh(partial_links, partial_q)


def fkine_dh_batch(links: List[DHLink], q_batch: np.ndarray) -> List[SE3]:
    """
    Batch forward kinematics for multiple configurations.

    Efficiently computes forward kinematics for multiple joint configurations.

    Args:
        links: List of DH links
        q_batch: Batch of joint configurations (m x n array)

    Returns:
        List of SE3 transformations, one for each configuration

    Examples:
        >>> # Compute FK for multiple configurations
        >>> q_batch = np.array([[0, 0, 0], [0.1, 0.2, 0.3], [0.5, -0.5, 1.0]])
        >>> transforms = fkine_dh_batch(links, q_batch)
    """
    q_batch = np.asarray(q_batch, dtype=float)

    if q_batch.ndim == 1:
        q_batch = q_batch.reshape(1, -1)

    if q_batch.shape[1] != len(links):
        raise ValueError(f"Joint configuration width ({q_batch.shape[1]}) must match number of links ({len(links)})")

    transforms = []
    for i in range(q_batch.shape[0]):
        T = fkine_dh(links, q_batch[i])
        transforms.append(T)

    return transforms


def link_poses(links: List[DHLink], q: JointConfig, base: Optional[SE3] = None) -> List[SE3]:
    """
    Compute poses of all link frames in world coordinates.

    Args:
        links: List of DH links
        q: Joint configuration
        base: Base transformation (default: identity)

    Returns:
        List of link poses in world frame

    Examples:
        >>> # Get all link poses including base transformation
        >>> base_transform = SE3.Trans(0, 0, 0.5)  # Robot on table
        >>> poses = link_poses(links, q, base=base_transform)
    """
    q = np.asarray(q, dtype=float)

    if len(q) != len(links):
        raise ValueError(f"Joint configuration length ({len(q)}) must match number of links ({len(links)})")

    if base is None:
        base = SE3()

    # Get all intermediate transformations
    transforms = fkine_dh_all(links, q)

    # Apply base transformation to all poses
    world_poses = [base * T for T in transforms]

    return world_poses


def joint_axes(links: List[DHLink], q: JointConfig, base: Optional[SE3] = None) -> List[np.ndarray]:
    """
    Compute joint axis directions in world coordinates.

    Args:
        links: List of DH links
        q: Joint configuration
        base: Base transformation (default: identity)

    Returns:
        List of joint axis unit vectors in world frame

    Examples:
        >>> # Get joint axes for visualization
        >>> axes = joint_axes(links, q)
        >>> print(f"Joint 0 axis: {axes[0]}")
    """
    q = np.asarray(q, dtype=float)

    if len(q) != len(links):
        raise ValueError(f"Joint configuration length ({len(q)}) must match number of links ({len(links)})")

    if base is None:
        base = SE3()

    # Get link poses
    poses = link_poses(links, q, base)

    # Extract Z-axis (joint axis) from each transformation
    axes = []
    for i, pose in enumerate(poses):
        # For DH convention, joint axis is always Z-axis of previous frame
        if i == 0:
            # First joint axis is Z-axis of base frame
            z_axis = base.R @ np.array([0, 0, 1])
        else:
            # Joint i axis is Z-axis of frame i-1
            z_axis = poses[i-1].R @ np.array([0, 0, 1])

        axes.append(z_axis)

    return axes


def validate_joint_config(links: List[DHLink], q: JointConfig,
                         check_limits: bool = True, warn: bool = True) -> bool:
    """
    Validate joint configuration against robot model.

    Args:
        links: List of DH links
        q: Joint configuration to validate
        check_limits: Whether to check joint limits
        warn: Whether to print warnings

    Returns:
        True if configuration is valid

    Examples:
        >>> # Check if configuration is valid
        >>> valid = validate_joint_config(links, q, check_limits=True)
        >>> if not valid:
        ...     print("Invalid configuration!")
    """
    q = np.asarray(q, dtype=float)

    # Check dimensions
    if len(q) != len(links):
        if warn:
            print(f"Error: Joint configuration length ({len(q)}) must match number of links ({len(links)})")
        return False

    # Check for NaN or infinite values
    if not np.all(np.isfinite(q)):
        if warn:
            print("Error: Joint configuration contains NaN or infinite values")
        return False

    # Check joint limits if requested
    if check_limits:
        for i, (link, qi) in enumerate(zip(links, q)):
            if link.qlim is not None:
                qmin, qmax = link.qlim
                if not (qmin <= qi <= qmax):
                    if warn:
                        if link.is_revolute():
                            print(f"Warning: Joint {i} ({qi:.3f} rad = {np.degrees(qi):.1f}°) "
                                  f"outside limits [{np.degrees(qmin):.1f}°, {np.degrees(qmax):.1f}°]")
                        else:
                            print(f"Warning: Joint {i} ({qi:.3f} m) outside limits [{qmin:.3f}, {qmax:.3f}] m")
                    return False

    return True


def fkine_performance_test(links: List[DHLink], n_iterations: int = 10000) -> dict:
    """
    Performance test for forward kinematics computation.

    Args:
        links: List of DH links
        n_iterations: Number of iterations to run

    Returns:
        Dictionary with performance statistics

    Examples:
        >>> # Test FK performance
        >>> stats = fkine_performance_test(links, n_iterations=10000)
        >>> print(f"Mean time: {stats['mean_time_us']:.2f} μs")
    """
    import time

    # Generate random valid joint configuration
    q = np.zeros(len(links))
    for i, link in enumerate(links):
        if link.qlim is not None:
            qmin, qmax = link.qlim
            q[i] = np.random.uniform(qmin, qmax)
        else:
            if link.is_revolute():
                q[i] = np.random.uniform(-np.pi, np.pi)
            else:
                q[i] = np.random.uniform(-1.0, 1.0)

    # Warmup
    for _ in range(100):
        fkine_dh(links, q)

    # Actual timing
    times = []
    for _ in range(n_iterations):
        start = time.perf_counter()
        T = fkine_dh(links, q)
        end = time.perf_counter()
        times.append(end - start)

    times = np.array(times)

    return {
        'mean_time_us': np.mean(times) * 1e6,
        'std_time_us': np.std(times) * 1e6,
        'min_time_us': np.min(times) * 1e6,
        'max_time_us': np.max(times) * 1e6,
        'median_time_us': np.median(times) * 1e6,
        'iterations': n_iterations,
        'total_time_s': np.sum(times),
        'target_position': T.t,
        'target_orientation_rpy': T.rpy(),
    }


# Convenience functions for common robot types
def fkine_6dof(links: List[DHLink], q: JointConfig) -> SE3:
    """
    Forward kinematics for 6-DOF manipulator with validation.

    Args:
        links: List of exactly 6 DH links
        q: Joint configuration with 6 values

    Returns:
        SE3 end-effector transformation

    Raises:
        ValueError: If not exactly 6 DOF
    """
    if len(links) != 6:
        raise ValueError(f"Expected 6 links, got {len(links)}")

    q = np.asarray(q, dtype=float)
    if len(q) != 6:
        raise ValueError(f"Expected 6 joint values, got {len(q)}")

    return fkine_dh(links, q)


def fkine_planar(links: List[DHLink], q: JointConfig) -> SE3:
    """
    Forward kinematics for planar manipulator (all alpha=0).

    Args:
        links: List of DH links (should have alpha=0 for all)
        q: Joint configuration

    Returns:
        SE3 end-effector transformation
    """
    # Verify it's actually planar
    for i, link in enumerate(links):
        if abs(link.alpha) > 1e-6:
            print(f"Warning: Link {i} has non-zero alpha ({link.alpha}), not truly planar")

    return fkine_dh(links, q)
