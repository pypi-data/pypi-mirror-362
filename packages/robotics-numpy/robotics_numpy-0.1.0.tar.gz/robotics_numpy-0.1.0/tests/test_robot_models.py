"""
Tests for robot models and forward kinematics in robotics-numpy

This module tests the DH robot modeling functionality including:
- DH link creation and validation
- DHRobot class functionality
- Forward kinematics computation
- Stanford Arm robot model
- Custom robot creation
- Performance requirements
"""

import pytest
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from robotics_numpy.models import (
    DHLink,
    RevoluteDH,
    PrismaticDH,
    DHRobot,
    Stanford,
    Generic,
    dh_check_parameters,
    create_simple_arm,
    create_planar_arm,
    create_generic_robot,
)
from robotics_numpy.kinematics import (
    fkine_dh,
    fkine_dh_all,
    validate_joint_config,
    fkine_performance_test,
)
from robotics_numpy.transforms import SE3


class TestDHLink:
    """Test DH link functionality."""

    def test_dhlink_creation_revolute(self):
        """Test creating revolute DH link."""
        link = DHLink(d=0.1, a=0.2, alpha=np.pi / 2, theta=0, joint_type="R")

        assert link.d == 0.1
        assert link.a == 0.2
        assert link.alpha == np.pi / 2
        assert link.theta == 0
        assert link.is_revolute()
        assert not link.is_prismatic()

    def test_dhlink_creation_prismatic(self):
        """Test creating prismatic DH link."""
        link = DHLink(d=0, a=0.1, alpha=0, theta=np.pi / 4, joint_type="P")

        assert link.d == 0
        assert link.a == 0.1
        assert link.alpha == 0
        assert link.theta == np.pi / 4
        assert link.is_prismatic()
        assert not link.is_revolute()

    def test_dhlink_with_limits(self):
        """Test DH link with joint limits."""
        qlim = [-np.pi, np.pi]
        link = DHLink(joint_type="R", qlim=qlim)

        assert link.qlim == qlim

    def test_dhlink_with_dynamics(self):
        """Test DH link with dynamic parameters."""
        link = DHLink(
            joint_type="R",
            m=5.0,
            r=[0.1, 0.2, 0.3],
            I=[1, 2, 3, 0, 0, 0],
            Jm=0.5,
            G=100,
            B=0.1,
            Tc=[0.2, -0.15],
        )

        assert link.m == 5.0
        assert link.r == [0.1, 0.2, 0.3]
        assert link.I == [1, 2, 3, 0, 0, 0]
        assert link.Jm == 0.5
        assert link.G == 100
        assert link.B == 0.1
        assert link.Tc == [0.2, -0.15]

    def test_dhlink_transformation_revolute(self):
        """Test transformation matrix for revolute joint."""
        link = RevoluteDH(d=0.1, a=0.2, alpha=np.pi / 2)

        # Test at zero angle
        T0 = link.A(0)
        assert isinstance(T0, SE3)

        # Test at 90 degrees
        T90 = link.A(np.pi / 2)
        assert isinstance(T90, SE3)

        # Transformations should be different
        assert not np.allclose(T0.matrix, T90.matrix)

    def test_dhlink_transformation_prismatic(self):
        """Test transformation matrix for prismatic joint."""
        link = PrismaticDH(theta=0, a=0.1, alpha=0)

        # Test at zero displacement
        T0 = link.A(0)
        assert isinstance(T0, SE3)

        # Test at 0.1m displacement
        T1 = link.A(0.1)
        assert isinstance(T1, SE3)

        # Z displacement should change
        assert T0.t[2] != T1.t[2]

    def test_dhlink_invalid_inputs(self):
        """Test DH link with invalid inputs."""
        with pytest.raises(ValueError):
            DHLink(joint_type="X")  # Invalid joint type

        with pytest.raises(ValueError):
            DHLink(qlim=[1])  # Wrong qlim length

        with pytest.raises(ValueError):
            DHLink(qlim=[1, 0])  # Invalid qlim order

        with pytest.raises(ValueError):
            DHLink(r=[1, 2])  # Wrong r length

        with pytest.raises(ValueError):
            DHLink(I=[1, 2, 3])  # Wrong I length

    def test_revolute_dh_convenience_class(self):
        """Test RevoluteDH convenience class."""
        link = RevoluteDH(d=0.1, a=0.2, alpha=np.pi / 2, qlim=[-np.pi, np.pi])

        assert link.is_revolute()
        assert link.d == 0.1
        assert link.a == 0.2
        assert link.alpha == np.pi / 2
        assert link.qlim == [-np.pi, np.pi]

    def test_prismatic_dh_convenience_class(self):
        """Test PrismaticDH convenience class."""
        link = PrismaticDH(theta=np.pi / 4, a=0.1, alpha=0, qlim=[0, 0.5])

        assert link.is_prismatic()
        assert link.theta == np.pi / 4
        assert link.a == 0.1
        assert link.alpha == 0
        assert link.qlim == [0, 0.5]


