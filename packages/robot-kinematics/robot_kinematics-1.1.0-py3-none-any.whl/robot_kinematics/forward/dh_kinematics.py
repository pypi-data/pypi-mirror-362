"""
Denavit-Hartenberg (DH) parameter-based forward kinematics.

This module implements forward kinematics using DH parameters for serial manipulators.
"""

import numpy as np
from typing import List, Tuple, Optional, Dict, Any
import threading
from ..core.base import RobotKinematicsBase
from ..core.transforms import Transform
from ..core.exceptions import KinematicsError, ConfigurationError


class DHParameters:
    """Denavit-Hartenberg parameters for a joint."""
    
    def __init__(self, a: float, alpha: float, d: float, theta: float, 
                 joint_type: str = 'revolute', offset: float = 0.0):
        """
        Initialize DH parameters.
        
        Args:
            a: Link length
            alpha: Link twist
            d: Link offset
            theta: Joint angle
            joint_type: 'revolute' or 'prismatic'
            offset: Joint offset
        """
        self.a = a
        self.alpha = alpha
        self.d = d
        self.theta = theta
        self.joint_type = joint_type
        self.offset = offset
    
    def get_transform(self, joint_value: float) -> np.ndarray:
        """
        Get homogeneous transformation matrix for given joint value.
        
        Args:
            joint_value: Joint value (angle for revolute, distance for prismatic)
            
        Returns:
            4x4 homogeneous transformation matrix
        """
        if self.joint_type == 'revolute':
            theta = self.theta + joint_value + self.offset
            d = self.d
        else:  # prismatic
            theta = self.theta + self.offset
            d = self.d + joint_value
        
        # Pre-compute trigonometric values
        ct = np.cos(theta)
        st = np.sin(theta)
        ca = np.cos(self.alpha)
        sa = np.sin(self.alpha)
        
        # DH transformation matrix
        T = np.array([
            [ct, -st*ca, st*sa, self.a*ct],
            [st, ct*ca, -ct*sa, self.a*st],
            [0, sa, ca, d],
            [0, 0, 0, 1]
        ])
        
        return T
    
    def __str__(self) -> str:
        return f"DH(a={self.a:.3f}, α={self.alpha:.3f}, d={self.d:.3f}, θ={self.theta:.3f}, type={self.joint_type})"


class DHKinematics(RobotKinematicsBase):
    """
    Forward kinematics using Denavit-Hartenberg parameters.
    
    This class implements forward kinematics for serial manipulators using
    the standard DH convention.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize DH kinematics.
        
        Args:
            config: Configuration dictionary with DH parameters
        """
        super().__init__(config)
        
        # Parse DH parameters
        self.dh_params = self._parse_dh_parameters(config)
        
        # Pre-compute trigonometric tables for efficiency
        self._trig_cache = {}
        self._cache_lock = threading.Lock()
    
    def _parse_dh_parameters(self, config: Dict[str, Any]) -> List[DHParameters]:
        """Parse DH parameters from configuration."""
        dh_data = config.get('dh_parameters', [])
        
        if len(dh_data) != self.n_joints:
            raise ConfigurationError(f"Number of DH parameters ({len(dh_data)}) must match number of joints ({self.n_joints})")
        
        dh_params = []
        for i, params in enumerate(dh_data):
            if isinstance(params, dict):
                dh_param = DHParameters(
                    a=params.get('a', 0.0),
                    alpha=params.get('alpha', 0.0),
                    d=params.get('d', 0.0),
                    theta=params.get('theta', 0.0),
                    joint_type=params.get('joint_type', 'revolute'),
                    offset=params.get('offset', 0.0)
                )
            elif isinstance(params, (list, tuple)) and len(params) >= 4:
                dh_param = DHParameters(
                    a=params[0],
                    alpha=params[1],
                    d=params[2],
                    theta=params[3],
                    joint_type=params[4] if len(params) > 4 else 'revolute',
                    offset=params[5] if len(params) > 5 else 0.0
                )
            else:
                raise ConfigurationError(f"Invalid DH parameters format at joint {i}")
            
            dh_params.append(dh_param)
        
        return dh_params
    
    def forward_kinematics(self, joint_config: np.ndarray) -> Transform:
        """
        Compute forward kinematics using DH parameters.
        
        Args:
            joint_config: Joint configuration vector
            
        Returns:
            End-effector pose
        """
        joint_config = np.asarray(joint_config).flatten()
        
        if len(joint_config) != self.n_joints:
            raise KinematicsError(f"Joint configuration length ({len(joint_config)}) must match number of joints ({self.n_joints})")
        
        # Check joint limits
        if not self.check_joint_limits(joint_config):
            raise KinematicsError("Joint configuration violates joint limits")
        
        # Start with base transformation
        T = self.base_transform.matrix.copy()
        
        # Apply transformations for each joint
        for i, (q, dh_param) in enumerate(zip(joint_config, self.dh_params)):
            T_joint = dh_param.get_transform(q)
            T = T @ T_joint
        
        # Apply tool transformation
        T = T @ self.tool_transform.matrix
        
        return Transform(T)
    
    def get_joint_transform(self, joint_idx: int, joint_config: np.ndarray) -> Transform:
        """
        Get transformation to a specific joint.
        
        Args:
            joint_idx: Joint index
            joint_config: Joint configuration vector
            
        Returns:
            Transformation to joint
        """
        if joint_idx < 0 or joint_idx >= self.n_joints:
            raise KinematicsError(f"Invalid joint index: {joint_idx}")
        
        joint_config = np.asarray(joint_config).flatten()
        
        # Start with base transformation
        T = self.base_transform.matrix.copy()
        
        # Apply transformations up to the specified joint
        for i in range(joint_idx + 1):
            q = joint_config[i]
            dh_param = self.dh_params[i]
            T_joint = dh_param.get_transform(q)
            T = T @ T_joint
        
        return Transform(T)
    
    def inverse_kinematics(self, target_pose: Transform, 
                          initial_guess: Optional[np.ndarray] = None,
                          **kwargs) -> np.ndarray:
        """
        Compute inverse kinematics (delegates to numerical solver).
        
        Args:
            target_pose: Target end-effector pose
            initial_guess: Initial joint configuration guess
            **kwargs: Additional solver parameters
            
        Returns:
            Joint configuration
        """
        # This is a placeholder - actual IK is implemented in inverse/ module
        from ..inverse.numerical import NumericalIK
        ik_solver = NumericalIK(self)
        return ik_solver.solve(target_pose, initial_guess, **kwargs)
    
    def get_dh_parameters(self) -> List[DHParameters]:
        """Get DH parameters."""
        return self.dh_params.copy()
    
    def set_dh_parameters(self, dh_params: List[DHParameters]):
        """Set DH parameters."""
        if len(dh_params) != self.n_joints:
            raise ConfigurationError(f"Number of DH parameters must match number of joints")
        self.dh_params = dh_params.copy()
        self._clear_cache()
    
    def _clear_cache(self):
        """Clear transformation cache."""
        with self._cache_lock:
            self._transforms_cache.clear()
    
    def get_robot_info(self) -> Dict[str, Any]:
        """Get robot information including DH parameters."""
        info = super().get_robot_info()
        info['dh_parameters'] = [str(dh) for dh in self.dh_params]
        return info


