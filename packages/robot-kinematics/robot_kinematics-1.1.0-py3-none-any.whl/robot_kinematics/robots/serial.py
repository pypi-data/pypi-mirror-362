"""
Serial manipulator implementations.

This module provides specific implementations for various serial manipulators
including industrial robots, research platforms, and educational robots.
"""

import numpy as np
from typing import Dict, Any, List, Optional
from ..core.base import RobotKinematicsBase
from ..forward.dh_kinematics import DHKinematics, create_ur5_kinematics, create_panda_kinematics
from ..core.transforms import Transform
from ..core.exceptions import KinematicsError


class SerialManipulator(RobotKinematicsBase):
    """
    Generic serial manipulator implementation.
    
    This class provides a flexible implementation for serial manipulators
    that can be configured with different DH parameters and joint configurations.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize serial manipulator.
        
        Args:
            config: Robot configuration dictionary
        """
        super().__init__(config)
        
        # Create DH kinematics instance
        self.dh_kinematics = DHKinematics(config)
    
    def forward_kinematics(self, joint_config: np.ndarray) -> Transform:
        """Compute forward kinematics."""
        return self.dh_kinematics.forward_kinematics(joint_config)
    
    def inverse_kinematics(self, target_pose: Transform, 
                          initial_guess: Optional[np.ndarray] = None,
                          **kwargs) -> np.ndarray:
        """Compute inverse kinematics."""
        return self.dh_kinematics.inverse_kinematics(target_pose, initial_guess, **kwargs)
    
    def get_joint_transform(self, joint_idx: int, joint_config: np.ndarray) -> Transform:
        """Get transformation to a specific joint."""
        return self.dh_kinematics.get_joint_transform(joint_idx, joint_config)


class UR5Manipulator(SerialManipulator):
    """
    Universal Robots UR5 manipulator.
    
    This class provides a specific implementation for the UR5 robot with
    accurate DH parameters and joint limits.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize UR5 manipulator.
        
        Args:
            config: Optional configuration overrides
        """
        if config is None:
            config = {}
        
        # UR5 default configuration
        ur5_config = {
            'n_joints': 6,
            'joint_types': ['revolute'] * 6,
            'joint_limits': [
                (-2*np.pi, 2*np.pi), (-2*np.pi, 2*np.pi), (-2*np.pi, 2*np.pi),
                (-2*np.pi, 2*np.pi), (-2*np.pi, 2*np.pi), (-2*np.pi, 2*np.pi)
            ],
            'dh_parameters': [
                {'a': 0, 'alpha': np.pi/2, 'd': 0.089159, 'theta': 0},
                {'a': -0.425, 'alpha': 0, 'd': 0, 'theta': 0},
                {'a': -0.39225, 'alpha': 0, 'd': 0, 'theta': 0},
                {'a': 0, 'alpha': np.pi/2, 'd': 0.10915, 'theta': 0},
                {'a': 0, 'alpha': -np.pi/2, 'd': 0.09465, 'theta': 0},
                {'a': 0, 'alpha': 0, 'd': 0.0823, 'theta': 0}
            ],
            'name': 'UR5',
            'manufacturer': 'Universal Robots',
            'payload': 5.0,  # kg
            'reach': 850.0,  # mm
        }
        
        # Update with provided config
        ur5_config.update(config)
        
        super().__init__(ur5_config)
    
    def get_workspace_analysis(self) -> Dict[str, Any]:
        """Get UR5-specific workspace analysis."""
        return {
            'reach': 850.0,  # mm
            'payload': 5.0,  # kg
            'repeatability': 0.1,  # mm
            'workspace_type': 'spherical',
            'base_height': 89.159,  # mm
            'max_speed': 1.0,  # m/s
        }


class PandaManipulator(SerialManipulator):
    """
    Franka Emika Panda manipulator.
    
    This class provides a specific implementation for the Panda robot with
    accurate DH parameters and joint limits.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Panda manipulator.
        
        Args:
            config: Optional configuration overrides
        """
        if config is None:
            config = {}
        
        # Panda default configuration
        panda_config = {
            'n_joints': 7,
            'joint_types': ['revolute'] * 7,
            'joint_limits': [
                (-2.8973, 2.8973), (-1.7628, 1.7628), (-2.8973, 2.8973),
                (-3.0718, -0.0698), (-2.8973, 2.8973), (-0.0175, 3.7525),
                (-2.8973, 2.8973)
            ],
            'dh_parameters': [
                {'a': 0, 'alpha': 0, 'd': 0.333, 'theta': 0},
                {'a': 0, 'alpha': -np.pi/2, 'd': 0, 'theta': 0},
                {'a': 0, 'alpha': np.pi/2, 'd': 0.316, 'theta': 0},
                {'a': 0.0825, 'alpha': np.pi/2, 'd': 0, 'theta': 0},
                {'a': -0.0825, 'alpha': -np.pi/2, 'd': 0.384, 'theta': 0},
                {'a': 0, 'alpha': np.pi/2, 'd': 0, 'theta': 0},
                {'a': 0.088, 'alpha': np.pi/2, 'd': 0.107, 'theta': 0}
            ],
            'name': 'Panda',
            'manufacturer': 'Franka Emika',
            'payload': 3.0,  # kg
            'reach': 855.0,  # mm
        }
        
        # Update with provided config
        panda_config.update(config)
        
        super().__init__(panda_config)
    
    def get_workspace_analysis(self) -> Dict[str, Any]:
        """Get Panda-specific workspace analysis."""
        return {
            'reach': 855.0,  # mm
            'payload': 3.0,  # kg
            'repeatability': 0.1,  # mm
            'workspace_type': 'spherical',
            'base_height': 333.0,  # mm
            'max_speed': 2.0,  # m/s
            'redundant': True,  # 7-DOF redundant manipulator
        }