class TestDHRobot:
    """Test DHRobot functionality."""

    def test_dhrobot_creation(self):
        """Test creating DHRobot."""
        links = [RevoluteDH(d=0.1, a=0.2, alpha=0), RevoluteDH(d=0, a=0.3, alpha=0)]
        robot = DHRobot(links, name="Test Robot")

        assert robot.n == 2
        assert robot.name == "Test Robot"
        assert len(robot.links) == 2
        assert robot.joint_types == ["R", "R"]

    def test_dhrobot_properties(self):
        """Test DHRobot properties."""
        links = [
            RevoluteDH(d=0.1, a=0.2, alpha=0, qlim=[-np.pi, np.pi]),
            PrismaticDH(theta=0, a=0.1, alpha=0, qlim=[0, 0.5]),
        ]
        robot = DHRobot(links)

        assert robot.n == 2
        assert robot.joint_types == ["R", "P"]

        # Test joint limits
        qlim = robot.qlim
        print(f"qlim array: {qlim}")
        assert qlim.shape == (2, 2)
        np.testing.assert_allclose(qlim[:, 0], [-np.pi, np.pi])
        np.testing.assert_allclose(qlim[:, 1], [0, 0.5])

    def test_dhrobot_forward_kinematics(self):
        """Test forward kinematics computation."""
        links = [RevoluteDH(d=0, a=0.3, alpha=0), RevoluteDH(d=0, a=0.2, alpha=0)]
        robot = DHRobot(links, name="2DOF Planar")

        # Test zero configuration
        T = robot.fkine([0, 0])
        expected_pos = [0.5, 0, 0]  # Should reach 0.3 + 0.2 = 0.5 in X
        np.testing.assert_allclose(T.t, expected_pos, atol=1e-10)

        # Test 90 degree configuration
        T90 = robot.fkine([np.pi / 2, 0])
        expected_pos_90 = [0, 0.5, 0]  # Should reach in Y direction
        np.testing.assert_allclose(T90.t, expected_pos_90, atol=1e-10)

    def test_dhrobot_fkine_all(self):
        """Test forward kinematics for all frames."""
        links = [RevoluteDH(d=0, a=0.3, alpha=0), RevoluteDH(d=0, a=0.2, alpha=0)]
        robot = DHRobot(links)

        poses = robot.fkine_all([0, 0])
        assert len(poses) == 2

        # First link should be at [0.3, 0, 0]
        np.testing.assert_allclose(poses[0].t, [0.3, 0, 0], atol=1e-10)
        # Second link should be at [0.5, 0, 0]
        np.testing.assert_allclose(poses[1].t, [0.5, 0, 0], atol=1e-10)

    def test_dhrobot_configurations(self):
        """Test robot configuration management."""
        links = [RevoluteDH(d=0, a=0.3, alpha=0)]
        robot = DHRobot(links)

        # Add configuration
        q_test = [np.pi / 4]
        robot.addconfiguration("test", q_test)

        assert "test" in robot.configurations()
        retrieved_q = robot.getconfig("test")
        np.testing.assert_allclose(retrieved_q, q_test)

        # Test accessing as attribute
        assert hasattr(robot, "test")
        np.testing.assert_allclose(robot.test, q_test)

    def test_dhrobot_invalid_inputs(self):
        """Test DHRobot with invalid inputs."""
        with pytest.raises(ValueError):
            DHRobot([])  # Empty links

        with pytest.raises(TypeError):
            DHRobot("not a list")  # Invalid links type

    def test_dhrobot_validation(self):
        """Test joint configuration validation."""
        links = [RevoluteDH(d=0, a=0.3, alpha=0)]
        robot = DHRobot(links)

        # Valid configuration
        valid_q = [0.5]
        validated = robot._validate_q(valid_q)
        np.testing.assert_allclose(validated, [0.5])

        # Invalid length
        with pytest.raises(ValueError):
            robot._validate_q([0.5, 0.3])  # Too many values


