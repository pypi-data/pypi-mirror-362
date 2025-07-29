import time
import numpy as np
import pytest

try:
    import roboticstoolbox as rtb
except ImportError:
    # If roboticstoolbox is not installed, we skip the tests
    # This is useful for environments where roboticstoolbox is not available
    rtb = None
from robotics_numpy.models import DHRobot, RevoluteDH, PrismaticDH, Generic

# Skip the entire test file if roboticstoolbox is not installed
pytestmark = pytest.mark.skipif(rtb is None, reason="Roboticstoolbox not installed")

# Variables to store performance results
fkine_results = {}
jacobian_results = {}
manipulability_results = {}


def format_time(t):
    """Formats time in seconds, switching to milliseconds if very small."""
    if t < 0.01:  # Threshold for switching to milliseconds
        return f"{t * 1000:.3f} ms"
    else:
        return f"{t:.6f} s"


def format_percentage_diff(diff):
    """Formats percentage difference, handling infinite values."""
    if diff == float("inf"):
        return "N/A"
    return f"{diff:>+14.2f}%"  # Add sign and align


def test_fkine_performance():
    """Tests the performance of forward kinematics calculation."""
    print("\n--- Testing Forward Kinematics Performance ---")

    # --- Simple 2-DOF Robot ---
    print("\nTesting with a simple 2-DOF robot:")
    links_simple = [
        RevoluteDH(d=0.1, a=0.2, alpha=0, qlim=[-np.pi, np.pi]),
        PrismaticDH(theta=0, a=0.1, alpha=0, qlim=[0, 0.5]),
    ]
    my_robot_simple = DHRobot(links_simple)
    toolbox_robot_simple = rtb.DHRobot(
        [
            rtb.RevoluteDH(d=0.1, a=0.2, alpha=0, qlim=[-np.pi, np.pi]),
            rtb.PrismaticDH(theta=0, a=0.1, alpha=0, qlim=[0, 0.5]),
        ]
    )
    q_simple = [np.pi / 4, 0.3]

    num_runs = 1000

    start_time = time.time()
    for _ in range(num_runs):
        my_fk = my_robot_simple.fkine(q_simple).matrix
    my_runtime = (time.time() - start_time) / num_runs
    print(f"  My robot fkine (2-DOF) average runtime: {format_time(my_runtime)}")
    fkine_results["My Robot (2-DOF)"] = my_runtime

    start_time = time.time()
    for _ in range(num_runs):
        toolbox_fk = toolbox_robot_simple.fkine(q_simple)
    toolbox_runtime = (time.time() - start_time) / num_runs
    print(
        f"  Robotics Toolbox fkine (2-DOF) average runtime: {format_time(toolbox_runtime)}"
    )
    fkine_results["Robotics Toolbox (2-DOF)"] = toolbox_runtime

    # Calculate and store percentage difference
    if my_runtime > 0 and toolbox_runtime > 0:
        percentage_diff = ((my_runtime - toolbox_runtime) / toolbox_runtime) * 100
        fkine_results["Percentage Diff (2-DOF)"] = percentage_diff
    else:
        fkine_results["Percentage Diff (2-DOF)"] = float("inf")

    # --- UR5 Robot ---
    print("\nTesting with a UR5 robot (6-DOF):")
    q_ur5 = np.random.uniform(-np.pi, np.pi, 6)
    ur5_my = Generic(
        dofs=6,
        a=[0, -0.42500, -0.39225, 0, 0, 0],
        d=[0.089459, 0, 0, 0.10915, 0.09465, 0.0823],
        alpha=[np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2, 0],
        name="UR5",
    )
    ur5_rtb = rtb.models.DH.UR5()

    start_time = time.time()
    for _ in range(num_runs):
        my_fk_ur5 = ur5_my.fkine(q_ur5).matrix
    my_runtime_ur5 = (time.time() - start_time) / num_runs
    print(f"  My robot fkine (UR5) average runtime: {format_time(my_runtime_ur5)}")
    fkine_results["My Robot (UR5)"] = my_runtime_ur5

    start_time = time.time()
    for _ in range(num_runs):
        toolbox_fk_ur5 = ur5_rtb.fkine(q_ur5)
    toolbox_runtime_ur5 = (time.time() - start_time) / num_runs
    print(
        f"  Robotics Toolbox fkine (UR5) average runtime: {format_time(toolbox_runtime_ur5)}"
    )
    fkine_results["Robotics Toolbox (UR5)"] = toolbox_runtime_ur5

    # Calculate and store percentage difference
    if my_runtime_ur5 > 0 and toolbox_runtime_ur5 > 0:
        percentage_diff_ur5 = (
            (my_runtime_ur5 - toolbox_runtime_ur5) / toolbox_runtime_ur5
        ) * 100
        fkine_results["Percentage Diff (UR5)"] = percentage_diff_ur5
    else:
        fkine_results["Percentage Diff (UR5)"] = float("inf")


