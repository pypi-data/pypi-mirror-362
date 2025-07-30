"""
RobotKinematics: Production-Ready Robotics Kinematics Library

A comprehensive Python library for forward and inverse kinematics calculations
supporting various robot configurations including serial manipulators, parallel robots,
and mobile manipulators.

Author: RobotKinematics Team
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "RobotKinematics Team"
__license__ = "MIT"

# Core imports
from .core.base import RobotKinematicsBase
from .core.transforms import (
    Transform,
    Rotation,
    euler_to_rotation_matrix,
    rotation_matrix_to_euler,
    quaternion_to_rotation_matrix,
    rotation_matrix_to_quaternion,
    axis_angle_to_rotation_matrix,
    rotation_matrix_to_axis_angle,
    pose_interpolation
)
from .core.jacobian import Jacobian
from .core.exceptions import (
    KinematicsError,
    SingularityError,
    JointLimitError,
    ConvergenceError,
    ConfigurationError
)

# Forward kinematics
from .forward.dh_kinematics import DHKinematics
from .forward.urdf_kinematics import URDFKinematics

# Inverse kinematics
from .inverse.analytical import AnalyticalIK
from .inverse.numerical import NumericalIK
from .inverse.hybrid import HybridIK

# Robot implementations
from .robots.serial import SerialManipulator
from .robots.parallel import ParallelRobot
from .robots.mobile import MobileManipulator

# Utilities
from .utils.workspace import WorkspaceAnalyzer
from .utils.singularity import SingularityAnalyzer
from .utils.performance import PerformanceOptimizer

# Convenience functions
def create_robot(robot_type, config):
    """
    Factory function to create robot instances.
    
    Args:
        robot_type (str): Type of robot ('serial', 'parallel', 'mobile')
        config (dict): Robot configuration parameters
        
    Returns:
        RobotKinematicsBase: Configured robot instance
    """
    if robot_type.lower() == 'serial':
        return SerialManipulator(config)
    elif robot_type.lower() == 'parallel':
        return ParallelRobot(config)
    elif robot_type.lower() == 'mobile':
        return MobileManipulator(config)
    else:
        raise ConfigurationError(f"Unknown robot type: {robot_type}")

__all__ = [
    # Core
    'RobotKinematicsBase',
    'Transform',
    'Rotation',
    'Jacobian',
    
    # Transforms
    'euler_to_rotation_matrix',
    'rotation_matrix_to_euler',
    'quaternion_to_rotation_matrix',
    'rotation_matrix_to_quaternion',
    'axis_angle_to_rotation_matrix',
    'rotation_matrix_to_axis_angle',
    'pose_interpolation',
    
    # Forward kinematics
    'DHKinematics',
    'URDFKinematics',
    
    # Inverse kinematics
    'AnalyticalIK',
    'NumericalIK',
    'HybridIK',
    
    # Robots
    'SerialManipulator',
    'ParallelRobot',
    'MobileManipulator',
    
    # Utilities
    'WorkspaceAnalyzer',
    'SingularityAnalyzer',
    'PerformanceOptimizer',
    
    # Exceptions
    'KinematicsError',
    'SingularityError',
    'JointLimitError',
    'ConvergenceError',
    'ConfigurationError',
    
    # Factory function
    'create_robot'
] 