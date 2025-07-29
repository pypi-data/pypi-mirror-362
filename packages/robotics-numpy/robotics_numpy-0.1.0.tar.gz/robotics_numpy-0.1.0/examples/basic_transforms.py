#!/usr/bin/env python3
"""
Basic Transforms Example for robotics-numpy

This example demonstrates the core transformation functionality of robotics-numpy,
including rotations, translations, and pose compositions.

Run this example:
    python examples/basic_transforms.py
"""

import numpy as np
import sys
import os

# Add the src directory to the path so we can import robotics_numpy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import robotics_numpy as rn
from robotics_numpy.transforms import is_rotation_matrix


def demo_basic_rotations():
    """Demonstrate basic rotation matrices."""
    print("=" * 60)
    print("Basic Rotation Matrices")
    print("=" * 60)

    # Single-axis rotations
    print("\n1. Single-axis rotations:")
    print("-" * 30)

    angle = np.pi / 4  # 45 degrees

    Rx = rn.rotx(angle)
    Ry = rn.roty(angle)
    Rz = rn.rotz(angle)

    print(f"Rotation about X-axis ({angle:.3f} rad = {np.degrees(angle):.1f}°):")
    print(Rx)
    print(f"\nRotation about Y-axis ({angle:.3f} rad = {np.degrees(angle):.1f}°):")
    print(Ry)
    print(f"\nRotation about Z-axis ({angle:.3f} rad = {np.degrees(angle):.1f}°):")
    print(Rz)

    # Verify orthogonality
    print(f"\nVerification - R @ R.T should be identity:")
    print(f"Rx @ Rx.T:\n{Rx @ Rx.T}")
    print(f"Determinant of Rx: {np.linalg.det(Rx):.6f} (should be 1.0)")


def demo_rpy_conversions():
    """Demonstrate roll-pitch-yaw conversions."""
    print("\n" + "=" * 60)
    print("Roll-Pitch-Yaw Conversions")
    print("=" * 60)

    # Define RPY angles
    roll = 0.1    # 5.7 degrees
    pitch = 0.2   # 11.5 degrees
    yaw = 0.3     # 17.2 degrees

    print(f"\nOriginal RPY angles:")
    print(f"Roll:  {roll:.3f} rad = {np.degrees(roll):.1f}°")
    print(f"Pitch: {pitch:.3f} rad = {np.degrees(pitch):.1f}°")
    print(f"Yaw:   {yaw:.3f} rad = {np.degrees(yaw):.1f}°")

    # Convert to rotation matrix
    R = rn.rpy2r(roll, pitch, yaw)
    print(f"\nRotation matrix from RPY:")
    print(R)

    # Convert back to RPY
    roll_back, pitch_back, yaw_back = rn.r2rpy(R)
    print(f"\nConverted back to RPY:")
    print(f"Roll:  {roll_back:.3f} rad = {np.degrees(roll_back):.1f}°")
    print(f"Pitch: {pitch_back:.3f} rad = {np.degrees(pitch_back):.1f}°")
    print(f"Yaw:   {yaw_back:.3f} rad = {np.degrees(yaw_back):.1f}°")

    # Check roundtrip accuracy
    rpy_error = np.array([roll_back - roll, pitch_back - pitch, yaw_back - yaw])
    print(f"\nRoundtrip error: {np.linalg.norm(rpy_error):.2e} rad")


def demo_homogeneous_transforms():
    """Demonstrate homogeneous transformation matrices."""
    print("\n" + "=" * 60)
    print("Homogeneous Transformation Matrices")
    print("=" * 60)

    # Pure translation
    print("\n1. Pure translation:")
    print("-" * 25)
    T_trans = rn.transl(1, 2, 3)
    print(f"Translation by [1, 2, 3]:")
    print(T_trans)

    # Pure rotation
    print("\n2. Pure rotation:")
    print("-" * 20)
    R = rn.rotx(np.pi/2)
    T_rot = rn.rotmat(R)
    print(f"Rotation about X-axis (90°):")
    print(T_rot)

    # Combined transformation
    print("\n3. Combined transformation:")
    print("-" * 30)
    T_combined = rn.rotmat(R, [1, 2, 3])
    print(f"Rotation + Translation:")
    print(T_combined)

    # Transformation composition
    print("\n4. Transformation composition:")
    print("-" * 35)
    T1 = rn.transl(1, 0, 0)  # Move 1 unit in X
    T2 = rn.rotmat(rn.rotz(np.pi/2))  # Rotate 90° about Z
    T3 = rn.transl(0, 1, 0)  # Move 1 unit in Y

    T_final = T1 @ T2 @ T3
    print(f"T1 (translate X) @ T2 (rotate Z) @ T3 (translate Y):")
    print(T_final)

    # Transform a point using SE3 class
    T_final_se3 = rn.SE3(T_final)
    point = np.array([0, 0, 0])
    point_transformed = T_final_se3 * point
    print(f"\nTransforming point {point} with T_final:")
    print(f"Result: {point_transformed}")


def demo_so3_class():
    """Demonstrate SO3 class usage."""
    print("\n" + "=" * 60)
    print("SO3 Class - Object-Oriented Rotations")
    print("=" * 60)

    # Create rotations using class methods
    print("\n1. Creating SO3 rotations:")
    print("-" * 30)

    R1 = rn.SO3.Rx(np.pi/4)
    R2 = rn.SO3.RPY(0.1, 0.2, 0.3)
    R3 = rn.SO3.Quaternion([0.924, 0.383, 0, 0])  # ~45° about X

    print(f"R1 (X-axis rotation): {R1}")
    print(f"R2 (from RPY): {R2}")
    print(f"R3 (from quaternion): {R3}")

    # Rotation composition
    print("\n2. Rotation composition:")
    print("-" * 28)
    R_composed = R1 * R2
    print(f"R1 * R2 = {R_composed}")

    # Rotation inverse
    print("\n3. Rotation inverse:")
    print("-" * 23)
    R_inv = R1.inv()
    R_identity = R1 * R_inv
    print(f"R1.inv() = {R_inv}")
    print(f"R1 * R1.inv() (should be identity):")
    print(R_identity.matrix)

    # Rotate vectors
    print("\n4. Rotating vectors:")
    print("-" * 23)
    vector = [1, 0, 0]
    rotated = R1.rotate(vector)
    print(f"Rotating {vector} by R1: {rotated}")


