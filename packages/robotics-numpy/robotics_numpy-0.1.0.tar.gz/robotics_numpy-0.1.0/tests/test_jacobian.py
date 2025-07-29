#!/usr/bin/env python3
"""
Test for Jacobian and manipulability functionality
"""

import numpy as np
import unittest

from robotics_numpy.models import Stanford, create_simple_arm
from robotics_numpy.kinematics import (
    tr2jac,
    jacobe,
    jacob0,
    manipulability,
    joint_velocity_ellipsoid,
)
from robotics_numpy.transforms import SE3


class TestJacobian(unittest.TestCase):
    """Test Jacobian computation functions."""

    def setUp(self):
        """Set up test cases."""
        self.robot = Stanford()
        self.q_zero = np.zeros(self.robot.n)
        self.q_nonzero = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])

    def test_tr2jac(self):
        """Test Jacobian transformation."""
        # Create a test transformation
        T = SE3.Rz(np.pi / 4) * SE3.Trans(1, 2, 3)
        J_transform = tr2jac(T.matrix)

        # Check dimensions
        self.assertEqual(J_transform.shape, (6, 6))

        # Check rotation part matches transformation rotation
        self.assertTrue(np.allclose(J_transform[:3, :3], T.R))
        self.assertTrue(np.allclose(J_transform[3:, 3:], T.R))

    def test_jacobe(self):
        """Test end-effector Jacobian."""
        # Test with zero configuration
        Je = jacobe(self.robot, self.q_zero)

        # Check dimensions
        self.assertEqual(Je.shape, (6, self.robot.n))

        # Test partial chain Jacobian
        Je_partial = jacobe(self.robot, self.q_zero, end=2, start=0)
        self.assertEqual(Je_partial.shape, (6, 3))

        # Test with non-zero configuration
        Je_nonzero = jacobe(self.robot, self.q_nonzero)
        self.assertEqual(Je_nonzero.shape, (6, self.robot.n))

    def test_jacob0(self):
        """Test base frame Jacobian."""
        # Test with zero configuration
        J0 = jacob0(self.robot, self.q_zero)

        # Check dimensions
        self.assertEqual(J0.shape, (6, self.robot.n))

        # Test with supplied transformation
        T = self.robot.fkine(self.q_zero)
        J0_with_T = jacob0(self.robot, self.q_zero, T=T)
        self.assertTrue(np.allclose(J0, J0_with_T))

        # Test half Jacobian options
        J0_trans = jacob0(self.robot, self.q_zero, half="trans")
        self.assertEqual(J0_trans.shape, (3, self.robot.n))

        J0_rot = jacob0(self.robot, self.q_zero, half="rot")
        self.assertEqual(J0_rot.shape, (3, self.robot.n))

        # Check that full Jacobian equals the stacked half Jacobians
        J0_combined = np.vstack((J0_trans, J0_rot))
        self.assertTrue(np.allclose(J0, J0_combined))

    def test_manipulability(self):
        """Test manipulability measures."""
        # Test Yoshikawa's measure with zero configuration
        m = manipulability(self.robot, self.q_zero)
        self.assertIsInstance(m, float)

        # Test with precomputed Jacobian
        J0 = jacob0(self.robot, self.q_zero)
        m_with_J = manipulability(self.robot, J=J0)
        self.assertAlmostEqual(m, m_with_J)

        # Test different methods
        m_inv_cond = manipulability(self.robot, self.q_zero, method="invcondition")
        self.assertIsInstance(m_inv_cond, float)
        self.assertTrue(0 <= m_inv_cond <= 1)  # Inverse condition number is in [0,1]

        m_min_sing = manipulability(self.robot, self.q_zero, method="minsingular")
        self.assertIsInstance(m_min_sing, float)
        self.assertTrue(m_min_sing >= 0)  # Singular values are non-negative

        # Test different axes options
        m_trans = manipulability(self.robot, self.q_zero, axes="trans")
        self.assertIsInstance(m_trans, float)

        m_rot = manipulability(self.robot, self.q_zero, axes="rot")
        self.assertIsInstance(m_rot, float)

        # Test with boolean list for axes selection
        m_custom = manipulability(
            self.robot, self.q_zero, axes=[True, True, True, False, False, False]
        )
        self.assertAlmostEqual(m_trans, m_custom)

    def test_joint_velocity_ellipsoid(self):
        """Test joint velocity ellipsoid computation."""
        # Compute Jacobian
        J = jacob0(self.robot, self.q_zero, half="trans")

        # Compute ellipsoid
        eigvals, eigvecs = joint_velocity_ellipsoid(J)

        # Check dimensions
        self.assertEqual(eigvals.shape, (3,))
        self.assertEqual(eigvecs.shape, (3, 3))

        # Check eigenvalues are non-negative
        self.assertTrue(np.all(eigvals >= 0))

        # Check eigenvectors are orthogonal
        for i in range(3):
            for j in range(i + 1, 3):
                dot_product = np.abs(np.dot(eigvecs[:, i], eigvecs[:, j]))
                self.assertAlmostEqual(dot_product, 0, places=5)

        # Test with custom joint velocity limits
        dq_max = np.ones(self.robot.n)
        eigvals2, eigvecs2 = joint_velocity_ellipsoid(J, dq_max)
        self.assertEqual(eigvals2.shape, (3,))


class TestRobotJacobian(unittest.TestCase):
    """Test Jacobian methods of the DHRobot class."""

    def setUp(self):
        """Set up test cases."""
        self.robot = Stanford()
        self.q_zero = np.zeros(self.robot.n)

    def test_robot_jacob0(self):
        """Test robot.jacob0() method."""
        # Compute Jacobian through robot method
        J0_robot = self.robot.jacob0(self.q_zero)

        # Compute Jacobian directly
        J0_direct = jacob0(self.robot, self.q_zero)

        # Check they match
        self.assertTrue(np.allclose(J0_robot, J0_direct))

        # Test half Jacobian options
        J0_trans = self.robot.jacob0(self.q_zero, half="trans")
        self.assertEqual(J0_trans.shape, (3, self.robot.n))

        # Test with invalid half option
        with self.assertRaises(ValueError):
            self.robot.jacob0(self.q_zero, half="invalid")

    def test_robot_manipulability(self):
        """Test robot.manipulability() method."""
        # Compute manipulability through robot method
        m_robot = self.robot.manipulability(self.q_zero)

        # Compute manipulability directly
        m_direct = manipulability(self.robot, self.q_zero)

        # Check they match
        self.assertAlmostEqual(m_robot, m_direct)

        # Test different methods
        m_inv_cond = self.robot.manipulability(self.q_zero, method="invcondition")
        self.assertTrue(0 <= m_inv_cond <= 1)

        # Test with invalid method
        with self.assertRaises(ValueError):
            self.robot.manipulability(self.q_zero, method="invalid")

        # Test with precomputed Jacobian
        J = self.robot.jacob0(self.q_zero)
        m_with_J = self.robot.manipulability(J=J)
        self.assertAlmostEqual(m_robot, m_with_J)


if __name__ == "__main__":
    unittest.main()
