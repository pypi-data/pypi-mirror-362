#!/usr/bin/env python3
"""
Robot Models and Forward Kinematics Demo for robotics-numpy

This example demonstrates the DH robot modeling and forward kinematics
functionality implemented in Phase 2 of robotics-numpy.

Features demonstrated:
- Creating robots using DH parameters
- Forward kinematics computation
- Stanford Arm robot model
- Custom robot creation
- Performance analysis

Run this example:
    python examples/robot_models_demo.py
"""

import numpy as np
import sys
import os
import time

# Add the src directory to the path so we can import robotics_numpy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import robotics_numpy as rn
from robotics_numpy.models import Stanford, DHRobot, RevoluteDH, PrismaticDH
from robotics_numpy.kinematics import fkine_performance_test


def demo_stanford_arm():
    """Demonstrate Stanford Arm robot model."""
    print("=" * 70)
    print("Stanford Arm Robot Model")
    print("=" * 70)

    # Create Stanford Arm
    robot = Stanford()
    print(robot)

    print("\n📊 Robot Properties:")
    print(f"  Number of joints: {robot.n}")
    print(f"  Joint types: {robot.joint_types}")
    print(f"  Has spherical wrist: {robot.isspherical()}")
    print(f"  Workspace volume: {robot.workspace_volume():.3f} m³")

    print("\n🔧 Standard Configurations:")
    configs = ["qr", "qz", "qextended", "qfolded"]

    for config_name in configs:
        q = getattr(robot, config_name)
        T = robot.fkine(q)

        print(f"\n  Configuration '{config_name}':")
        print(f"    Joint values: {q}")
        print(f"    End-effector position: [{T.t[0]:.3f}, {T.t[1]:.3f}, {T.t[2]:.3f}]")
        print(f"    End-effector orientation (RPY): [{np.degrees(T.rpy()[0]):.1f}°, {np.degrees(T.rpy()[1]):.1f}°, {np.degrees(T.rpy()[2]):.1f}°]")

        # Check singularity
        if robot.is_singular(q):
            print(f"    ⚠️  SINGULAR configuration!")
        else:
            print(f"    ✅ Valid configuration")


def demo_forward_kinematics():
    """Demonstrate forward kinematics computation."""
    print("\n" + "=" * 70)
    print("Forward Kinematics Computation")
    print("=" * 70)

    # Create Stanford Arm
    robot = Stanford()

    print("\n🎯 Single Forward Kinematics:")
    q = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]  # Random configuration
    print(f"Joint configuration: {q}")

    # Forward kinematics
    T = robot.fkine(q)
    print(f"End-effector transformation:\n{T}")

    print("\n🔄 All Link Poses:")
    poses = robot.fkine_all(q)

    for i, pose in enumerate(poses):
        print(f"  Link {i}: position = [{pose.t[0]:.3f}, {pose.t[1]:.3f}, {pose.t[2]:.3f}]")

    print("\n📏 Partial Chain Kinematics:")
    # First 3 links only
    T_partial = robot.fkine(q, end=2)
    print(f"First 3 links end pose: {T_partial.t}")

    # Last 3 links (wrist)
    T_wrist = robot.fkine(q, start=3)
    print(f"Wrist transformation: {T_wrist.t}")


