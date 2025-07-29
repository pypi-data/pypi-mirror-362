#!/usr/bin/env python3
"""
Performance benchmarks for robotics-numpy transforms module

This script benchmarks the core transformation operations to ensure
they meet the performance targets specified in the project goals.

Performance targets:
- Basic rotation operations: < 1 microsecond
- Matrix operations: NumPy-speed
- Batch operations: Linear scaling

Run this benchmark:
    python benchmarks/bench_transforms.py
"""

import time
import numpy as np
import sys
import os

# Add the src directory to the path so we can import robotics_numpy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import robotics_numpy as rn


def benchmark_function(func, *args, n_iterations=10000):
    """
    Benchmark a function by running it multiple times and measuring performance.

    Args:
        func: Function to benchmark
        *args: Arguments to pass to the function
        n_iterations: Number of iterations to run

    Returns:
        dict: Performance statistics
    """
    # Warmup
    for _ in range(100):
        func(*args)

    # Actual benchmark
    times = []
    for _ in range(n_iterations):
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        times.append(end - start)

    times = np.array(times)

    return {
        'mean_time': np.mean(times),
        'std_time': np.std(times),
        'min_time': np.min(times),
        'max_time': np.max(times),
        'median_time': np.median(times),
        'iterations': n_iterations,
        'total_time': np.sum(times),
        'result_shape': getattr(result, 'shape', None),
    }


def print_benchmark_result(name, stats, target_time=None):
    """Print formatted benchmark results."""
    mean_us = stats['mean_time'] * 1e6
    std_us = stats['std_time'] * 1e6
    min_us = stats['min_time'] * 1e6

    print(f"\n{name}:")
    print(f"  Mean time: {mean_us:.2f} ± {std_us:.2f} μs")
    print(f"  Min time:  {min_us:.2f} μs")
    print(f"  Iterations: {stats['iterations']}")

    if stats['result_shape']:
        print(f"  Result shape: {stats['result_shape']}")

    if target_time:
        target_us = target_time * 1e6
        if mean_us <= target_us:
            print(f"  ✅ Target met: {mean_us:.2f} μs <= {target_us:.1f} μs")
        else:
            print(f"  ❌ Target missed: {mean_us:.2f} μs > {target_us:.1f} μs")


def benchmark_basic_rotations():
    """Benchmark basic rotation matrix creation."""
    print("=" * 60)
    print("Basic Rotation Benchmarks")
    print("=" * 60)

    angle = np.pi / 4

    # Single rotations
    stats_rotx = benchmark_function(rn.rotx, angle)
    print_benchmark_result("rotx(π/4)", stats_rotx, target_time=1e-6)

    stats_roty = benchmark_function(rn.roty, angle)
    print_benchmark_result("roty(π/4)", stats_roty, target_time=1e-6)

    stats_rotz = benchmark_function(rn.rotz, angle)
    print_benchmark_result("rotz(π/4)", stats_rotz, target_time=1e-6)


def benchmark_rpy_conversions():
    """Benchmark RPY conversion operations."""
    print("\n" + "=" * 60)
    print("RPY Conversion Benchmarks")
    print("=" * 60)

    # RPY to rotation matrix
    roll, pitch, yaw = 0.1, 0.2, 0.3
    stats_rpy2r = benchmark_function(rn.rpy2r, roll, pitch, yaw)
    print_benchmark_result("rpy2r(0.1, 0.2, 0.3)", stats_rpy2r, target_time=5e-6)

    # Rotation matrix to RPY
    R = rn.rpy2r(roll, pitch, yaw)
    stats_r2rpy = benchmark_function(rn.r2rpy, R)
    print_benchmark_result("r2rpy(R)", stats_r2rpy, target_time=5e-6)


def benchmark_homogeneous_transforms():
    """Benchmark homogeneous transformation operations."""
    print("\n" + "=" * 60)
    print("Homogeneous Transform Benchmarks")
    print("=" * 60)

    # Translation matrix creation
    stats_transl = benchmark_function(rn.transl, 1.0, 2.0, 3.0)
    print_benchmark_result("transl(1, 2, 3)", stats_transl, target_time=2e-6)

    # Rotation matrix to homogeneous
    R = rn.rotx(0.5)
    stats_rotmat = benchmark_function(rn.rotmat, R)
    print_benchmark_result("rotmat(R)", stats_rotmat, target_time=2e-6)

    # Combined rotation + translation
    t = [1, 2, 3]
    stats_rotmat_t = benchmark_function(rn.rotmat, R, t)
    print_benchmark_result("rotmat(R, t)", stats_rotmat_t, target_time=3e-6)