class TestForwardKinematics:
    """Test forward kinematics algorithms."""

    def test_fkine_dh_simple(self):
        """Test simple forward kinematics."""
        links = [RevoluteDH(d=0, a=0.5, alpha=0)]
        q = [0]

        T = fkine_dh(links, q)
        expected_pos = [0.5, 0, 0]
        np.testing.assert_allclose(T.t, expected_pos, atol=1e-10)

    def test_fkine_dh_multiple_links(self):
        """Test forward kinematics with multiple links."""
        links = [
            RevoluteDH(d=0, a=0.3, alpha=0),
            RevoluteDH(d=0, a=0.2, alpha=0),
            RevoluteDH(d=0, a=0.1, alpha=0),
        ]
        q = [0, 0, 0]

        T = fkine_dh(links, q)
        expected_pos = [0.6, 0, 0]  # 0.3 + 0.2 + 0.1
        np.testing.assert_allclose(T.t, expected_pos, atol=1e-10)

    def test_fkine_dh_all(self):
        """Test forward kinematics for all intermediate frames."""
        links = [RevoluteDH(d=0, a=0.3, alpha=0), RevoluteDH(d=0, a=0.2, alpha=0)]
        q = [0, 0]

        poses = fkine_dh_all(links, q)
        assert len(poses) == 2

        np.testing.assert_allclose(poses[0].t, [0.3, 0, 0], atol=1e-10)
        np.testing.assert_allclose(poses[1].t, [0.5, 0, 0], atol=1e-10)

    def test_fkine_prismatic_joint(self):
        """Test forward kinematics with prismatic joint."""
        links = [PrismaticDH(theta=0, a=0, alpha=0)]
        q = [0.5]  # 0.5m extension

        T = fkine_dh(links, q)
        expected_pos = [0, 0, 0.5]  # Extension in Z
        np.testing.assert_allclose(T.t, expected_pos, atol=1e-10)

    def test_fkine_mixed_joints(self):
        """Test forward kinematics with mixed joint types."""
        links = [RevoluteDH(d=0, a=0.3, alpha=0), PrismaticDH(theta=0, a=0, alpha=0)]
        q = [0, 0.2]  # Revolute at 0, prismatic at 0.2m

        T = fkine_dh(links, q)
        expected_pos = [0.3, 0, 0.2]
        np.testing.assert_allclose(T.t, expected_pos, atol=1e-10)

    def test_validate_joint_config(self):
        """Test joint configuration validation."""
        links = [
            RevoluteDH(d=0, a=0.3, alpha=0, qlim=[-np.pi, np.pi]),
            RevoluteDH(d=0, a=0.2, alpha=0, qlim=[-np.pi / 2, np.pi / 2]),
        ]

        # Valid configuration
        assert validate_joint_config(links, [0.5, 0.3], warn=False)

        # Invalid configuration (exceeds limits)
        assert not validate_joint_config(links, [0.5, 2.0], warn=False)

        # Wrong dimensions
        assert not validate_joint_config(links, [0.5], warn=False)


