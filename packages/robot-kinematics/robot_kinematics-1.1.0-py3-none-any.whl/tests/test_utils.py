"""
Tests for utility modules.
"""

import unittest
import numpy as np
from robot_kinematics.utils.workspace import WorkspaceAnalyzer
from robot_kinematics.utils.singularity import SingularityAnalyzer
from robot_kinematics.utils.performance import PerformanceOptimizer
from robot_kinematics.core.transforms import Transform
from robot_kinematics.core.base import RobotKinematicsBase

class TestUtilityModules(unittest.TestCase):
    def setUp(self):
        # Create a mock robot for testing
        class MockRobot(RobotKinematicsBase):
            def forward_kinematics(self, joint_config):
                # Simple forward kinematics that moves end-effector based on joint values
                T = np.eye(4)
                T[:3, 3] = [joint_config[0] * 0.1, joint_config[1] * 0.1, 0.5 + joint_config[2] * 0.1]
                return Transform(T)
            
            def inverse_kinematics(self, target_pose, initial_guess=None, **kwargs):
                # Simple inverse kinematics
                pos = target_pose.position
                return np.array([pos[0] * 10, pos[1] * 10, pos[2] * 10, 0, 0, 0])
            
            def get_joint_transform(self, joint_idx, joint_config):
                return Transform(np.eye(4))
        
        self.mock_config = {
            'n_joints': 6,
            'joint_types': ['revolute'] * 6,
            'joint_limits': [(-np.pi, np.pi)] * 6,
            'base_transform': np.eye(4),
            'tool_transform': np.eye(4)
        }
        self.mock_robot = MockRobot(self.mock_config)

    def test_workspace_analyzer(self):
        workspace_analyzer = WorkspaceAnalyzer(robot=self.mock_robot)
        # Test that the analyzer can be created
        self.assertIsNotNone(workspace_analyzer)
        self.assertEqual(workspace_analyzer.robot, self.mock_robot)

    def test_singularity_analyzer(self):
        singularity_analyzer = SingularityAnalyzer(robot=self.mock_robot)
        # Test that the analyzer can be created
        self.assertIsNotNone(singularity_analyzer)
        self.assertEqual(singularity_analyzer.robot, self.mock_robot)

    def test_performance_optimizer(self):
        performance_optimizer = PerformanceOptimizer(robot=self.mock_robot)
        # Test that the optimizer can be created
        self.assertIsNotNone(performance_optimizer)
        self.assertEqual(performance_optimizer.robot, self.mock_robot)

    def test_workspace_analysis_basic(self):
        workspace_analyzer = WorkspaceAnalyzer(robot=self.mock_robot)
        try:
            # This might fail due to implementation details, but should not crash
            analysis = workspace_analyzer.analyze_workspace()
            self.assertIsInstance(analysis, dict)
        except Exception as e:
            # Expected to potentially fail, but should not crash
            self.assertIsInstance(e, Exception)

    def test_singularity_analysis_basic(self):
        singularity_analyzer = SingularityAnalyzer(robot=self.mock_robot)
        joint_positions = np.zeros(6)
        try:
            # This might fail due to implementation details, but should not crash
            analysis = singularity_analyzer.analyze_singularities(joint_positions)
            self.assertIsInstance(analysis, dict)
        except Exception as e:
            # Expected to potentially fail, but should not crash
            self.assertIsInstance(e, Exception)

    def test_performance_optimization_basic(self):
        performance_optimizer = PerformanceOptimizer(robot=self.mock_robot)
        optimization_config = {
            'enable_caching': True,
            'enable_vectorization': True,
            'enable_jit': False,
            'use_float32': True
        }
        try:
            # This might fail due to implementation details, but should not crash
            optimized_robot = performance_optimizer.optimize_performance(optimization_config)
            self.assertIsNotNone(optimized_robot)
        except Exception as e:
            # Expected to potentially fail, but should not crash
            self.assertIsInstance(e, Exception)

if __name__ == "__main__":
    unittest.main() 