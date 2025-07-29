#!/usr/bin/env python3
"""
User's Generic Robot Example for robotics-numpy

This script demonstrates the exact example provided by the user,
showing how to create a Generic robot with custom DH parameters
and use it for forward kinematics and visualization.
"""

import numpy as np
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from robotics_numpy.models import Generic

# Constants
pi = np.pi

def main():
    """Demonstrate the user's Generic robot example."""

    print("User's Generic Robot Example")
    print("=" * 40)
    print()

    # Create the robot exactly as specified by the user
    robot = Generic(
        dofs=4,
        a=[0, -0.5, -0.5, -0.5],
        d=[0.5, 0, 0, 0],
        alpha=[pi / 2, 0, 0, 0],
        # offset=[0, pi / 4, -pi / 4, pi / 2],  # Commented out in original
        qlim=[[-pi, pi], [-pi / 2, pi / 2], [-pi / 3, pi / 3], [-pi / 6, pi / 6]],
        name="GenericRobot",
    )

    print("✓ Robot created successfully!")
    print(f"  Name: {robot.name}")
    print(f"  DOFs: {robot.dofs}")
    print(f"  Joint types: {' '.join(robot.joint_types)}")
    print()

    # Display robot summary
    print("Robot Configuration:")
    print("-" * 20)
    print(robot)
    print()

    # Test forward kinematics with different configurations
    print("Forward Kinematics Results:")
    print("-" * 30)

    configurations = {
        "qz (zero)": robot.qz,
        "qr (ready)": robot.qr,
        "custom_1": [0.1, -0.2, 0.3, -0.1],
        "custom_2": [pi/4, -pi/6, pi/6, -pi/12],
        "joint_limits": [pi/2, pi/4, pi/4, pi/8]
    }

    print("Config       |   X    |   Y    |   Z    | Status")
    print("-------------+--------+--------+--------+--------")

    for name, q in configurations.items():
        try:
            # Check if configuration is within limits
            at_limits = robot.islimit(q)
            if np.any(at_limits):
                status = "AT_LIM"
            else:
                status = "OK"

            # Compute forward kinematics
            T = robot.fkine(q)
            print(f"{name:11s} | {T.t[0]:6.3f} | {T.t[1]:6.3f} | {T.t[2]:6.3f} | {status}")

        except Exception as e:
            print(f"{name:11s} | ERROR: {str(e)[:20]}...")

    print()

    # Set some realistic dynamic properties
    print("Setting Dynamic Properties:")
    print("-" * 30)

    robot.set_dynamic_properties(
        m=[2.0, 5.0, 3.0, 1.0],  # Link masses (kg)
        r=[  # Centers of mass relative to link frames
            [0.0, 0.0, 0.25],    # Link 0 COM
            [-0.25, 0.0, 0.0],   # Link 1 COM
            [-0.25, 0.0, 0.0],   # Link 2 COM
            [-0.25, 0.0, 0.0]    # Link 3 COM
        ],
        I=[  # Inertia tensors [Ixx, Iyy, Izz, Ixy, Iyz, Ixz]
            [0.1, 0.1, 0.05, 0, 0, 0],
            [0.2, 0.05, 0.2, 0, 0, 0],
            [0.15, 0.04, 0.15, 0, 0, 0],
            [0.05, 0.02, 0.05, 0, 0, 0]
        ]
    )

    print("✓ Dynamic properties set successfully")
    print(f"  Total robot mass: {sum([link.m for link in robot.links]):.1f} kg")
    print()

    # Workspace analysis
    print("Workspace Analysis:")
    print("-" * 20)
    print(f"Max reach: {robot.workspace_radius():.3f} m")

    # Test some points for reachability (simplified check)
    test_points = [
        [0.5, 0, 0.5],
        [1.0, 0, 0.5],
        [1.5, 0, 0.5],
        [2.0, 0, 0.5]
    ]

    print("\nReachability test (approximate):")
    for point in test_points:
        distance = np.linalg.norm(point)
        max_reach = robot.workspace_radius()
        reachable = "✓" if distance <= max_reach else "✗"
        print(f"  Point {point}: {reachable} (dist: {distance:.3f}m)")

    print()

    # Test the plotly visualization method
    print("Visualization Test:")
    print("-" * 20)

    try:
        print("Attempting to visualize robot with Plotly...")
        robot.plotly(robot.qz)
        print("✓ Visualization opened in browser")
    except ImportError as e:
        print(f"⚠️  Visualization not available: {e}")
        print("   To enable visualization, install plotly:")
        print("   pip install plotly")
    except Exception as e:
        print(f"✗ Visualization error: {e}")

    print()

    # Performance test
    print("Performance Test:")
    print("-" * 20)

    import time

    # Time forward kinematics
    n_trials = 1000
    q_test = robot.qz

    start_time = time.time()
    for _ in range(n_trials):
        T = robot.fkine(q_test)
    end_time = time.time()

    avg_time_us = (end_time - start_time) / n_trials * 1e6
    print(f"Forward kinematics: {avg_time_us:.1f} μs per call")
    print(f"                   ({n_trials} trials)")

    print()
    print("=" * 40)
    print("Example completed successfully!")
    print()
    print("Next steps:")
    print("- Try different joint configurations")
    print("- Modify DH parameters for your robot")
    print("- Add dynamic properties for your application")
    print("- Install plotly for 3D visualization")
    print()
    print("Example usage:")
    print(">>> from robotics_numpy.models import Generic")
    print(">>> robot = Generic(dofs=6, a=[...], d=[...], alpha=[...])")
    print(">>> T = robot.fkine([0, 0, 0, 0, 0, 0])")
    print(">>> robot.plotly()  # If plotly is installed")


if __name__ == "__main__":
    main()
