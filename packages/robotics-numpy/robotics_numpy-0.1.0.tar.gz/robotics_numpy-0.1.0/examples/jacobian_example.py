#!/usr/bin/env python3
"""
Jacobian and Manipulability Example

This example demonstrates the computation of manipulator Jacobians
and manipulability measures using the robotics-numpy library.

Features demonstrated:
- Computing Jacobians in base frame (jacob0)
- Computing Jacobians in end-effector frame (jacobe)
- Calculating manipulability with different methods
- Analyzing manipulability for different subsets of DOFs
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Ellipse

from robotics_numpy.models import Stanford, create_simple_arm
from robotics_numpy.kinematics import jacobe, joint_velocity_ellipsoid


def main():
    """Main function for Jacobian and manipulability examples."""
    print("Jacobian and Manipulability Example")
    print("===================================")
    print()

    # Create a Stanford arm robot
    robot = Stanford()
    print(f"Created robot: {robot.name}")
    print()

    # Define joint configurations to test
    q_zero = np.zeros(robot.n)
    q_stretched = np.array([0, 0, 0.5, 0, 0, 0])  # Extended prismatic joint
    q_bent = np.array([np.pi / 4, np.pi / 4, 0.3, np.pi / 4, np.pi / 4, np.pi / 4])

    # Compute and display Jacobian at zero configuration
    print("Computing Jacobians...")
    print("-" * 50)
    J0 = robot.jacob0(q_zero)
    Je = jacobe(robot, q_zero)

    print(f"Jacobian in base frame (shape {J0.shape}):")
    print(np.round(J0, 3))
    print()

    print(f"Jacobian in end-effector frame (shape {Je.shape}):")
    print(np.round(Je, 3))
    print()

    # Compute manipulability for different configurations
    print("Computing Manipulability...")
    print("-" * 50)

    # Configurations to test
    configs = {"Zero": q_zero, "Stretched": q_stretched, "Bent": q_bent}

    # Methods to test
    methods = ["yoshikawa", "invcondition", "minsingular"]

    # Axes to test
    axes_options = ["all", "trans", "rot"]

    # Compute and display manipulability for all combinations
    print("Configuration | Method      | Axes  | Value")
    print("-" * 50)

    for config_name, q in configs.items():
        for method in methods:
            for axes in axes_options:
                m = robot.manipulability(q, method=method, axes=axes)
                print(f"{config_name:12} | {method:12} | {axes:5} | {m:.6f}")

    print()

    # Demonstrate manipulability visualization for one configuration
    visualize_manipulability(robot, q_bent)


def visualize_manipulability(robot, q):
    """
    Visualize manipulability ellipsoid for translational DOFs.

    Args:
        robot: Robot model
        q: Joint configuration
    """
    try:
        # Compute Jacobian
        J = robot.jacob0(q)

        # Get translational Jacobian (first 3 rows)
        J_trans = J[:3, :]

        # Compute the manipulability ellipsoid
        eigvals, eigvecs = joint_velocity_ellipsoid(J_trans)

        # Sort eigenvalues and eigenvectors
        idx = eigvals.argsort()[::-1]
        eigvals = eigvals[idx]
        eigvecs = eigvecs[:, idx]

        # Create figure
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection="3d")

        # Plot robot base
        ax.scatter([0], [0], [0], color="red", s=100, marker="o", label="Robot Base")

        # Plot end-effector position
        T = robot.fkine(q)
        ee_pos = T.t
        ax.scatter(
            [ee_pos[0]],
            [ee_pos[1]],
            [ee_pos[2]],
            color="blue",
            s=100,
            marker="o",
            label="End-effector",
        )

        # Plot manipulability ellipsoid at end-effector
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        # Scale factor for visualization
        scale = 0.2

        # Generate ellipsoid points
        x = scale * np.sqrt(eigvals[0]) * np.outer(np.cos(u), np.sin(v))
        y = scale * np.sqrt(eigvals[1]) * np.outer(np.sin(u), np.sin(v))
        z = scale * np.sqrt(eigvals[2]) * np.outer(np.ones_like(u), np.cos(v))

        # Apply rotation from eigenvectors and translate to end-effector
        for i in range(len(u)):
            for j in range(len(v)):
                point = np.array([x[i, j], y[i, j], z[i, j]])
                rotated = eigvecs @ point
                x[i, j] = rotated[0] + ee_pos[0]
                y[i, j] = rotated[1] + ee_pos[1]
                z[i, j] = rotated[2] + ee_pos[2]

        # Plot ellipsoid
        ax.plot_surface(x, y, z, color="cyan", alpha=0.3)

        # Plot ellipsoid principal axes
        for i in range(3):
            ax.quiver(
                ee_pos[0],
                ee_pos[1],
                ee_pos[2],
                scale * np.sqrt(eigvals[i]) * eigvecs[0, i],
                scale * np.sqrt(eigvals[i]) * eigvecs[1, i],
                scale * np.sqrt(eigvals[i]) * eigvecs[2, i],
                color=["r", "g", "b"][i],
                linewidth=2,
            )

        # Configure plot
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("Translational Manipulability Ellipsoid")

        # Make axis limits equal for better visualization
        max_range = max(
            [
                np.max(np.abs(x.flatten())),
                np.max(np.abs(y.flatten())),
                np.max(np.abs(z.flatten())),
            ]
        )

        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range, max_range])

        plt.legend()
        plt.tight_layout()

        print("Translational manipulability ellipsoid visualization:")
        print(f"Principal axes lengths: {np.sqrt(eigvals)}")

        plt.show()

    except ImportError:
        print("Could not create visualization. Make sure matplotlib is installed.")


def compare_robot_designs():
    """Compare manipulability of different robot designs."""
    print("\nComparing Manipulability of Different Robot Designs")
    print("-" * 50)

    # Create different robot designs
    stanford = Stanford()
    arm6r = create_simple_arm(n_joints=6)

    # Define standard test configuration
    q_stanford = np.zeros(stanford.n)
    q_arm6r = np.zeros(arm6r.n)

    # Compare manipulability
    print("Robot         | Trans Manip | Rot Manip  | Combined")
    print("-" * 50)

    m_stanford_trans = stanford.manipulability(q_stanford, axes="trans")
    m_stanford_rot = stanford.manipulability(q_stanford, axes="rot")
    m_stanford_all = stanford.manipulability(q_stanford, axes="all")

    m_arm6r_trans = arm6r.manipulability(q_arm6r, axes="trans")
    m_arm6r_rot = arm6r.manipulability(q_arm6r, axes="rot")
    m_arm6r_all = arm6r.manipulability(q_arm6r, axes="all")

    print(
        f"Stanford Arm  | {m_stanford_trans:.6f} | {m_stanford_rot:.6f} | {m_stanford_all:.6f}"
    )
    print(
        f"6R Simple Arm | {m_arm6r_trans:.6f} | {m_arm6r_rot:.6f} | {m_arm6r_all:.6f}"
    )


if __name__ == "__main__":
    main()
    compare_robot_designs()