class ModifiedDHKinematics(DHKinematics):
    """
    Forward kinematics using modified Denavit-Hartenberg parameters.
    
    This class implements forward kinematics using the modified DH convention,
    which is commonly used in robotics literature.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize modified DH kinematics.
        
        Args:
            config: Configuration dictionary with modified DH parameters
        """
        super().__init__(config)
    
    def _parse_dh_parameters(self, config: Dict[str, Any]) -> List[DHParameters]:
        """Parse modified DH parameters from configuration."""
        dh_data = config.get('modified_dh_parameters', config.get('dh_parameters', []))
        
        if len(dh_data) != self.n_joints:
            raise ConfigurationError(f"Number of DH parameters ({len(dh_data)}) must match number of joints ({self.n_joints})")
        
        dh_params = []
        for i, params in enumerate(dh_data):
            if isinstance(params, dict):
                dh_param = DHParameters(
                    a=params.get('a', 0.0),
                    alpha=params.get('alpha', 0.0),
                    d=params.get('d', 0.0),
                    theta=params.get('theta', 0.0),
                    joint_type=params.get('joint_type', 'revolute'),
                    offset=params.get('offset', 0.0)
                )
            elif isinstance(params, (list, tuple)) and len(params) >= 4:
                dh_param = DHParameters(
                    a=params[0],
                    alpha=params[1],
                    d=params[2],
                    theta=params[3],
                    joint_type=params[4] if len(params) > 4 else 'revolute',
                    offset=params[5] if len(params) > 5 else 0.0
                )
            else:
                raise ConfigurationError(f"Invalid DH parameters format at joint {i}")
            
            dh_params.append(dh_param)
        
        return dh_params
    
    def forward_kinematics(self, joint_config: np.ndarray) -> Transform:
        """
        Compute forward kinematics using modified DH parameters.
        
        Args:
            joint_config: Joint configuration vector
            
        Returns:
            End-effector pose
        """
        joint_config = np.asarray(joint_config).flatten()
        
        if len(joint_config) != self.n_joints:
            raise KinematicsError(f"Joint configuration length ({len(joint_config)}) must match number of joints ({self.n_joints})")
        
        # Check joint limits
        if not self.check_joint_limits(joint_config):
            raise KinematicsError("Joint configuration violates joint limits")
        
        # Start with base transformation
        T = self.base_transform.matrix.copy()
        
        # Apply transformations for each joint using modified DH convention
        for i, (q, dh_param) in enumerate(zip(joint_config, self.dh_params)):
            T_joint = self._modified_dh_transform(dh_param, q)
            T = T @ T_joint
        
        # Apply tool transformation
        T = T @ self.tool_transform.matrix
        
        return Transform(T)
    
    def _modified_dh_transform(self, dh_param: DHParameters, joint_value: float) -> np.ndarray:
        """
        Get modified DH transformation matrix.
        
        Args:
            dh_param: DH parameters
            joint_value: Joint value
            
        Returns:
            4x4 homogeneous transformation matrix
        """
        if dh_param.joint_type == 'revolute':
            theta = dh_param.theta + joint_value + dh_param.offset
            d = dh_param.d
        else:  # prismatic
            theta = dh_param.theta + dh_param.offset
            d = dh_param.d + joint_value
        
        # Pre-compute trigonometric values
        ct = np.cos(theta)
        st = np.sin(theta)
        ca = np.cos(dh_param.alpha)
        sa = np.sin(dh_param.alpha)
        
        # Modified DH transformation matrix
        T = np.array([
            [ct, -st*ca, st*sa, dh_param.a*ct],
            [st, ct*ca, -ct*sa, dh_param.a*st],
            [0, sa, ca, d],
            [0, 0, 0, 1]
        ])
        
        return T


# Factory functions for common robot configurations
def create_ur5_kinematics() -> DHKinematics:
    """Create UR5 robot kinematics."""
    config = {
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
        ]
    }
    return DHKinematics(config)


def create_panda_kinematics() -> DHKinematics:
    """Create Panda robot kinematics."""
    config = {
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
        ]
    }
    return DHKinematics(config) 