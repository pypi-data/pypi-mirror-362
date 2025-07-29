#!/usr/bin/env python3
"""
Generic Robot Demonstration for robotics-numpy

This example demonstrates how to use the Generic robot class to create
custom robot configurations with arbitrary DH parameters.

The Generic class allows you to:
- Create robots with any number of DOFs
- Specify custom DH parameters (a, d, alpha, offset)
- Mix revolute and prismatic joints
- Set dynamic properties
- Perform forward kinematics

Examples include:
1. Simple planar arms
2. Anthropomorphic 6-DOF arms
3. Mixed joint type robots
4. Custom industrial robot configurations
"""

import numpy as np
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from robotics_numpy.models import Generic, create_generic_robot

# Constants
pi = np.pi
deg = pi / 180


def demo_simple_planar_arm():
    """Demonstrate a simple 3-DOF planar arm."""
    print("=" * 60)
    print("1. Simple 3-DOF Planar Arm")
    print("=" * 60)

    # Create a 3-DOF planar arm (all joints parallel)
    robot = Generic(
        dofs=3,
        a=[0.3, 0.25, 0.15],  # Link lengths
        d=[0.1, 0, 0],        # Only first joint has offset
        alpha=[0, 0, 0],      # All joints parallel (planar)
        offset=[0, 0, 0],     # No joint offsets
        name="Planar3DOF"
    )

    print(robot)
    print()

    # Test different configurations
    configurations = {
        "Zero": [0, 0, 0],
        "90°-0°-0°": [pi/2, 0, 0],
        "45°-45°-45°": [pi/4, pi/4, pi/4],
        "Folded": [0, pi/2, -pi/2]
    }

    print("Forward Kinematics Results:")
    print("Configuration        |   X    |   Y    |   Z    ")
    print("--------------------+--------+--------+--------")

    for name, q in configurations.items():
        T = robot.fkine(q)
        print(f"{name:18s} | {T.t[0]:6.3f} | {T.t[1]:6.3f} | {T.t[2]:6.3f}")


def demo_anthropomorphic_6dof():
    """Demonstrate a 6-DOF anthropomorphic arm with spherical wrist."""
    print("\n" + "=" * 60)
    print("2. Anthropomorphic 6-DOF Arm (Spherical Wrist)")
    print("=" * 60)

    # Create a 6-DOF robot similar to industrial arms
    robot = Generic(
        dofs=6,
        a=[0, 0.4, 0.3, 0, 0, 0],           # Upper arm, forearm lengths
        d=[0.15, 0, 0, 0.35, 0, 0.08],      # Base height, wrist extension, tool
        alpha=[pi/2, 0, pi/2, -pi/2, pi/2, 0],  # Standard 6-DOF configuration
        offset=[0, 0, 0, 0, 0, 0],          # No offsets
        qlim=[
            [-180*deg, 180*deg],   # Base rotation
            [-90*deg, 90*deg],     # Shoulder
            [-150*deg, 150*deg],   # Elbow
            [-180*deg, 180*deg],   # Wrist roll
            [-90*deg, 90*deg],     # Wrist pitch
            [-180*deg, 180*deg],   # Wrist yaw
        ],
        name="Anthropomorphic6DOF"
    )

    print(robot)
    print()

    # Set realistic dynamic properties
    robot.set_dynamic_properties(
        m=[5.0, 8.0, 3.0, 1.5, 1.0, 0.5],  # Masses (kg)
        r=[  # Centers of mass
            [0, 0, 0.075],
            [0, 0.2, 0],
            [0, 0.15, 0],
            [0, 0, 0.1],
            [0, 0, 0],
            [0, 0, 0.04]
        ]
    )

    # Test important configurations
    configurations = {
        "Home": [0, 0, 0, 0, 0, 0],
        "Ready": [0, -pi/4, pi/2, 0, pi/4, 0],
        "Reach_Front": [0, pi/6, pi/3, 0, pi/6, 0],
        "Reach_Side": [pi/2, -pi/6, pi/4, 0, pi/3, 0]
    }

    print("6-DOF Forward Kinematics:")
    print("Configuration  |   X    |   Y    |   Z    | Roll | Pitch| Yaw  ")
    print("---------------+--------+--------+--------+------+------+------")

    for name, q in configurations.items():
        T = robot.fkine(q)
        rpy = T.rpy()  # Roll-pitch-yaw angles
        print(f"{name:13s} | {T.t[0]:6.3f} | {T.t[1]:6.3f} | {T.t[2]:6.3f} | "
              f"{rpy[0]*180/pi:5.1f} | {rpy[1]*180/pi:5.1f} | {rpy[2]*180/pi:5.1f}")

    print(f"\nWorkspace radius: {robot.workspace_radius():.3f} m")


