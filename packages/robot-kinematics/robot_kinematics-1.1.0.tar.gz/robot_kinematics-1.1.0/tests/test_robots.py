"""
Tests for robot implementations.
"""

import unittest
import numpy as np
from robot_kinematics.robots.serial import SerialManipulator
from robot_kinematics.robots.parallel import ParallelRobot
from robot_kinematics.robots.mobile import MobileManipulator
from robot_kinematics.core.transforms import Transform

class TestRobotImplementations(unittest.TestCase):
    def test_serial_manipulator(self):
        config = {
            'n_joints': 6,
            'joint_types': ['revolute'] * 6,
            'joint_limits': [(-np.pi, np.pi)] * 6,
            'base_transform': np.eye(4),
            'tool_transform': np.eye(4),
            'dh_parameters': [[0, 0, 0, 0] for _ in range(6)]
        }
        serial_robot = SerialManipulator(config)
        joint_positions = np.zeros(6)
        pose = serial_robot.forward_kinematics(joint_positions)
        self.assertIsInstance(pose, Transform)
        self.assertEqual(pose.matrix.shape, (4, 4))

    def test_parallel_robot(self):
        config = {
            'n_joints': 6,
            'joint_types': ['prismatic'] * 6,
            'joint_limits': [(0, 1)] * 6,
            'base_transform': np.eye(4),
            'tool_transform': np.eye(4)
        }
        parallel_robot = ParallelRobot(config)
        joint_positions = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
        
        # ParallelRobot is a base class that raises NotImplementedError
        # This is expected behavior for the base class
        with self.assertRaises(NotImplementedError):
            pose = parallel_robot.forward_kinematics(joint_positions)

    def test_mobile_manipulator(self):
        config = {
            'n_joints': 8,  # 2 base + 6 manipulator
            'joint_types': ['revolute', 'revolute'] + ['revolute'] * 6,
            'joint_limits': [(-np.pi, np.pi)] * 8,
            'base_transform': np.eye(4),
            'tool_transform': np.eye(4),
            'base_type': 'differential_drive',
            'manipulator_joints': 6
        }
        mobile_robot = MobileManipulator(config)
        joint_positions = np.zeros(8)
        pose = mobile_robot.forward_kinematics(joint_positions)
        self.assertIsInstance(pose, Transform)
        self.assertEqual(pose.matrix.shape, (4, 4))

    def test_robot_joint_limits(self):
        config = {
            'n_joints': 6,
            'joint_types': ['revolute'] * 6,
            'joint_limits': [(-np.pi, np.pi)] * 6,
            'base_transform': np.eye(4),
            'tool_transform': np.eye(4),
            'dh_parameters': [[0, 0, 0, 0] for _ in range(6)]
        }
        serial_robot = SerialManipulator(config)
        
        # Test valid joint positions
        valid_positions = np.zeros(6)
        self.assertTrue(serial_robot.check_joint_limits(valid_positions))
        
        # Test invalid joint positions
        invalid_positions = np.array([2*np.pi, 0, 0, 0, 0, 0])
        self.assertFalse(serial_robot.check_joint_limits(invalid_positions))
        
        # Test joint limit enforcement
        clamped = serial_robot.enforce_joint_limits(invalid_positions)
        self.assertTrue(np.all(clamped <= np.pi))

    def test_robot_jacobian(self):
        config = {
            'n_joints': 6,
            'joint_types': ['revolute'] * 6,
            'joint_limits': [(-np.pi, np.pi)] * 6,
            'base_transform': np.eye(4),
            'tool_transform': np.eye(4),
            'dh_parameters': [[0, 0, 0, 0] for _ in range(6)]
        }
        serial_robot = SerialManipulator(config)
        joint_positions = np.zeros(6)
        jacobian = serial_robot.get_jacobian(joint_positions)
        J = jacobian.compute()
        self.assertEqual(J.shape, (6, 6))
        self.assertTrue(np.all(np.isfinite(J)))

if __name__ == "__main__":
    unittest.main() 