class SCARAManipulator(SerialManipulator):
    """
    SCARA (Selective Compliance Assembly Robot Arm) manipulator.
    
    This class provides an implementation for SCARA robots with
    typical DH parameters and joint limits.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize SCARA manipulator.
        
        Args:
            config: Optional configuration overrides
        """
        if config is None:
            config = {}
        
        # SCARA default configuration
        scara_config = {
            'n_joints': 4,
            'joint_types': ['revolute', 'revolute', 'prismatic', 'revolute'],
            'joint_limits': [
                (-np.pi, np.pi), (-np.pi, np.pi), (0.0, 0.3), (-np.pi, np.pi)
            ],
            'dh_parameters': [
                {'a': 0.4, 'alpha': 0, 'd': 0, 'theta': 0},  # Link 1
                {'a': 0.3, 'alpha': 0, 'd': 0, 'theta': 0},  # Link 2
                {'a': 0, 'alpha': 0, 'd': 0, 'theta': 0},    # Prismatic joint
                {'a': 0, 'alpha': 0, 'd': 0.1, 'theta': 0},  # End effector
            ],
            'name': 'SCARA',
            'manufacturer': 'Generic',
            'payload': 10.0,  # kg
            'reach': 700.0,  # mm
        }
        
        # Update with provided config
        scara_config.update(config)
        
        super().__init__(scara_config)
    
    def get_workspace_analysis(self) -> Dict[str, Any]:
        """Get SCARA-specific workspace analysis."""
        return {
            'reach': 700.0,  # mm
            'payload': 10.0,  # kg
            'repeatability': 0.02,  # mm (high precision)
            'workspace_type': 'cylindrical',
            'base_height': 0.0,  # mm
            'max_speed': 1.5,  # m/s
            'planar': True,  # Planar motion
        }


class DeltaRobot(SerialManipulator):
    """
    Delta robot (parallel manipulator with serial-like interface).
    
    This class provides an implementation for Delta robots with
    simplified kinematics for the end-effector.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Delta robot.
        
        Args:
            config: Optional configuration overrides
        """
        if config is None:
            config = {}
        
        # Delta robot default configuration
        delta_config = {
            'n_joints': 3,
            'joint_types': ['revolute'] * 3,
            'joint_limits': [
                (-np.pi/3, np.pi/3), (-np.pi/3, np.pi/3), (-np.pi/3, np.pi/3)
            ],
            'dh_parameters': [
                {'a': 0.2, 'alpha': 0, 'd': 0, 'theta': 0},  # Arm 1
                {'a': 0.2, 'alpha': 0, 'd': 0, 'theta': 2*np.pi/3},  # Arm 2
                {'a': 0.2, 'alpha': 0, 'd': 0, 'theta': 4*np.pi/3},  # Arm 3
            ],
            'name': 'Delta',
            'manufacturer': 'Generic',
            'payload': 1.0,  # kg
            'reach': 300.0,  # mm
        }
        
        # Update with provided config
        delta_config.update(config)
        
        super().__init__(delta_config)
    
    def forward_kinematics(self, joint_config: np.ndarray) -> Transform:
        """
        Compute forward kinematics for Delta robot.
        
        This is a simplified implementation. Real Delta robots require
        more complex parallel kinematics calculations.
        """
        # Simplified FK for Delta robot
        # In practice, this would involve solving the parallel kinematics
        
        # For now, use a simplified approach
        theta1, theta2, theta3 = joint_config
        
        # Simplified position calculation
        x = 0.1 * (np.cos(theta1) + np.cos(theta2) + np.cos(theta3))
        y = 0.1 * (np.sin(theta1) + np.sin(theta2) + np.sin(theta3))
        z = 0.3 - 0.1 * (np.sin(theta1) + np.sin(theta2) + np.sin(theta3))
        
        # Create transformation matrix
        T = np.eye(4)
        T[:3, 3] = [x, y, z]
        
        return Transform(T)
    
    def get_workspace_analysis(self) -> Dict[str, Any]:
        """Get Delta-specific workspace analysis."""
        return {
            'reach': 300.0,  # mm
            'payload': 1.0,  # kg
            'repeatability': 0.01,  # mm (very high precision)
            'workspace_type': 'spherical',
            'base_height': 0.0,  # mm
            'max_speed': 5.0,  # m/s (very fast)
            'parallel': True,  # Parallel manipulator
        }


