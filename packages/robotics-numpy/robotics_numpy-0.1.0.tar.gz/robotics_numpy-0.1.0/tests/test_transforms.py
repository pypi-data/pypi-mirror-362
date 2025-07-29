"""
Tests for transforms module in robotics-numpy

This module tests all transformation functionality including:
- Basic rotation matrices (rotx, roty, rotz)
- Roll-pitch-yaw conversions
- Euler angle conversions
- Quaternion operations
- Homogeneous transformations
- SE3 and SO3 classes
"""

import pytest
import numpy as np
from robotics_numpy.transforms import (
    rotx, roty, rotz, rpy2r, r2rpy, eul2r, r2eul,
    quat2r, r2quat, quat_multiply, quat_inverse, quat_normalize,
    is_rotation_matrix, transl, rotmat, SE3_from_matrix,
    homogeneous_inverse, is_homogeneous, SO3, SE3
)


class TestBasicRotations:
    """Test basic rotation matrices."""

    def test_rotx_identity(self):
        """Test X-axis rotation by 0."""
        R = rotx(0)
        np.testing.assert_allclose(R, np.eye(3))

    def test_rotx_90deg(self):
        """Test X-axis rotation by 90 degrees."""
        R = rotx(np.pi/2)
        expected = np.array([
            [1, 0, 0],
            [0, 0, -1],
            [0, 1, 0]
        ])
        np.testing.assert_allclose(R, expected, atol=1e-10)

    def test_roty_identity(self):
        """Test Y-axis rotation by 0."""
        R = roty(0)
        np.testing.assert_allclose(R, np.eye(3))

    def test_roty_90deg(self):
        """Test Y-axis rotation by 90 degrees."""
        R = roty(np.pi/2)
        expected = np.array([
            [0, 0, 1],
            [0, 1, 0],
            [-1, 0, 0]
        ])
        np.testing.assert_allclose(R, expected, atol=1e-10)

    def test_rotz_identity(self):
        """Test Z-axis rotation by 0."""
        R = rotz(0)
        np.testing.assert_allclose(R, np.eye(3))

    def test_rotz_90deg(self):
        """Test Z-axis rotation by 90 degrees."""
        R = rotz(np.pi/2)
        expected = np.array([
            [0, -1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])
        np.testing.assert_allclose(R, expected, atol=1e-10)

    def test_batch_rotations(self):
        """Test batch rotation operations."""
        angles = np.array([0, np.pi/4, np.pi/2])
        R_batch = rotx(angles)

        assert R_batch.shape == (3, 3, 3)

        # Check first rotation (identity)
        np.testing.assert_allclose(R_batch[0], np.eye(3))

        # Check last rotation (90 degrees)
        expected = np.array([
            [1, 0, 0],
            [0, 0, -1],
            [0, 1, 0]
        ])
        np.testing.assert_allclose(R_batch[2], expected, atol=1e-10)


class TestRPYConversions:
    """Test roll-pitch-yaw conversions."""

    def test_rpy2r_identity(self):
        """Test RPY to rotation matrix for identity."""
        R = rpy2r(0, 0, 0)
        np.testing.assert_allclose(R, np.eye(3))

    def test_rpy2r_roundtrip(self):
        """Test RPY to rotation matrix and back."""
        roll, pitch, yaw = 0.1, 0.2, 0.3
        R = rpy2r(roll, pitch, yaw)
        roll_out, pitch_out, yaw_out = r2rpy(R)

        np.testing.assert_allclose([roll_out, pitch_out, yaw_out],
                                 [roll, pitch, yaw], atol=1e-10)

    def test_r2rpy_gimbal_lock(self):
        """Test RPY extraction at gimbal lock."""
        # Create rotation with pitch = ±π/2 (gimbal lock)
        R = rpy2r(0.5, np.pi/2, 0.3)
        roll, pitch, yaw = r2rpy(R)

        # Should handle gimbal lock gracefully
        assert abs(pitch - np.pi/2) < 1e-10

    def test_rpy_orthogonality(self):
        """Test that RPY rotations produce orthogonal matrices."""
        for _ in range(10):
            roll = np.random.uniform(-np.pi, np.pi)
            pitch = np.random.uniform(-np.pi/2, np.pi/2)
            yaw = np.random.uniform(-np.pi, np.pi)

            R = rpy2r(roll, pitch, yaw)
            assert is_rotation_matrix(R)


class TestEulerAngles:
    """Test Euler angle conversions."""

    def test_eul2r_zyz_identity(self):
        """Test ZYZ Euler angles for identity."""
        R = eul2r(0, 0, 0, 'ZYZ')
        np.testing.assert_allclose(R, np.eye(3))

    def test_eul2r_zyx_identity(self):
        """Test ZYX Euler angles for identity."""
        R = eul2r(0, 0, 0, 'ZYX')
        np.testing.assert_allclose(R, np.eye(3))

    def test_eul_roundtrip_zyz(self):
        """Test ZYZ Euler angle roundtrip."""
        phi, theta, psi = 0.1, 0.5, 0.3
        R = eul2r(phi, theta, psi, 'ZYZ')
        phi_out, theta_out, psi_out = r2eul(R, 'ZYZ')

        np.testing.assert_allclose([phi_out, theta_out, psi_out],
                                 [phi, theta, psi], atol=1e-10)

    def test_unsupported_convention(self):
        """Test error for unsupported Euler convention."""
        with pytest.raises(ValueError):
            eul2r(0, 0, 0, 'XYZ')


class TestQuaternions:
    """Test quaternion operations."""

    def test_quat2r_identity(self):
        """Test identity quaternion to rotation matrix."""
        q = [1, 0, 0, 0]  # Identity quaternion
        R = quat2r(q)
        np.testing.assert_allclose(R, np.eye(3))

    def test_quat_roundtrip(self):
        """Test quaternion to rotation matrix and back."""
        # Random rotation matrix
        R_original = rotx(0.3) @ roty(0.4) @ rotz(0.5)
        q = r2quat(R_original)
        R_reconstructed = quat2r(q)

        np.testing.assert_allclose(R_original, R_reconstructed, atol=1e-10)

    def test_quat_multiply(self):
        """Test quaternion multiplication."""
        q1 = [1, 0, 0, 0]  # Identity
        q2 = r2quat(rotx(np.pi/2))

        q_result = quat_multiply(q1, q2)
        np.testing.assert_allclose(q_result, q2, atol=1e-10)

    def test_quat_inverse(self):
        """Test quaternion inverse."""
        q = r2quat(rotx(0.5))
        q_inv = quat_inverse(q)
        q_identity = quat_multiply(q, q_inv)

        expected_identity = [1, 0, 0, 0]
        np.testing.assert_allclose(q_identity, expected_identity, atol=1e-10)

    def test_quat_normalize(self):
        """Test quaternion normalization."""
        q = [2, 0, 0, 0]  # Unnormalized
        q_norm = quat_normalize(q)

        assert abs(np.linalg.norm(q_norm) - 1.0) < 1e-10
        np.testing.assert_allclose(q_norm, [1, 0, 0, 0])


class TestRotationMatrixValidation:
    """Test rotation matrix validation."""

    def test_is_rotation_matrix_identity(self):
        """Test validation of identity matrix."""
        assert is_rotation_matrix(np.eye(3))

    def test_is_rotation_matrix_valid(self):
        """Test validation of valid rotation matrices."""
        R1 = rotx(0.5)
        R2 = roty(0.3) @ rotz(0.7)

        assert is_rotation_matrix(R1)
        assert is_rotation_matrix(R2)

    def test_is_rotation_matrix_invalid_shape(self):
        """Test rejection of wrong-shaped matrices."""
        assert not is_rotation_matrix(np.eye(2))
        assert not is_rotation_matrix(np.ones((3, 4)))

    def test_is_rotation_matrix_invalid_orthogonal(self):
        """Test rejection of non-orthogonal matrices."""
        R_bad = np.array([
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        assert not is_rotation_matrix(R_bad)

    def test_is_rotation_matrix_invalid_determinant(self):
        """Test rejection of matrices with wrong determinant."""
        R_bad = np.array([
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        assert not is_rotation_matrix(R_bad)


class TestHomogeneousTransforms:
    """Test homogeneous transformation operations."""

    def test_transl_scalar_args(self):
        """Test translation matrix from scalar arguments."""
        T = transl(1, 2, 3)
        expected = np.array([
            [1, 0, 0, 1],
            [0, 1, 0, 2],
            [0, 0, 1, 3],
            [0, 0, 0, 1]
        ])
        np.testing.assert_allclose(T, expected)

    def test_transl_vector_arg(self):
        """Test translation matrix from vector argument."""
        T1 = transl([1, 2, 3])
        T2 = transl(np.array([1, 2, 3]))

        expected = np.array([
            [1, 0, 0, 1],
            [0, 1, 0, 2],
            [0, 0, 1, 3],
            [0, 0, 0, 1]
        ])
        np.testing.assert_allclose(T1, expected)
        np.testing.assert_allclose(T2, expected)

    def test_rotmat_pure_rotation(self):
        """Test homogeneous matrix from pure rotation."""
        R = rotx(np.pi/2)
        T = rotmat(R)

        expected = np.array([
            [1, 0, 0, 0],
            [0, 0, -1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]
        ])
        np.testing.assert_allclose(T, expected, atol=1e-10)

    def test_rotmat_with_translation(self):
        """Test homogeneous matrix from rotation and translation."""
        R = rotx(np.pi/2)
        t = [1, 2, 3]
        T = rotmat(R, t)

        expected = np.array([
            [1, 0, 0, 1],
            [0, 0, -1, 2],
            [0, 1, 0, 3],
            [0, 0, 0, 1]
        ])
        np.testing.assert_allclose(T, expected, atol=1e-10)

    def test_homogeneous_inverse(self):
        """Test homogeneous transformation inverse."""
        T = transl(1, 2, 3) @ rotmat(rotx(0.5))
        T_inv = homogeneous_inverse(T)

        # T * T_inv should be identity
        identity = T @ T_inv
        np.testing.assert_allclose(identity, np.eye(4), atol=1e-10)

    def test_is_homogeneous_valid(self):
        """Test validation of valid homogeneous matrices."""
        T1 = transl(1, 2, 3)
        T2 = rotmat(rotx(0.5))
        T3 = transl(0, 0, 0) @ rotmat(roty(0.3))

        assert is_homogeneous(T1)
        assert is_homogeneous(T2)
        assert is_homogeneous(T3)

    def test_is_homogeneous_invalid(self):
        """Test rejection of invalid homogeneous matrices."""
        # Wrong shape
        assert not is_homogeneous(np.eye(3))

        # Wrong bottom row
        T_bad = np.eye(4)
        T_bad[3, 0] = 1
        assert not is_homogeneous(T_bad)

        # Invalid rotation part
        T_bad = np.eye(4)
        T_bad[0, 0] = 2
        assert not is_homogeneous(T_bad)


class TestSO3Class:
    """Test SO3 class functionality."""

    def test_so3_init_default(self):
        """Test SO3 default initialization."""
        R = SO3()
        np.testing.assert_allclose(R.matrix, np.eye(3))

    def test_so3_init_matrix(self):
        """Test SO3 initialization from matrix."""
        matrix = rotx(np.pi/4)
        R = SO3(matrix)
        np.testing.assert_allclose(R.matrix, matrix)

    def test_so3_factory_methods(self):
        """Test SO3 factory methods."""
        R1 = SO3.Rx(np.pi/2)
        R2 = SO3.Ry(np.pi/2)
        R3 = SO3.Rz(np.pi/2)
        R4 = SO3.RPY(0.1, 0.2, 0.3)

        np.testing.assert_allclose(R1.matrix, rotx(np.pi/2), atol=1e-10)
        np.testing.assert_allclose(R2.matrix, roty(np.pi/2), atol=1e-10)
        np.testing.assert_allclose(R3.matrix, rotz(np.pi/2), atol=1e-10)
        np.testing.assert_allclose(R4.matrix, rpy2r(0.1, 0.2, 0.3), atol=1e-10)

    def test_so3_multiplication(self):
        """Test SO3 multiplication (composition)."""
        R1 = SO3.Rx(np.pi/4)
        R2 = SO3.Ry(np.pi/6)
        R3 = R1 * R2

        expected = rotx(np.pi/4) @ roty(np.pi/6)
        np.testing.assert_allclose(R3.matrix, expected)

    def test_so3_inverse(self):
        """Test SO3 inverse."""
        R = SO3.RPY(0.1, 0.2, 0.3)
        R_inv = R.inv()

        identity = R * R_inv
        np.testing.assert_allclose(identity.matrix, np.eye(3), atol=1e-10)

    def test_so3_conversions(self):
        """Test SO3 conversion methods."""
        R = SO3.RPY(0.1, 0.2, 0.3)

        # Test RPY extraction
        rpy = R.rpy()
        np.testing.assert_allclose(rpy, (0.1, 0.2, 0.3), atol=1e-10)

        # Test quaternion conversion
        q = R.quaternion()
        R_from_q = SO3.Quaternion(q)
        np.testing.assert_allclose(R.matrix, R_from_q.matrix, atol=1e-10)


class TestSE3Class:
    """Test SE3 class functionality."""

    def test_se3_init_default(self):
        """Test SE3 default initialization."""
        T = SE3()
        np.testing.assert_allclose(T.matrix, np.eye(4))

    def test_se3_init_matrix(self):
        """Test SE3 initialization from matrix."""
        matrix = transl(1, 2, 3)
        T = SE3(matrix)
        np.testing.assert_allclose(T.matrix, matrix)

    def test_se3_factory_methods(self):
        """Test SE3 factory methods."""
        T1 = SE3.Trans(1, 2, 3)
        T2 = SE3.Rx(np.pi/2)
        T3 = SE3.RPY(0.1, 0.2, 0.3, [1, 2, 3])

        np.testing.assert_allclose(T1.matrix, transl(1, 2, 3))
        np.testing.assert_allclose(T2.matrix, rotmat(rotx(np.pi/2)), atol=1e-10)

        expected_T3 = rotmat(rpy2r(0.1, 0.2, 0.3), [1, 2, 3])
        np.testing.assert_allclose(T3.matrix, expected_T3, atol=1e-10)

    def test_se3_properties(self):
        """Test SE3 property access."""
        R = rotx(0.3)
        t = [1, 2, 3]
        T = SE3.Rt(R, t)

        np.testing.assert_allclose(T.R, R)
        np.testing.assert_allclose(T.t, t)
        assert isinstance(T.rotation, SO3)

    def test_se3_multiplication_composition(self):
        """Test SE3 composition."""
        T1 = SE3.Trans(1, 0, 0)
        T2 = SE3.Rx(np.pi/2)
        T3 = T1 * T2

        expected = transl(1, 0, 0) @ rotmat(rotx(np.pi/2))
        np.testing.assert_allclose(T3.matrix, expected, atol=1e-10)

    def test_se3_multiplication_point(self):
        """Test SE3 point transformation."""
        T = SE3.Trans(1, 2, 3)
        point = [0, 0, 0]
        transformed = T * point

        np.testing.assert_allclose(transformed, [1, 2, 3])

    def test_se3_multiplication_points(self):
        """Test SE3 multiple point transformation."""
        T = SE3.Trans(1, 0, 0)
        points = np.array([[0, 0, 0], [1, 1, 1]])
        transformed = T * points

        expected = np.array([[1, 0, 0], [2, 1, 1]])
        np.testing.assert_allclose(transformed, expected)

    def test_se3_inverse(self):
        """Test SE3 inverse."""
        T = SE3.Trans(1, 2, 3) * SE3.Rx(0.5)
        T_inv = T.inv()

        identity = T * T_inv
        np.testing.assert_allclose(identity.matrix, np.eye(4), atol=1e-10)


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_invalid_rotation_matrix(self):
        """Test error for invalid rotation matrix."""
        bad_matrix = np.ones((3, 3))

        with pytest.raises(ValueError):
            SO3(bad_matrix)

        with pytest.raises(ValueError):
            rotmat(bad_matrix)

    def test_invalid_homogeneous_matrix(self):
        """Test error for invalid homogeneous matrix."""
        bad_matrix = np.ones((4, 4))

        with pytest.raises(ValueError):
            SE3(bad_matrix)

        with pytest.raises(ValueError):
            SE3_from_matrix(bad_matrix)

    def test_wrong_input_shapes(self):
        """Test errors for wrong input shapes."""
        with pytest.raises(ValueError):
            transl([1, 2])  # Wrong vector size

        with pytest.raises(ValueError):
            quat2r([1, 0, 0])  # Wrong quaternion size

        with pytest.raises(ValueError):
            r2rpy(np.eye(2))  # Wrong matrix size


if __name__ == "__main__":
    pytest.main([__file__])