def test_jacobian_performance():
    """Tests the performance of Jacobian matrix calculation."""
    print("\n--- Testing Jacobian Performance ---")

    # --- Simple 2-DOF Robot ---
    print("\nTesting with a simple 2-DOF robot:")
    links_simple = [
        RevoluteDH(d=0.1, a=0.2, alpha=0, qlim=[-np.pi, np.pi]),
        PrismaticDH(theta=0, a=0.1, alpha=0, qlim=[0, 0.5]),
    ]
    my_robot_simple = DHRobot(links_simple)
    toolbox_robot_simple = rtb.DHRobot(
        [
            rtb.RevoluteDH(d=0.1, a=0.2, alpha=0, qlim=[-np.pi, np.pi]),
            rtb.PrismaticDH(theta=0, a=0.1, alpha=0, qlim=[0, 0.5]),
        ]
    )
    q_simple = [np.pi / 4, 0.3]

    num_runs = 1000

    start_time = time.time()
    for _ in range(num_runs):
        my_jacobian = my_robot_simple.jacob0(q_simple)
    my_runtime = (time.time() - start_time) / num_runs
    print(f"  My robot jacob0 (2-DOF) average runtime: {format_time(my_runtime)}")
    jacobian_results["My Robot (2-DOF)"] = my_runtime

    start_time = time.time()
    for _ in range(num_runs):
        toolbox_jacobian = toolbox_robot_simple.jacob0(q_simple)
    toolbox_runtime = (time.time() - start_time) / num_runs
    print(
        f"  Robotics Toolbox jacob0 (2-DOF) average runtime: {format_time(toolbox_runtime)}"
    )
    jacobian_results["Robotics Toolbox (2-DOF)"] = toolbox_runtime

    # Calculate and store percentage difference
    if my_runtime > 0 and toolbox_runtime > 0:
        percentage_diff = ((my_runtime - toolbox_runtime) / toolbox_runtime) * 100
        jacobian_results["Percentage Diff (2-DOF)"] = percentage_diff
    else:
        jacobian_results["Percentage Diff (2-DOF)"] = float("inf")

    # --- UR5 Robot ---
    print("\nTesting with a UR5 robot (6-DOF):")
    q_ur5 = np.random.uniform(-np.pi, np.pi, 6)
    ur5_my = Generic(
        dofs=6,
        a=[0, -0.42500, -0.39225, 0, 0, 0],
        d=[0.089459, 0, 0, 0.10915, 0.09465, 0.0823],
        alpha=[np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2, 0],
        name="UR5",
    )
    ur5_rtb = rtb.models.DH.UR5()

    start_time = time.time()
    for _ in range(num_runs):
        my_jacobian_ur5 = ur5_my.jacob0(q_ur5)
    my_runtime_ur5 = (time.time() - start_time) / num_runs
    print(f"  My robot jacob0 (UR5) average runtime: {format_time(my_runtime_ur5)}")
    jacobian_results["My Robot (UR5)"] = my_runtime_ur5

    start_time = time.time()
    for _ in range(num_runs):
        toolbox_jacobian_ur5 = ur5_rtb.jacob0(q_ur5)
    toolbox_runtime_ur5 = (time.time() - start_time) / num_runs
    print(
        f"  Robotics Toolbox jacob0 (UR5) average runtime: {format_time(toolbox_runtime_ur5)}"
    )
    jacobian_results["Robotics Toolbox (UR5)"] = toolbox_runtime_ur5

    # Calculate and store percentage difference
    if my_runtime_ur5 > 0 and toolbox_runtime_ur5 > 0:
        percentage_diff_ur5 = (
            (my_runtime_ur5 - toolbox_runtime_ur5) / toolbox_runtime_ur5
        ) * 100
        jacobian_results["Percentage Diff (UR5)"] = percentage_diff_ur5
    else:
        jacobian_results["Percentage Diff (UR5)"] = float("inf")