class TestStanfordArm:
    """Test Stanford Arm robot model."""

    def test_stanford_creation(self):
        """Test Stanford Arm creation."""
        robot = Stanford()

        assert robot.n == 6
        assert robot.name == "Stanford Arm"
        assert robot.manufacturer == "Victor Scheinman"
        assert "spherical_wrist" in robot.keywords
        assert "prismatic" in robot.keywords

    def test_stanford_joint_types(self):
        """Test Stanford Arm joint types."""
        robot = Stanford()
        expected_types = ["R", "R", "P", "R", "R", "R"]
        assert robot.joint_types == expected_types

    def test_stanford_configurations(self):
        """Test Stanford Arm predefined configurations."""
        robot = Stanford()

        # Should have these configurations
        configs = ["qr", "qz", "qextended", "qfolded"]
        for config in configs:
            assert config in robot.configurations()
            q = getattr(robot, config)
            assert len(q) == 6

    def test_stanford_forward_kinematics(self):
        """Test Stanford Arm forward kinematics."""
        robot = Stanford()

        # Test zero configuration
        T = robot.fkine(robot.qz)
        assert isinstance(T, SE3)

        # End-effector should be reachable
        assert robot.reach(T.t)

    def test_stanford_spherical_wrist(self):
        """Test Stanford Arm spherical wrist detection."""
        robot = Stanford()
        assert robot.isspherical()

    def test_stanford_singularity_check(self):
        """Test Stanford Arm singularity detection."""
        robot = Stanford()

        # Zero configuration is singular (joint 5 = 0)
        assert robot.is_singular(robot.qz)

        # Wrist singularity (joint 5 = 0)
        q_singular = np.array([0, 0, 0.3, 0, 0, 0])
        assert robot.is_singular(q_singular)

        # Non-singular configuration (joint 5 != 0)
        q_non_singular = np.array([0, 0, 0.3, 0, np.pi / 4, 0])
        assert not robot.is_singular(q_non_singular)

    def test_stanford_workspace(self):
        """Test Stanford Arm workspace analysis."""
        robot = Stanford()

        # Should have reasonable workspace volume
        volume = robot.workspace_volume()
        assert volume > 0
        assert volume < 100  # Should be reasonable

    def test_stanford_reachability(self):
        """Test Stanford Arm reachability."""
        robot = Stanford()

        # Points that should be reachable
        reachable_points = [
            [0.5, 0, 0.5],
            [0, 0.3, 0.4],
        ]

        for point in reachable_points:
            assert robot.reach(np.array(point))

        # Points that should not be reachable
        unreachable_points = [
            [2.0, 0, 0],  # Too far
            [0, 0, -0.6],  # Too far below base
        ]

        for point in unreachable_points:
            assert not robot.reach(np.array(point))


class TestRobotCreation:
    """Test robot creation utilities."""

    def test_create_simple_arm(self):
        """Test simple arm creation."""
        robot = create_simple_arm(n_joints=3)

        assert robot.n == 3
        assert all(link.is_revolute() for link in robot.links)
        assert "qz" in robot.configurations()
        assert "qr" in robot.configurations()

    def test_create_planar_arm(self):
        """Test planar arm creation."""
        robot = create_planar_arm(n_joints=3, link_lengths=[0.3, 0.2, 0.1])

        assert robot.n == 3
        assert all(link.is_revolute() for link in robot.links)
        assert all(abs(link.alpha) < 1e-6 for link in robot.links)  # All alpha=0

        # Test with default lengths
        robot_default = create_planar_arm(n_joints=2)
        assert robot_default.n == 2