def demo_mixed_joint_types():
    """Demonstrate robot with mixed revolute and prismatic joints."""
    print("\n" + "=" * 60)
    print("3. Mixed Joint Types (R-P-R-R)")
    print("=" * 60)

    # Create robot similar to SCARA with vertical prismatic joint
    robot = Generic(
        dofs=4,
        joint_types=['R', 'R', 'P', 'R'],   # Mixed joint types
        a=[0.3, 0.25, 0, 0],               # SCARA-like link lengths
        d=[0.1, 0, 0, 0.05],               # Base height and tool offset
        alpha=[0, 0, 0, 0],                # All parallel (SCARA-style)
        qlim=[
            [-180*deg, 180*deg],           # Base rotation
            [-150*deg, 150*deg],           # Arm rotation
            [0, 0.2],                      # Vertical extension (m)
            [-180*deg, 180*deg],           # Tool rotation
        ],
        name="SCARA_Style"
    )

    print(robot)
    print()

    # Test configurations with prismatic joint
    configurations = {
        "Home": [0, 0, 0, 0],
        "Extended": [pi/4, pi/4, 0.15, pi/2],
        "Compact": [pi/6, -pi/3, 0.05, 0],
        "Reach": [pi/2, pi/6, 0.1, -pi/4]
    }

    print("Mixed Joint Forward Kinematics:")
    print("Configuration |   X    |   Y    |   Z    | Joint 3 (m)")
    print("-------------+--------+--------+--------+-----------")

    for name, q in configurations.items():
        T = robot.fkine(q)
        print(f"{name:11s} | {T.t[0]:6.3f} | {T.t[1]:6.3f} | {T.t[2]:6.3f} | {q[2]:8.3f}")


def demo_factory_functions():
    """Demonstrate factory functions for quick robot creation."""
    print("\n" + "=" * 60)
    print("4. Factory Functions for Quick Creation")
    print("=" * 60)

    # Create robots using factory function
    robots = {
        "3DOF": create_generic_robot(3),
        "4DOF": create_generic_robot(4, link_lengths=[0.2, 0.3, 0.2, 0.1]),
        "6DOF": create_generic_robot(6)
    }

    for name, robot in robots.items():
        print(f"\n{name} Robot:")
        print(f"  DOFs: {robot.n}")
        print(f"  Name: {robot.name}")
        print(f"  Max reach: {robot.workspace_radius():.3f} m")

        # Test zero configuration
        T = robot.fkine(robot.qz)
        print(f"  Zero config end-effector: [{T.t[0]:.3f}, {T.t[1]:.3f}, {T.t[2]:.3f}]")


def demo_custom_industrial_robot():
    """Demonstrate creating a custom industrial robot configuration."""
    print("\n" + "=" * 60)
    print("5. Custom Industrial Robot Configuration")
    print("=" * 60)

    # Create a robot inspired by common industrial designs
    robot = Generic(
        dofs=6,
        a=[0.025, 0.315, 0.035, 0, 0, 0],
        d=[0.147, 0, 0, 0.295, 0, 0.080],
        alpha=[pi/2, 0, pi/2, -pi/2, pi/2, 0],
        offset=[0, -pi/2, 0, 0, 0, 0],  # Shoulder joint offset
        qlim=[
            [-170*deg, 170*deg],
            [-65*deg, 85*deg],
            [-150*deg, 158*deg],
            [-180*deg, 180*deg],
            [-120*deg, 120*deg],
            [-360*deg, 360*deg],
        ],
        name="Industrial6R"
    )

    print(robot)
    print()

    # Set industrial-grade dynamic properties
    robot.set_dynamic_properties(
        m=[3.5, 15.0, 6.0, 2.5, 1.8, 0.3],  # Realistic masses
        Jm=[0.05, 0.2, 0.1, 0.02, 0.01, 0.005],  # Motor inertias
        G=[100, 100, 50, 50, 25, 25],  # Gear ratios
    )

    # Test typical industrial poses
    poses = {
        "Home": [0, 0, 0, 0, 0, 0],
        "Pick_Above": [pi/4, -pi/6, pi/3, 0, pi/6, 0],
        "Place_Side": [pi/2, -pi/4, pi/2, pi/2, 0, 0],
        "Maintenance": [0, -pi/2, pi/2, 0, pi/2, 0]
    }

    print("Industrial Robot Poses:")
    print("Pose         |   X    |   Y    |   Z    | Reach%")
    print("-------------+--------+--------+--------+-------")

    max_reach = robot.workspace_radius()
    for name, q in poses.items():
        T = robot.fkine(q)
        reach_pct = (np.linalg.norm(T.t) / max_reach) * 100
        print(f"{name:11s} | {T.t[0]:6.3f} | {T.t[1]:6.3f} | {T.t[2]:6.3f} | {reach_pct:5.1f}%")


def demo_performance_comparison():
    """Demonstrate performance characteristics."""
    print("\n" + "=" * 60)
    print("6. Performance Comparison")
    print("=" * 60)

    import time

    # Create robots of different sizes
    robot_sizes = [3, 6, 9, 12]

    print("Forward Kinematics Performance:")
    print("DOFs | Time per FK (μs) | Memory (links)")
    print("-----+------------------+--------------")

    for dofs in robot_sizes:
        robot = create_generic_robot(dofs)
        q = np.random.uniform(-pi, pi, dofs)

        # Time forward kinematics
        n_trials = 1000
        start_time = time.time()
        for _ in range(n_trials):
            T = robot.fkine(q)
        end_time = time.time()

        avg_time_us = (end_time - start_time) / n_trials * 1e6
        print(f" {dofs:2d}  | {avg_time_us:14.1f} | {len(robot.links):12d}")


def main():
    """Run all demonstrations."""
    print("Generic Robot Demonstration for robotics-numpy")
    print("This example shows various uses of the Generic robot class")

    try:
        demo_simple_planar_arm()
        demo_anthropomorphic_6dof()
        demo_mixed_joint_types()
        demo_factory_functions()
        demo_custom_industrial_robot()
        demo_performance_comparison()

        print("\n" + "=" * 60)
        print("All demonstrations completed successfully!")
        print("\nTo create your own robot:")
        print(">>> from robotics_numpy.models import Generic")
        print(">>> robot = Generic(dofs=6, a=[...], d=[...], alpha=[...])")
        print(">>> T = robot.fkine([0, 0, 0, 0, 0, 0])")

    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