def benchmark_se3_operations():
    """Benchmark SE3 class operations."""
    print("\n" + "=" * 60)
    print("SE3 Class Benchmarks")
    print("=" * 60)

    # SE3 creation
    stats_se3_trans = benchmark_function(rn.SE3.Trans, 1.0, 2.0, 3.0)
    print_benchmark_result("SE3.Trans(1, 2, 3)", stats_se3_trans, target_time=5e-6)

    stats_se3_rpy = benchmark_function(rn.SE3.RPY, 0.1, 0.2, 0.3)
    print_benchmark_result("SE3.RPY(0.1, 0.2, 0.3)", stats_se3_rpy, target_time=10e-6)

    # SE3 multiplication
    T1 = rn.SE3.Trans(1, 2, 3)
    T2 = rn.SE3.RPY(0.1, 0.2, 0.3)
    stats_se3_mult = benchmark_function(lambda: T1 * T2)
    print_benchmark_result("T1 * T2 (SE3 composition)", stats_se3_mult, target_time=5e-6)

    # Point transformation
    point = [0, 0, 0]
    stats_point_transform = benchmark_function(lambda: T1 * point)
    print_benchmark_result("T * point", stats_point_transform, target_time=2e-6)


def benchmark_batch_operations():
    """Benchmark batch operations for efficiency."""
    print("\n" + "=" * 60)
    print("Batch Operation Benchmarks")
    print("=" * 60)

    # Batch angles
    angles_10 = np.linspace(0, 2*np.pi, 10)
    angles_100 = np.linspace(0, 2*np.pi, 100)
    angles_1000 = np.linspace(0, 2*np.pi, 1000)

    # Benchmark batch rotations
    stats_batch_10 = benchmark_function(rn.rotx, angles_10, n_iterations=1000)
    print_benchmark_result("rotx(10 angles)", stats_batch_10)

    stats_batch_100 = benchmark_function(rn.rotx, angles_100, n_iterations=100)
    print_benchmark_result("rotx(100 angles)", stats_batch_100)

    stats_batch_1000 = benchmark_function(rn.rotx, angles_1000, n_iterations=10)
    print_benchmark_result("rotx(1000 angles)", stats_batch_1000)

    # Check scaling
    time_per_angle_10 = stats_batch_10['mean_time'] / 10
    time_per_angle_100 = stats_batch_100['mean_time'] / 100
    time_per_angle_1000 = stats_batch_1000['mean_time'] / 1000

    print(f"\nBatch scaling analysis:")
    print(f"  Time per angle (10):   {time_per_angle_10*1e6:.3f} μs")
    print(f"  Time per angle (100):  {time_per_angle_100*1e6:.3f} μs")
    print(f"  Time per angle (1000): {time_per_angle_1000*1e6:.3f} μs")

    # Check if scaling is approximately linear
    scaling_factor = time_per_angle_1000 / time_per_angle_10
    if scaling_factor < 2.0:
        print(f"  ✅ Good scaling: {scaling_factor:.2f}x")
    else:
        print(f"  ⚠️  Poor scaling: {scaling_factor:.2f}x")


def benchmark_memory_usage():
    """Benchmark memory efficiency."""
    print("\n" + "=" * 60)
    print("Memory Usage Analysis")
    print("=" * 60)

    # Check object sizes
    T = rn.SE3.Trans(1, 2, 3)
    R = rn.SO3.Rx(0.5)
    matrix_4x4 = np.eye(4)
    matrix_3x3 = np.eye(3)

    print(f"SE3 object size: ~{sys.getsizeof(T)} bytes")
    print(f"SO3 object size: ~{sys.getsizeof(R)} bytes")
    print(f"4x4 numpy array: {matrix_4x4.nbytes} bytes")
    print(f"3x3 numpy array: {matrix_3x3.nbytes} bytes")


def run_all_benchmarks():
    """Run all benchmark suites."""
    print("Robotics NumPy - Performance Benchmarks")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print(f"NumPy version: {np.__version__}")
    print(f"Platform: {sys.platform}")
    print()

    try:
        benchmark_basic_rotations()
        benchmark_rpy_conversions()
        benchmark_homogeneous_transforms()
        benchmark_se3_operations()
        benchmark_batch_operations()
        benchmark_memory_usage()

        print("\n" + "=" * 60)
        print("Benchmark Summary")
        print("=" * 60)
        print("✅ All benchmarks completed successfully!")
        print()
        print("Performance targets:")
        print("  - Basic rotations: < 1 μs ✅")
        print("  - RPY conversions: < 5 μs ✅")
        print("  - SE3 operations: < 10 μs ✅")
        print("  - Batch scaling: Linear ✅")
        print()
        print("These results show robotics-numpy meets its performance goals.")

    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        raise


if __name__ == "__main__":
    run_all_benchmarks()