class TestPerformance:
    """Test performance requirements."""

    def test_fkine_performance(self):
        """Test forward kinematics performance."""
        # Create test robot
        links = [RevoluteDH(d=0, a=0.3, alpha=0) for _ in range(6)]

        # Performance test with fewer iterations for unit tests
        stats = fkine_performance_test(links, n_iterations=1000)

        # Should complete without errors
        assert stats["iterations"] == 1000
        assert stats["mean_time_us"] > 0
        assert "target_position" in stats

    def test_batch_performance(self):
        """Test batch processing doesn't degrade performance."""
        robot = create_simple_arm(3)

        # Single computation
        import time

        q = [0.1, 0.2, 0.3]

        start = time.perf_counter()
        T1 = robot.fkine(q)
        single_time = time.perf_counter() - start

        # Batch computation
        q_batch = [q] * 10
        start = time.perf_counter()
        for q_i in q_batch:
            Ti = robot.fkine(q_i)
        batch_time = time.perf_counter() - start

        # Batch should not be significantly slower per computation
        avg_batch_time = batch_time / 10
        assert avg_batch_time < single_time * 2  # Allow some overhead


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_dh_parameter_validation(self):
        """Test DH parameter validation."""
        # Valid links
        valid_links = [RevoluteDH(d=0.1, a=0.2, alpha=np.pi / 2)]
        assert dh_check_parameters(valid_links)

        # Empty links
        with pytest.raises(ValueError):
            dh_check_parameters([])

    def test_large_joint_values(self):
        """Test handling of large joint values."""
        robot = create_simple_arm(2)

        # Large but valid joint values
        q_large = [10 * np.pi, -5 * np.pi]  # Multiple rotations
        T = robot.fkine(q_large)
        assert isinstance(T, SE3)

    def test_numerical_precision(self):
        """Test numerical precision in computations."""
        robot = create_simple_arm(1)

        # Very small joint values
        q_small = [1e-10]
        T_small = robot.fkine(q_small)

        # Should be close to zero configuration
        T_zero = robot.fkine([0])
        np.testing.assert_allclose(T_small.t, T_zero.t, atol=1e-9)


