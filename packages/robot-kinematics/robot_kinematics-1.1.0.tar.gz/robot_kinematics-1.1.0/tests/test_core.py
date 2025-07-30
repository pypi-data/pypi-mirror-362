"""
Tests for core modules.
"""

import unittest
import numpy as np
from robot_kinematics.core.exceptions import KinematicsError, SingularityError, ConfigurationError
from robot_kinematics.core.transforms import Transform
from robot_kinematics.core.jacobian import Jacobian
from robot_kinematics.core.base import RobotKinematicsBase

class TestCoreModules(unittest.TestCase):
    def test_exceptions(self):
        with self.assertRaises(KinematicsError):
            raise KinematicsError("Test KinematicsError")
        with self.assertRaises(SingularityError):
            raise SingularityError("Test SingularityError")
        with self.assertRaises(ConfigurationError):
            raise ConfigurationError("Test ConfigurationError")

    def test_transform(self):
        mat = np.eye(4)
        mat[:3, 3] = [1, 2, 3]
        t = Transform(matrix=mat)
        np.testing.assert_array_almost_equal(t.position, [1, 2, 3])
        np.testing.assert_array_almost_equal(t.rotation, np.eye(3))
        t2 = Transform(matrix=np.eye(4))
        t3 = t * t2
        self.assertIsInstance(t3, Transform)
        t_inv = t.inverse()
        self.assertIsInstance(t_inv, Transform)

    def test_jacobian(self):
        # Minimal mock robot
        class MockRobot(RobotKinematicsBase):
            def forward_kinematics(self, joint_config):
                return Transform(np.eye(4))
            def inverse_kinematics(self, target_pose, initial_guess=None, **kwargs):
                return np.zeros(self.n_joints)
            def get_joint_transform(self, joint_idx, joint_config):
                return Transform(np.eye(4))
        config = {
            'n_joints': 6,
            'joint_types': ['revolute'] * 6,
            'joint_limits': [(-np.pi, np.pi)] * 6,
            'base_transform': np.eye(4),
            'tool_transform': np.eye(4)
        }
        robot = MockRobot(config)
        jac = Jacobian(robot, np.zeros(6))
        J = jac.compute()
        self.assertEqual(J.shape, (6, 6))
        self.assertTrue(np.all(np.isfinite(J)))

    def test_robot_kinematics_base(self):
        # Minimal mock robot
        class MockRobot(RobotKinematicsBase):
            def forward_kinematics(self, joint_config):
                return Transform(np.eye(4))
            def inverse_kinematics(self, target_pose, initial_guess=None, **kwargs):
                return np.zeros(self.n_joints)
            def get_joint_transform(self, joint_idx, joint_config):
                return Transform(np.eye(4))
        config = {
            'n_joints': 6,
            'joint_types': ['revolute'] * 6,
            'joint_limits': [(-np.pi, np.pi)] * 6,
            'base_transform': np.eye(4),
            'tool_transform': np.eye(4)
        }
        robot = MockRobot(config)
        self.assertTrue(robot.check_joint_limits(np.zeros(6)))
        clamped = robot.enforce_joint_limits(np.array([10, 0, 0, 0, 0, 0]))
        self.assertTrue(np.all(clamped <= np.pi))

if __name__ == "__main__":
    unittest.main() 