def test_manipulability_performance():
    """Tests the performance of manipulability calculation."""
    print("\n--- Testing Manipulability Performance ---")

    # --- UR5 Robot ---
    print("\nTesting with a UR5 robot (6-DOF):")
    q_ur5 = np.random.uniform(-np.pi, np.pi, 6)
    ur5_my = Generic(
        dofs=6,
        a=[0, -0.42500, -0.39225, 0, 0, 0],
        d=[0.089459, 0, 0, 0.10915, 0.09465, 0.0823],
        alpha=[np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2, 0],
        name="UR5",
    )
    ur5_rtb = rtb.models.DH.UR5()

    num_runs = 100

    start_time = time.time()
    for _ in range(num_runs):
        G_my = ur5_my.manipulability(q=q_ur5, method="yoshikawa")
    my_runtime = (time.time() - start_time) / num_runs
    print(f"  My robot manipulability (UR5) average runtime: {format_time(my_runtime)}")
    manipulability_results["My Robot (UR5)"] = my_runtime

    start_time = time.time()
    for _ in range(num_runs):
        G_rtb = ur5_rtb.manipulability(q=q_ur5, method="yoshikawa")
    toolbox_runtime = (time.time() - start_time) / num_runs
    print(
        f"  Robotics Toolbox manipulability (UR5) average runtime: {format_time(toolbox_runtime)}"
    )
    manipulability_results["Robotics Toolbox (UR5)"] = toolbox_runtime

    # Calculate and store percentage difference
    if my_runtime > 0 and toolbox_runtime > 0:
        percentage_diff = ((my_runtime - toolbox_runtime) / toolbox_runtime) * 100
        manipulability_results["Percentage Diff (UR5)"] = percentage_diff
    else:
        manipulability_results["Percentage Diff (UR5)"] = float("inf")


def print_performance_table():
    """Prints an ASCII table comparing the performance results."""
    print("\n\n" + "=" * 80)
    print("Performance Comparison Table")
    print("=" * 80)

    # Header
    print(
        "| Feature             | robotics-numpy         | rtb                    | Difference (%) |"
    )
    print(
        "|---------------------|------------------------|------------------------|----------------|"
    )

    # FKine results
    my_fk_2dof = fkine_results.get("My Robot (2-DOF)", 0)
    diff_fk_2dof = fkine_results.get("Percentage Diff (2-DOF)", 0)
    rtb_fk_2dof = fkine_results.get("Robotics Toolbox (2-DOF)", 0)
    print(
        f"| Forward Kinematics  | {format_time(my_fk_2dof):<20} | {format_time(rtb_fk_2dof):<22} | {format_percentage_diff(diff_fk_2dof):<14} |"
    )

    my_fk_ur5 = fkine_results.get("My Robot (UR5)", 0)
    diff_fk_ur5 = fkine_results.get("Percentage Diff (UR5)", 0)
    rtb_fk_ur5 = fkine_results.get("Robotics Toolbox (UR5)", 0)
    print(
        f"|                     | {format_time(my_fk_ur5):<20} | {format_time(rtb_fk_ur5):<22} | {format_percentage_diff(diff_fk_ur5):<14} |"
    )

    # Jacobian results
    my_jac_2dof = jacobian_results.get("My Robot (2-DOF)", 0)
    diff_jac_2dof = jacobian_results.get("Percentage Diff (2-DOF)", 0)
    rtb_jac_2dof = jacobian_results.get("Robotics Toolbox (2-DOF)", 0)
    print(
        f"| Jacobian            | {format_time(my_jac_2dof):<20} | {format_time(rtb_jac_2dof):<22} | {format_percentage_diff(diff_jac_2dof):<14} |"
    )

    my_jac_ur5 = jacobian_results.get("My Robot (UR5)", 0)
    diff_jac_ur5 = jacobian_results.get("Percentage Diff (UR5)", 0)
    rtb_jac_ur5 = jacobian_results.get("Robotics Toolbox (UR5)", 0)
    print(
        f"|                     | {format_time(my_jac_ur5):<20} | {format_time(rtb_jac_ur5):<22} | {format_percentage_diff(diff_jac_ur5):<14} |"
    )

    # Manipulability results
    my_manip_ur5 = manipulability_results.get("My Robot (UR5)", 0)
    diff_manip_ur5 = manipulability_results.get("Percentage Diff (UR5)", 0)
    rtb_manip_ur5 = manipulability_results.get("Robotics Toolbox (UR5)", 0)
    print(
        f"| Manipulability      | {format_time(my_manip_ur5):<20} | {format_time(rtb_manip_ur5):<22} | {format_percentage_diff(diff_manip_ur5):<14} |"
    )

    print("=" * 80)


if __name__ == "__main__":
    test_fkine_performance()
    test_jacobian_performance()
    test_manipulability_performance()
    print_performance_table()