def demo_custom_robots():
    """Demonstrate creating custom robots."""
    print("\n" + "=" * 70)
    print("Custom Robot Creation")
    print("=" * 70)

    print("\n🤖 Simple 3-DOF Planar Arm:")

    # Create a simple 3-DOF planar arm
    links = [
        RevoluteDH(d=0, a=0.3, alpha=0, qlim=[-np.pi, np.pi]),
        RevoluteDH(d=0, a=0.25, alpha=0, qlim=[-np.pi, np.pi]),
        RevoluteDH(d=0, a=0.15, alpha=0, qlim=[-np.pi, np.pi])
    ]

    planar_robot = DHRobot(links, name="3DOF Planar Arm")
    print(planar_robot)

    # Test configurations
    configurations = {
        "straight": [0, 0, 0],
        "elbow_up": [0, np.pi/4, -np.pi/2],
        "elbow_down": [0, -np.pi/4, np.pi/2],
        "folded": [0, np.pi/2, -np.pi],
    }

    print(f"\n📐 Planar Arm Configurations:")
    for name, q in configurations.items():
        T = planar_robot.fkine(q)
        reach = np.linalg.norm(T.t[:2])  # Distance in X-Y plane
        print(f"  {name:12s}: reach = {reach:.3f}m, height = {T.t[2]:.3f}m")

    print("\n🦾 6-DOF Articulated Arm:")

    # Create a 6-DOF articulated arm
    links_6dof = [
        RevoluteDH(d=0.15, a=0, alpha=np.pi/2, qlim=[-np.pi, np.pi]),      # Base
        RevoluteDH(d=0, a=0.4, alpha=0, qlim=[-np.pi/2, np.pi/2]),         # Shoulder
        RevoluteDH(d=0, a=0.3, alpha=0, qlim=[-np.pi, np.pi]),             # Elbow
        RevoluteDH(d=0.1, a=0, alpha=np.pi/2, qlim=[-np.pi, np.pi]),       # Wrist 1
        RevoluteDH(d=0.1, a=0, alpha=-np.pi/2, qlim=[-np.pi/2, np.pi/2]),  # Wrist 2
        RevoluteDH(d=0.08, a=0, alpha=0, qlim=[-np.pi, np.pi])             # Wrist 3
    ]

    robot_6dof = DHRobot(links_6dof, name="6DOF Articulated Arm")
    robot_6dof.addconfiguration("qz", np.zeros(6))
    robot_6dof.addconfiguration("qready", [0, -np.pi/6, np.pi/3, 0, np.pi/6, 0])

    print(f"6-DOF Robot: {robot_6dof.n} joints, reach ≈ {0.4 + 0.3 + 0.1 + 0.08:.2f}m")

    # Test reach calculation
    T_ready = robot_6dof.fkine(robot_6dof.qready)
    print(f"Ready position reach: {np.linalg.norm(T_ready.t):.3f}m")


def demo_mixed_joints():
    """Demonstrate robot with mixed revolute and prismatic joints."""
    print("\n" + "=" * 70)
    print("Mixed Joint Types (Revolute + Prismatic)")
    print("=" * 70)

    print("\n🔄+↕️ SCARA-like Robot (RRP):")

    # Create SCARA-like robot: two revolute joints + one prismatic
    scara_links = [
        RevoluteDH(d=0.1, a=0.25, alpha=0, qlim=[-np.pi, np.pi]),
        RevoluteDH(d=0, a=0.2, alpha=0, qlim=[-np.pi, np.pi]),
        PrismaticDH(theta=0, a=0, alpha=0, qlim=[0, 0.2])  # Vertical motion
    ]

    scara = DHRobot(scara_links, name="SCARA-like Robot")
    print(scara)

    # Test different configurations
    test_configs = [
        [0, 0, 0],              # Straight, down
        [np.pi/4, -np.pi/4, 0.1],   # Elbow bent, up
        [np.pi/2, -np.pi/2, 0.15],  # Max reach, mid height
        [np.pi, 0, 0.2],        # Opposite direction, max height
    ]

    print(f"\n📍 SCARA Configurations:")
    for i, q in enumerate(test_configs):
        T = scara.fkine(q)
        xy_pos = T.t[:2]
        z_pos = T.t[2]
        reach = np.linalg.norm(xy_pos)

        print(f"  Config {i+1}: XY=({xy_pos[0]:.3f}, {xy_pos[1]:.3f}), Z={z_pos:.3f}, reach={reach:.3f}m")


def demo_performance_analysis():
    """Demonstrate performance analysis of forward kinematics."""
    print("\n" + "=" * 70)
    print("Forward Kinematics Performance Analysis")
    print("=" * 70)

    # Test different robot sizes
    robots = {
        "3-DOF Planar": rn.models.create_planar_arm(3),
        "6-DOF Simple": rn.models.create_simple_arm(6),
        "Stanford Arm": Stanford(),
    }

    print(f"\n⚡ Performance Benchmarks ({10000} iterations each):")
    print(f"{'Robot':<15} {'Mean Time':<12} {'Std Dev':<12} {'Target Met':<12}")
    print("-" * 55)

    for name, robot in robots.items():
        stats = fkine_performance_test(robot.links, n_iterations=10000)
        mean_time = stats['mean_time_us']
        std_time = stats['std_time_us']

        # Target: < 10 μs for forward kinematics
        target_met = "✅ Yes" if mean_time < 10.0 else "❌ No"

        print(f"{name:<15} {mean_time:>8.2f} μs   {std_time:>8.2f} μs   {target_met}")

    print(f"\n🎯 Performance Targets:")
    print(f"  Forward kinematics: < 10 μs per computation")
    print(f"  Batch operations: Linear scaling")
    print(f"  Memory usage: Minimal overhead")


