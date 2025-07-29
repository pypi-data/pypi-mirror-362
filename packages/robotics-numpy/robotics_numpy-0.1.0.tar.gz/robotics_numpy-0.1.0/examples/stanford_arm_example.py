#!/usr/bin/env python3
"""
Simple Stanford Arm Usage Example for robotics-numpy

This example shows the basic usage of the Stanford Arm robot model
with forward kinematics computation. This demonstrates the key features
implemented in Phase 2.

Run this example:
    python examples/stanford_arm_example.py
"""

import numpy as np
import sys
import os

# Add the src directory to the path so we can import robotics_numpy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import robotics_numpy as rn


def main():
    """Simple Stanford Arm example."""
    print("Stanford Arm Example - robotics-numpy")
    print("=" * 50)

    # Create Stanford Arm robot
    print("Creating Stanford Arm robot...")
    robot = rn.models.Stanford()
    print(f"✅ Created {robot.name} with {robot.n} joints")
    print(f"   Joint types: {robot.joint_types}")

    # Test different configurations
    print("\n🔧 Testing different configurations:")

    configurations = {
        "Zero position": robot.qz,
        "Extended": robot.qextended,
        "Folded": robot.qfolded,
        "Custom": [0.2, 0.3, 0.4, 0.1, 0.5, 0.0]
    }

    for name, q in configurations.items():
        print(f"\n{name}:")
        print(f"  Joint values: {np.array(q)}")

        # Compute forward kinematics
        T = robot.fkine(q)
        pos = T.t
        rpy = np.degrees(T.rpy())

        print(f"  End-effector position: [{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}] m")
        print(f"  End-effector orientation: [{rpy[0]:.1f}°, {rpy[1]:.1f}°, {rpy[2]:.1f}°]")

        # Check if reachable
        reachable = robot.reach(pos)
        print(f"  Reachability: {'✅ Yes' if reachable else '❌ No'}")

        # Check singularity
        singular = robot.is_singular(q)
        print(f"  Singularity: {'⚠️ Singular' if singular else '✅ Regular'}")

    # Demonstrate workspace analysis
    print(f"\n🌐 Workspace Analysis:")
    volume = robot.workspace_volume()
    print(f"  Estimated workspace volume: {volume:.2f} m³")

    # Test some points
    test_points = [
        [0.5, 0, 0.5],
        [0, 0.8, 0.3],
        [1.0, 0, 0],
        [0, 0, -0.3]
    ]

    print("  Point reachability test:")
    for point in test_points:
        reachable = robot.reach(np.array(point))
        status = "✅ Reachable" if reachable else "❌ Not reachable"
        print(f"    {point}: {status}")

    # Performance test
    print(f"\n⚡ Performance Test:")
    import time

    q_test = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    n_iterations = 1000

    start_time = time.perf_counter()
    for _ in range(n_iterations):
        T = robot.fkine(q_test)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / n_iterations * 1e6  # Convert to microseconds
    print(f"  Forward kinematics: {avg_time:.1f} μs per computation")
    print(f"  ({n_iterations} iterations completed)")

    # Show robot info
    print(f"\n📋 Robot Information:")
    print(f"  Model: {robot.name}")
    print(f"  Manufacturer: {robot.manufacturer}")
    print(f"  DOF: {robot.n}")
    print(f"  Spherical wrist: {'Yes' if robot.isspherical() else 'No'}")
    print(f"  Available configurations: {', '.join(robot.configurations())}")

    print(f"\n🎉 Example completed successfully!")
    print(f"Try modifying the joint values in 'Custom' configuration above.")


if __name__ == "__main__":
    main()
