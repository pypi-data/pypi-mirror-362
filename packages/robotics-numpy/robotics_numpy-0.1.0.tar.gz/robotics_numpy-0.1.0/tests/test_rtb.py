# robotics-numpy/tests/test_rtb.py
import pytest
from re import L
import numpy as np

try:
    import roboticstoolbox as rtb
except ImportError:
    # If roboticstoolbox is not installed, we skip the tests
    # This is useful for environments where roboticstoolbox is not available
    print("Roboticstoolbox not found, skipping tests.")
    rtb = None

from robotics_numpy.models import DHRobot, RevoluteDH, PrismaticDH

# Skip the entire test file if roboticstoolbox is not installed
pytestmark = pytest.mark.skipif(rtb is None, reason="Roboticstoolbox not installed")


def test_robot_comparison():
    # Define the robot using your implementation
    links = [
        RevoluteDH(d=0.1, a=0.2, alpha=0, qlim=[-np.pi, np.pi]),
        PrismaticDH(theta=0, a=0.1, alpha=0, qlim=[0, 0.5]),
    ]
    my_robot = DHRobot(links)

    # Define the same robot using roboticstoolbox-python
    toolbox_robot = rtb.DHRobot(
        [
            rtb.RevoluteDH(d=0.1, a=0.2, alpha=0, qlim=[-np.pi, np.pi]),
            rtb.PrismaticDH(theta=0, a=0.1, alpha=0, qlim=[0, 0.5]),
        ]
    )

    # Test joint limits
    np.testing.assert_allclose(my_robot.qlim, toolbox_robot.qlim, rtol=1e-7, atol=0)

    # Test forward kinematics
    q = [np.pi / 4, 0.3]  # Example joint configuration
    my_fk = my_robot.fkine(q).matrix  # Convert SE3 object to numpy array
    print(f"My robot forward kinematics output (as array): {my_fk}")
    toolbox_fk = toolbox_robot.fkine(q)
    print(f"Robotics Toolbox forward kinematics output: {toolbox_fk.A}")

    # Compare forward kinematics results
    np.testing.assert_allclose(my_fk, toolbox_fk.A, rtol=1e-7, atol=1e-7)

    print("All tests passed!")


def test_robot_jacobian():
    # Define the robot using your implementation
    links = [
        RevoluteDH(d=0.1, a=0.2, alpha=0, qlim=[-np.pi, np.pi]),
        PrismaticDH(theta=0, a=0.1, alpha=0, qlim=[0, 0.5]),
    ]
    my_robot = DHRobot(links)

    # Define the same robot using roboticstoolbox-python
    toolbox_robot = rtb.DHRobot(
        [
            rtb.RevoluteDH(d=0.1, a=0.2, alpha=0, qlim=[-np.pi, np.pi]),
            rtb.PrismaticDH(theta=0, a=0.1, alpha=0, qlim=[0, 0.5]),
        ]
    )

    # Test Jacobian
    q = [np.pi / 4, 0.3]  # Example joint configuration
    my_jacobian = my_robot.jacob0(q)
    toolbox_jacobian = toolbox_robot.jacob0(q)

    print(f"My robot Jacobian output:\n{my_jacobian}")
    print(f"Robotics Toolbox Jacobian output:\n{toolbox_jacobian}")

    # Compare Jacobian results
    np.testing.assert_allclose(my_jacobian, toolbox_jacobian, rtol=1e-7, atol=1e-7)


def test_ur5_manipulability():
    from robotics_numpy.models import Generic

    q = np.random.uniform(-np.pi, np.pi, 6)  # Random joint configuration for UR5
    ur5 = Generic(
        dofs=6,
        a=[0, -0.42500, -0.39225, 0, 0, 0],
        d=[0.089459, 0, 0, 0.10915, 0.09465, 0.0823],
        alpha=[np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2, 0],
        # offset=[0, -np.pi / 2, 0, 0],
        # qlim=[[-np.pi, np.pi], [-np.pi / 2, np.pi / 2],
        #       [-np.pi / 3, np.pi / 3], [-np.pi / 6, np.pi / 6],
        #       [-np.pi / 4, np.pi / 4], [-np.pi / 4, np.pi / 4]],
        name="UR5",
    )
    G = ur5.manipulability(q=q, method="yoshikawa")

    print(f"UR5 Manipulability: {G}")

    ur5_rtb = rtb.models.DH.UR5()
    G_rtb = ur5_rtb.manipulability(q=q, method="yoshikawa")
    print(f"Robotics Toolbox UR5 Manipulability: {G_rtb}")
    # Compare manipulability results
    np.testing.assert_allclose(G, G_rtb, rtol=1e-7, atol=1e-7)


if __name__ == "__main__":
    # test_robot_comparison()
    # test_robot_jacobian()
    test_ur5_manipulability()