def demo_workspace_analysis():
    """Demonstrate workspace analysis."""
    print("\n" + "=" * 70)
    print("Robot Workspace Analysis")
    print("=" * 70)

    # Create Stanford Arm
    stanford = Stanford()

    print(f"\n🌐 Stanford Arm Workspace:")

    # Test reachability of various points
    test_points = [
        ([0.5, 0, 0.5], "Front position"),
        ([0, 0.5, 0.5], "Side position"),
        ([0, 0, 1.0], "Overhead position"),
        ([0.8, 0, 0.3], "Extended front"),
        ([0.1, 0.1, 0.2], "Close position"),
        ([1.5, 0, 0], "Far position"),
        ([0, 0, -0.2], "Below base"),
    ]

    print(f"Reachability test:")
    for point, description in test_points:
        reachable = stanford.reach(np.array(point))
        status = "✅ Reachable" if reachable else "❌ Not reachable"
        print(f"  {description:<18}: {point} -> {status}")

    # Sample workspace
    print(f"\n📊 Workspace Sampling (random configurations):")
    n_samples = 1000
    positions = []

    for _ in range(n_samples):
        # Generate random valid configuration
        q = np.zeros(6)
        for i, link in enumerate(stanford.links):
            if link.qlim:
                qmin, qmax = link.qlim
                q[i] = np.random.uniform(qmin, qmax)

        T = stanford.fkine(q)
        positions.append(T.t)

    positions = np.array(positions)

    # Workspace statistics
    print(f"  Samples: {n_samples}")
    print(f"  X range: [{positions[:, 0].min():.3f}, {positions[:, 0].max():.3f}] m")
    print(f"  Y range: [{positions[:, 1].min():.3f}, {positions[:, 1].max():.3f}] m")
    print(f"  Z range: [{positions[:, 2].min():.3f}, {positions[:, 2].max():.3f}] m")
    print(f"  Max reach: {np.max(np.linalg.norm(positions, axis=1)):.3f} m")
    print(f"  Min reach: {np.min(np.linalg.norm(positions, axis=1)):.3f} m")


def main():
    """Run all robot modeling demonstrations."""
    print("Robotics NumPy - Robot Models and Forward Kinematics Demo")
    print("=" * 70)
    print(f"Phase 2 Implementation: DH Parameters and Forward Kinematics")
    print(f"Created by: robotics-numpy team")
    print(f"Version: 0.2.0-dev")

    try:
        demo_stanford_arm()
        demo_forward_kinematics()
        demo_custom_robots()
        demo_mixed_joints()
        demo_performance_analysis()
        demo_workspace_analysis()

        print("\n" + "=" * 70)
        print("🎉 All Demonstrations Completed Successfully!")
        print("=" * 70)
        print("\n✨ Key Features Demonstrated:")
        print("  ✅ DH parameter robot modeling")
        print("  ✅ Forward kinematics computation")
        print("  ✅ Stanford Arm implementation")
        print("  ✅ Custom robot creation")
        print("  ✅ Mixed joint types (revolute + prismatic)")
        print("  ✅ Performance benchmarking")
        print("  ✅ Workspace analysis")
        print("\n🚀 Next Steps:")
        print("  • Try creating your own robot models")
        print("  • Experiment with different DH parameters")
        print("  • Test performance with larger robots")
        print("  • Explore the visualization capabilities (coming soon)")
        print("  • Check out inverse kinematics (Phase 2.1)")

    except Exception as e:
        print(f"\n❌ Error running demo: {e}")
        print("\nMake sure you have installed robotics-numpy correctly:")
        print("  uv sync")
        print("  uv run python examples/robot_models_demo.py")
        raise


if __name__ == "__main__":
    main()