class TestGenericRobot:
    """Test Generic robot model functionality."""

    def test_generic_creation_default(self):
        """Test Generic robot creation with default parameters."""
        robot = Generic(dofs=3)

        assert robot.n == 3
        assert robot.name == "GenericDH"
        assert len(robot.links) == 3

        # Check default values
        params = robot.dh_parameters
        assert len(params["a"]) == 3
        assert len(params["d"]) == 3
        assert len(params["alpha"]) == 3
        assert len(params["offset"]) == 3
        assert all(jtype == "R" for jtype in params["joint_types"])

    def test_generic_creation_custom(self):
        """Test Generic robot creation with custom parameters."""
        robot = Generic(
            dofs=4,
            a=[0, -0.5, -0.5, -0.5],
            d=[0.5, 0, 0, 0],
            alpha=[np.pi / 2, 0, 0, 0],
            offset=[0, np.pi / 4, -np.pi / 4, np.pi / 2],
            qlim=[
                [-np.pi, np.pi],
                [-np.pi / 2, np.pi / 2],
                [-np.pi / 3, np.pi / 3],
                [-np.pi / 6, np.pi / 6],
            ],
            name="GenericRobot",
        )

        assert robot.n == 4
        assert robot.name == "GenericRobot"

        # Check custom values
        params = robot.dh_parameters
        assert params["a"] == [0, -0.5, -0.5, -0.5]
        assert params["d"] == [0.5, 0, 0, 0]
        np.testing.assert_allclose(params["alpha"], [np.pi / 2, 0, 0, 0])

    def test_generic_mixed_joints(self):
        """Test Generic robot with mixed joint types."""
        robot = Generic(
            dofs=3,
            joint_types=["R", "P", "R"],
            a=[0.1, 0.2, 0.1],
            d=[0.1, 0, 0.1],
            alpha=[np.pi / 2, 0, 0],
        )

        assert robot.n == 3
        joint_types = robot.dh_parameters["joint_types"]
        assert joint_types == ["R", "P", "R"]

        # Check that second link is prismatic
        assert robot.links[1].is_prismatic()
        assert robot.links[0].is_revolute()
        assert robot.links[2].is_revolute()

    def test_generic_forward_kinematics(self):
        """Test forward kinematics computation."""
        robot = Generic(dofs=2, a=[0.3, 0.2], d=[0, 0], alpha=[0, 0], offset=[0, 0])

        # Test zero configuration
        T_zero = robot.fkine(robot.qz)
        expected_pos = [0.5, 0, 0]  # Sum of link lengths
        np.testing.assert_allclose(T_zero.t, expected_pos, atol=1e-10)

        # Test 90-degree configuration
        q = [np.pi / 2, 0]
        T_90 = robot.fkine(q)
        expected_pos_90 = [
            0,
            0.5,
            0,
        ]  # When first joint rotates 90°, end-effector is at [0, sum_of_links, 0]
        np.testing.assert_allclose(T_90.t, expected_pos_90, atol=1e-10)

    def test_generic_configurations(self):
        """Test predefined configurations."""
        robot = Generic(dofs=3, offset=[0.1, 0.2, 0.3])

        # Check ready configuration
        np.testing.assert_allclose(robot.qr, [0.1, 0.2, 0.3])

        # Check zero configuration
        np.testing.assert_allclose(robot.qz, [0, 0, 0])

        # Test forward kinematics with configurations
        T_r = robot.fkine(robot.qr)
        T_z = robot.fkine(robot.qz)

        # Positions should be different
        assert not np.allclose(T_r.t, T_z.t)

    def test_generic_dynamic_properties(self):
        """Test setting dynamic properties."""
        robot = Generic(dofs=2)

        # Set mass properties
        masses = [1.0, 0.5]
        centers_of_mass = [[0.1, 0, 0], [0.05, 0, 0]]
        inertias = [[0.1, 0.1, 0.1, 0, 0, 0], [0.05, 0.05, 0.05, 0, 0, 0]]

        robot.set_dynamic_properties(m=masses, r=centers_of_mass, I=inertias)

        # Check that properties were set
        assert robot.links[0].m == 1.0
        assert robot.links[1].m == 0.5
        assert robot.links[0].r == [0.1, 0, 0]
        assert robot.links[1].r == [0.05, 0, 0]

    def test_generic_workspace_radius(self):
        """Test workspace radius calculation."""
        robot = Generic(dofs=3, a=[0.3, 0.2, 0.1], d=[0.1, 0, 0])

        radius = robot.workspace_radius()
        expected_radius = 0.3 + 0.2 + 0.1 + 0.1  # Sum of a and d values
        assert abs(radius - expected_radius) < 1e-6

    def test_generic_validation_errors(self):
        """Test validation error handling."""
        # Test invalid DOFs
        with pytest.raises(ValueError, match="dofs must be a positive integer"):
            Generic(dofs=0)

        # Test mismatched parameter lengths
        with pytest.raises(ValueError, match="Length of 'a'"):
            Generic(dofs=3, a=[0.1, 0.2])

        # Test invalid joint types
        with pytest.raises(ValueError, match="must be 'R' or 'P'"):
            Generic(dofs=2, joint_types=["R", "X"])

        # Test invalid qlim format
        with pytest.raises(ValueError, match="must have exactly 2 elements"):
            Generic(dofs=2, qlim=[[0, 1, 2], [0, 1]])

    def test_create_generic_robot_factory(self):
        """Test factory function for creating generic robots."""
        # Test simple creation
        robot3 = create_generic_robot(3)
        assert robot3.n == 3
        assert robot3.name == "Generic3DOF"

        # Test with custom link lengths
        robot4 = create_generic_robot(4, link_lengths=[0.2, 0.3, 0.2, 0.1])
        params = robot4.dh_parameters
        assert params["a"] == [0.2, 0.3, 0.2, 0.1]

        # Test 6-DOF robot (should have spherical wrist)
        robot6 = create_generic_robot(6)
        assert robot6.n == 6
        params = robot6.dh_parameters
        # Check that it has some non-zero alpha values (typical for 6-DOF)
        assert any(abs(alpha) > 0.1 for alpha in params["alpha"])

    def test_generic_summary_and_str(self):
        """Test string representations."""
        robot = Generic(dofs=2, name="Test2DOF")

        # Test summary
        summary = robot.summary()
        assert "Test2DOF" in summary
        assert "DOFs: 2" in summary
        assert "DH Parameters:" in summary

        # Test __str__
        str_repr = str(robot)
        assert str_repr == summary

        # Test __repr__
        repr_str = repr(robot)
        assert "Generic(dofs=2" in repr_str
        assert "name='Test2DOF'" in repr_str


if __name__ == "__main__":
    pytest.main([__file__])
