"""
Base classes for robotics kinematics.

This module provides the abstract base class for all robot kinematics implementations.
"""

import numpy as np
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any
import threading
from .transforms import Transform
from .jacobian import Jacobian
from .exceptions import KinematicsError, JointLimitError, ConfigurationError


class RobotKinematicsBase(ABC):
    """
    Abstract base class for robot kinematics implementations.
    
    This class defines the interface that all robot kinematics implementations
    must follow, providing common functionality for forward and inverse kinematics.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize robot kinematics.
        
        Args:
            config: Robot configuration dictionary
        """
        self.config = config
        self.n_joints = config.get('n_joints', 0)
        self.joint_types = config.get('joint_types', [])
        self.joint_limits = config.get('joint_limits', [])
        self.base_transform = Transform(config.get('base_transform', np.eye(4)))
        self.tool_transform = Transform(config.get('tool_transform', np.eye(4)))
        
        # Thread safety
        self._lock = threading.Lock()
        self._transforms_cache = {}
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate robot configuration."""
        if self.n_joints <= 0:
            raise ConfigurationError("Number of joints must be positive")
        
        if len(self.joint_types) != self.n_joints:
            raise ConfigurationError("Joint types must match number of joints")
        
        if len(self.joint_limits) != self.n_joints:
            raise ConfigurationError("Joint limits must match number of joints")
        
        # Validate joint types
        valid_types = {'revolute', 'prismatic'}
        for i, joint_type in enumerate(self.joint_types):
            if joint_type not in valid_types:
                raise ConfigurationError(f"Invalid joint type at joint {i}: {joint_type}")
        
        # Validate joint limits
        for i, (min_val, max_val) in enumerate(self.joint_limits):
            if min_val >= max_val:
                raise ConfigurationError(f"Invalid joint limits at joint {i}: {min_val} >= {max_val}")
    
    @abstractmethod
    def forward_kinematics(self, joint_config: np.ndarray) -> Transform:
        """
        Compute forward kinematics.
        
        Args:
            joint_config: Joint configuration vector
            
        Returns:
            End-effector pose
        """
        pass
    
    @abstractmethod
    def inverse_kinematics(self, target_pose: Transform, 
                          initial_guess: Optional[np.ndarray] = None,
                          **kwargs) -> np.ndarray:
        """
        Compute inverse kinematics.
        
        Args:
            target_pose: Target end-effector pose
            initial_guess: Initial joint configuration guess
            **kwargs: Additional solver parameters
            
        Returns:
            Joint configuration
        """
        pass
    
    @abstractmethod
    def get_joint_transform(self, joint_idx: int, joint_config: np.ndarray) -> Transform:
        """
        Get transformation to a specific joint.
        
        Args:
            joint_idx: Joint index
            joint_config: Joint configuration vector
            
        Returns:
            Transformation to joint
        """
        pass
    
    def check_joint_limits(self, joint_config: np.ndarray) -> bool:
        """
        Check if joint configuration is within limits.
        
        Args:
            joint_config: Joint configuration vector
            
        Returns:
            True if within limits
        """
        joint_config = np.asarray(joint_config).flatten()
        
        for i, (q, (min_val, max_val)) in enumerate(zip(joint_config, self.joint_limits)):
            if q < min_val or q > max_val:
                return False
        
        return True
    
    def enforce_joint_limits(self, joint_config: np.ndarray) -> np.ndarray:
        """
        Enforce joint limits by clamping values.
        
        Args:
            joint_config: Joint configuration vector
            
        Returns:
            Clamped joint configuration
        """
        joint_config = np.asarray(joint_config).flatten()
        clamped = np.zeros_like(joint_config)
        
        for i, (q, (min_val, max_val)) in enumerate(zip(joint_config, self.joint_limits)):
            clamped[i] = np.clip(q, min_val, max_val)
        
        return clamped
    
    def get_jacobian(self, joint_config: np.ndarray) -> Jacobian:
        """
        Get Jacobian for current configuration.
        
        Args:
            joint_config: Joint configuration vector
            
        Returns:
            Jacobian instance
        """
        return Jacobian(self, joint_config)
    
    def velocity_kinematics(self, joint_config: np.ndarray, 
                           joint_velocities: np.ndarray) -> np.ndarray:
        """
        Compute forward velocity kinematics.
        
        Args:
            joint_config: Joint configuration vector
            joint_velocities: Joint velocities
            
        Returns:
            End-effector velocity [linear, angular]
        """
        jacobian = self.get_jacobian(joint_config)
        return jacobian.compute() @ joint_velocities
    
    def inverse_velocity_kinematics(self, joint_config: np.ndarray,
                                   end_effector_velocity: np.ndarray,
                                   damping: float = 0.0) -> np.ndarray:
        """
        Compute inverse velocity kinematics.
        
        Args:
            joint_config: Joint configuration vector
            end_effector_velocity: End-effector velocity [linear, angular]
            damping: Damping factor for singularity handling
            
        Returns:
            Joint velocities
        """
        jacobian = self.get_jacobian(joint_config)
        return jacobian.redundancy_resolution(end_effector_velocity, damping=damping)
    
    def batch_forward_kinematics(self, joint_configs: np.ndarray) -> List[Transform]:
        """
        Compute forward kinematics for multiple configurations.
        
        Args:
            joint_configs: Array of joint configurations (N x n_joints)
            
        Returns:
            List of end-effector poses
        """
        joint_configs = np.asarray(joint_configs)
        if joint_configs.ndim == 1:
            joint_configs = joint_configs.reshape(1, -1)
        
        poses = []
        for config in joint_configs:
            poses.append(self.forward_kinematics(config))
        
        return poses
    
    def workspace_analysis(self, n_samples: int = 1000) -> Dict[str, Any]:
        """
        Analyze robot workspace.
        
        Args:
            n_samples: Number of random samples
            
        Returns:
            Workspace analysis results
        """
        positions = []
        manipulabilities = []
        
        for _ in range(n_samples):
            # Random joint configuration within limits
            q = np.array([
                np.random.uniform(lim[0], lim[1]) for lim in self.joint_limits
            ])
            
            # Check if configuration is valid
            if not self.check_joint_limits(q):
                continue
            
            try:
                pose = self.forward_kinematics(q)
                positions.append(pose.position)
                
                # Compute manipulability
                jacobian = self.get_jacobian(q)
                manipulabilities.append(jacobian.manipulability())
            except KinematicsError:
                continue
        
        if not positions:
            return {'error': 'No valid configurations found'}
        
        positions = np.array(positions)
        
        return {
            'positions': positions,
            'manipulabilities': manipulabilities,
            'workspace_volume': self._compute_workspace_volume(positions),
            'reachable_range': {
                'x': (np.min(positions[:, 0]), np.max(positions[:, 0])),
                'y': (np.min(positions[:, 1]), np.max(positions[:, 1])),
                'z': (np.min(positions[:, 2]), np.max(positions[:, 2]))
            },
            'mean_manipulability': np.mean(manipulabilities),
            'std_manipulability': np.std(manipulabilities)
        }
    
    def _compute_workspace_volume(self, positions: np.ndarray) -> float:
        """Compute approximate workspace volume using convex hull."""
        try:
            from scipy.spatial import ConvexHull
            hull = ConvexHull(positions)
            return hull.volume
        except ImportError:
            # Fallback: bounding box volume
            ranges = np.ptp(positions, axis=0)
            return np.prod(ranges)
    
    def get_robot_info(self) -> Dict[str, Any]:
        """
        Get robot information.
        
        Returns:
            Robot information dictionary
        """
        return {
            'n_joints': self.n_joints,
            'joint_types': self.joint_types,
            'joint_limits': self.joint_limits,
            'base_transform': self.base_transform.matrix,
            'tool_transform': self.tool_transform.matrix,
            'robot_type': self.__class__.__name__
        }
    
    def __str__(self) -> str:
        info = self.get_robot_info()
        return f"{info['robot_type']}(n_joints={info['n_joints']})"
    
    def __repr__(self) -> str:
        return self.__str__()


class RobotConfig:
    """Configuration class for robot parameters."""
    
    def __init__(self, **kwargs):
        """
        Initialize robot configuration.
        
        Args:
            **kwargs: Configuration parameters
        """
        self.params = kwargs
    
    def __getitem__(self, key: str) -> Any:
        return self.params[key]
    
    def __setitem__(self, key: str, value: Any):
        self.params[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.params.get(key, default)
    
    def update(self, other: Dict[str, Any]):
        self.params.update(other)
    
    def to_dict(self) -> Dict[str, Any]:
        return self.params.copy()
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'RobotConfig':
        return cls(**config_dict)
    
    @classmethod
    def from_file(cls, file_path: str) -> 'RobotConfig':
        """Load configuration from file."""
        import yaml
        with open(file_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return cls.from_dict(config_dict)
    
    def save_to_file(self, file_path: str):
        """Save configuration to file."""
        import yaml
        with open(file_path, 'w') as f:
            yaml.dump(self.params, f, default_flow_style=False) 