class KUKAKR5Manipulator(SerialManipulator):
    """
    KUKA KR5 sixx 850 industrial manipulator.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        if config is None:
            config = {}
        # KUKA KR5 DH parameters (approximate, for demonstration)
        kr5_config = {
            'n_joints': 6,
            'joint_types': ['revolute'] * 6,
            'joint_limits': [
                (-2.967, 2.967), (-2.094, 2.094), (-2.967, 2.967),
                (-2.094, 2.094), (-2.967, 2.967), (-2.094, 2.094)
            ],
            'dh_parameters': [
                {'a': 0,      'alpha': np.pi/2,  'd': 0.400,   'theta': 0},
                {'a': 0.180,  'alpha': 0,        'd': 0,       'theta': 0},
                {'a': 0.600,  'alpha': 0,        'd': 0,       'theta': 0},
                {'a': 0.120,  'alpha': np.pi/2,  'd': 0.620,   'theta': 0},
                {'a': 0,      'alpha': -np.pi/2, 'd': 0,       'theta': 0},
                {'a': 0,      'alpha': 0,        'd': 0.115,   'theta': 0}
            ],
            'name': 'KUKA_KR5',
            'manufacturer': 'KUKA',
            'payload': 5.0,  # kg
            'reach': 855.0,  # mm
        }
        kr5_config.update(config)
        super().__init__(kr5_config)
    def get_workspace_analysis(self) -> Dict[str, Any]:
        return {
            'reach': 855.0,  # mm
            'payload': 5.0,  # kg
            'repeatability': 0.1,  # mm
            'workspace_type': 'spherical',
            'base_height': 400.0,  # mm
            'max_speed': 2.0,  # m/s
        }


# Factory functions for creating robot instances
def create_ur5() -> UR5Manipulator:
    """Create UR5 robot instance."""
    return UR5Manipulator()


def create_panda() -> PandaManipulator:
    """Create Panda robot instance."""
    return PandaManipulator()


def create_scara() -> SCARAManipulator:
    """Create SCARA robot instance."""
    return SCARAManipulator()


def create_delta() -> DeltaRobot:
    """Create Delta robot instance."""
    return DeltaRobot()


def create_serial_manipulator(robot_type: str, **kwargs) -> SerialManipulator:
    """
    Factory function to create serial manipulators.
    
    Args:
        robot_type: Type of robot ('ur5', 'panda', 'scara', 'delta', 'kuka_kr5')
        **kwargs: Additional configuration parameters
        
    Returns:
        Serial manipulator instance
    """
    robot_type = robot_type.lower()
    
    if robot_type == 'ur5':
        return UR5Manipulator(kwargs)
    elif robot_type == 'panda':
        return PandaManipulator(kwargs)
    elif robot_type == 'scara':
        return SCARAManipulator(kwargs)
    elif robot_type == 'delta':
        return DeltaRobot(kwargs)
    elif robot_type == 'kuka_kr5':
        return KUKAKR5Manipulator(kwargs)
    else:
        raise ValueError(f"Unknown robot type: {robot_type}")


# Robot registry for easy access
ROBOT_REGISTRY = {
    'ur5': UR5Manipulator,
    'panda': PandaManipulator,
    'scara': SCARAManipulator,
    'delta': DeltaRobot,
}

def create_kuka_kr5() -> KUKAKR5Manipulator:
    """Create KUKA KR5 robot instance."""
    return KUKAKR5Manipulator()

# Add to factory and registry
ROBOT_REGISTRY['kuka_kr5'] = KUKAKR5Manipulator


def get_available_robots() -> List[str]:
    """Get list of available robot types."""
    return list(ROBOT_REGISTRY.keys())


def create_robot_from_registry(robot_type: str, **kwargs) -> SerialManipulator:
    """
    Create robot from registry.
    
    Args:
        robot_type: Type of robot
        **kwargs: Configuration parameters
        
    Returns:
        Robot instance
    """
    if robot_type not in ROBOT_REGISTRY:
        raise ValueError(f"Robot type '{robot_type}' not found. Available: {get_available_robots()}")
    
    return ROBOT_REGISTRY[robot_type](**kwargs) 