def demo_se3_class():
    """Demonstrate SE3 class usage."""
    print("\n" + "=" * 60)
    print("SE3 Class - Object-Oriented Transformations")
    print("=" * 60)

    # Create transformations
    print("\n1. Creating SE3 transformations:")
    print("-" * 35)

    T1 = rn.SE3.Trans(1, 2, 3)
    T2 = rn.SE3.Rx(np.pi/2)
    T3 = rn.SE3.RPY(0.1, 0.2, 0.3, [1, 2, 3])

    print(f"T1 (translation): {T1}")
    print(f"T2 (X rotation): {T2}")
    print(f"T3 (RPY + translation): {T3}")

    # Access properties
    print("\n2. Accessing transformation components:")
    print("-" * 40)
    print(f"T3 translation: {T3.t}")
    print(f"T3 rotation matrix:\n{T3.R}")
    print(f"T3 RPY angles: {T3.rpy()}")

    # Transform points
    print("\n3. Transforming points:")
    print("-" * 26)

    # Single point
    point = [0, 0, 0]
    transformed_point = T3 * point
    print(f"Transform {point} with T3: {transformed_point}")

    # Multiple points
    points = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    transformed_points = T3 * points
    print(f"\nTransforming multiple points:")
    print(f"Original:\n{points}")
    print(f"Transformed:\n{transformed_points}")

    # Composition
    print("\n4. Transformation composition:")
    print("-" * 35)
    T_composed = T1 * T2 * T3
    print(f"T1 * T2 * T3 = {T_composed}")


def demo_batch_operations():
    """Demonstrate batch operations for efficiency."""
    print("\n" + "=" * 60)
    print("Batch Operations for Efficiency")
    print("=" * 60)

    # Batch rotations
    print("\n1. Batch rotations:")
    print("-" * 22)

    angles = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
    print(f"Angles: {angles}")
    print(f"Angles in degrees: {np.degrees(angles)}")

    # Create batch of rotation matrices
    R_batch = rn.rotx(angles)
    print(f"\nBatch rotation shape: {R_batch.shape}")
    print(f"First rotation (0°):\n{R_batch[0]}")
    print(f"Last rotation (90°):\n{R_batch[-1]}")

    # Verify all are valid rotation matrices
    print("\n2. Validation:")
    print("-" * 15)
    for i, R in enumerate(R_batch):
        valid = is_rotation_matrix(R)
        det = np.linalg.det(R)
        print(f"Rotation {i}: valid={valid}, det={det:.6f}")


def demo_practical_example():
    """Demonstrate a practical robotics example."""
    print("\n" + "=" * 60)
    print("Practical Example: Robot End-Effector Poses")
    print("=" * 60)

    print("\nScenario: Robot picking up objects at different orientations")
    print("-" * 60)

    # Base poses for objects
    object_positions = [
        [0.5, 0.2, 0.1],   # Object 1
        [0.4, -0.3, 0.15], # Object 2
        [0.6, 0.1, 0.05],  # Object 3
    ]

    # Different approach angles
    approach_angles = [
        (0, 0, 0),           # Straight down
        (0, np.pi/6, 0),     # 30° tilt
        (np.pi/4, 0, np.pi/2), # 45° roll + 90° yaw
    ]

    print(f"\nCalculating end-effector poses:")
    print("-" * 35)

    for i, (pos, angles) in enumerate(zip(object_positions, approach_angles)):
        # Create transformation for this object
        T_object = rn.SE3.RPY(*angles, pos)

        # Add approach offset (10cm above object)
        T_approach_offset = rn.SE3.Trans(0, 0, 0.1)
        T_approach = T_object * T_approach_offset

        roll, pitch, yaw = angles
        x, y, z = pos

        print(f"\nObject {i+1}:")
        print(f"  Position: [{x:.1f}, {y:.1f}, {z:.1f}]")
        print(f"  Orientation: R={roll:.2f}, P={pitch:.2f}, Y={yaw:.2f} rad")
        print(f"  Approach pose: {T_approach}")

        # Calculate distance from origin
        distance = np.linalg.norm(T_approach.t)
        print(f"  Distance from base: {distance:.3f} m")


def main():
    """Run all demonstration functions."""
    print("Robotics NumPy - Basic Transforms Demo")
    print("Created by: robotics-numpy team")
    print("Version: 0.1.0")

    try:
        demo_basic_rotations()
        demo_rpy_conversions()
        demo_homogeneous_transforms()
        demo_so3_class()
        demo_se3_class()
        demo_batch_operations()
        demo_practical_example()

        print("\n" + "=" * 60)
        print("Demo completed successfully! 🎉")
        print("=" * 60)
        print("\nNext steps:")
        print("- Try modifying the examples above")
        print("- Explore the API documentation")
        print("- Check out more examples in the examples/ directory")
        print("- Star the project on GitHub if you find it useful!")

    except Exception as e:
        print(f"\n❌ Error running demo: {e}")
        print("\nMake sure you have installed robotics-numpy correctly:")
        print("  pip install robotics-numpy")
        raise


if __name__ == "__main__":
    main()
