"""
Jacobian calculations for robotics kinematics.

This module provides tools for computing geometric and analytical Jacobians,
including singularity analysis and redundancy resolution.
"""

import numpy as np
from typing import List, Tuple, Optional, Union
from abc import ABC, abstractmethod
import threading
from .transforms import Transform
from .exceptions import SingularityError, KinematicsError


class Jacobian:
    """Geometric Jacobian for robotic manipulators."""
    
    def __init__(self, robot, joint_config: np.ndarray):
        """
        Initialize Jacobian for given robot and joint configuration.
        
        Args:
            robot: Robot instance
            joint_config: Joint configuration vector
        """
        self.robot = robot
        self.joint_config = np.asarray(joint_config).flatten()
        self._jacobian_matrix = None
        self._computed = False
        self._lock = threading.Lock()
    
    def compute(self) -> np.ndarray:
        """
        Compute the geometric Jacobian.
        
        Returns:
            6xN Jacobian matrix (N = number of joints)
        """
        with self._lock:
            if not self._computed:
                self._jacobian_matrix = self._compute_jacobian()
                self._computed = True
            return self._jacobian_matrix.copy()
    
    def _compute_jacobian(self) -> np.ndarray:
        """Compute the geometric Jacobian matrix."""
        n_joints = len(self.joint_config)
        J = np.zeros((6, n_joints))
        
        # Get current end-effector pose
        T_end = self.robot.forward_kinematics(self.joint_config)
        p_end = T_end.position
        
        # Compute Jacobian columns for each joint
        for i in range(n_joints):
            # Get transformation to joint i
            T_i = self.robot.get_joint_transform(i, self.joint_config)
            z_i = T_i.rotation[:, 2]  # Z-axis of joint i
            
            if self.robot.joint_types[i] == 'revolute':
                # Revolute joint: linear and angular components
                p_i = T_i.position
                J[:3, i] = np.cross(z_i, p_end - p_i)  # Linear velocity
                J[3:, i] = z_i  # Angular velocity
            else:
                # Prismatic joint: only linear component
                J[:3, i] = z_i  # Linear velocity
                J[3:, i] = np.zeros(3)  # No angular velocity
        
        return J
    
    @property
    def matrix(self) -> np.ndarray:
        """Get the Jacobian matrix."""
        return self.compute()
    
    def condition_number(self) -> float:
        """
        Compute the condition number of the Jacobian.
        
        Returns:
            Condition number (higher values indicate closer to singularity)
        """
        J = self.compute()
        if J.shape[0] != J.shape[1]:
            # For non-square Jacobians, use singular values
            U, s, Vt = np.linalg.svd(J)
            if np.min(s) < 1e-10:
                return np.inf
            return np.max(s) / np.min(s)
        else:
            # For square Jacobians, use determinant-based condition number
            det = np.linalg.det(J)
            if abs(det) < 1e-10:
                return np.inf
            return np.linalg.cond(J)
    
    def manipulability(self) -> float:
        """
        Compute the manipulability index.
        
        Returns:
            Manipulability index (higher values indicate better dexterity)
        """
        J = self.compute()
        return np.sqrt(np.linalg.det(J @ J.T))
    
    def distance_to_singularity(self) -> float:
        """
        Compute distance to nearest singularity.
        
        Returns:
            Distance metric (smaller values indicate closer to singularity)
        """
        J = self.compute()
        U, s, Vt = np.linalg.svd(J)
        return np.min(s)
    
    def is_singular(self, threshold: float = 1e-6) -> bool:
        """
        Check if the current configuration is singular.
        
        Args:
            threshold: Singularity threshold
            
        Returns:
            True if singular
        """
        return self.distance_to_singularity() < threshold
    
    def pseudo_inverse(self, damping: float = 0.0) -> np.ndarray:
        """
        Compute the pseudo-inverse of the Jacobian.
        
        Args:
            damping: Damping factor for singularity robustness
            
        Returns:
            Pseudo-inverse matrix
        """
        J = self.compute()
        
        if damping > 0:
            # Damped least squares
            J_damped = J.T @ (J @ J.T + damping * np.eye(J.shape[0]))
            return J_damped
        else:
            # Standard pseudo-inverse
            return np.linalg.pinv(J)
    
    def redundancy_resolution(self, primary_task: np.ndarray, 
                            secondary_task: Optional[np.ndarray] = None,
                            damping: float = 0.0) -> np.ndarray:
        """
        Perform redundancy resolution.
        
        Args:
            primary_task: Primary task velocity (6D)
            secondary_task: Secondary task velocity (N-dimensional)
            damping: Damping factor
            
        Returns:
            Joint velocities
        """
        J = self.compute()
        J_pinv = self.pseudo_inverse(damping)
        
        # Primary task
        q_dot_primary = J_pinv @ primary_task
        
        if secondary_task is not None:
            # Add secondary task in null space
            N = np.eye(J.shape[1]) - J_pinv @ J
            q_dot_secondary = N @ secondary_task
            return q_dot_primary + q_dot_secondary
        
        return q_dot_primary


class AnalyticalJacobian:
    """Analytical Jacobian for different orientation representations."""
    
    def __init__(self, geometric_jacobian: Jacobian, orientation_repr: str = 'quaternion'):
        """
        Initialize analytical Jacobian.
        
        Args:
            geometric_jacobian: Geometric Jacobian instance
            orientation_repr: Orientation representation ('quaternion', 'euler', 'axis_angle')
        """
        self.geometric_jacobian = geometric_jacobian
        self.orientation_repr = orientation_repr
        self._analytical_jacobian = None
        self._computed = False
    
    def compute(self) -> np.ndarray:
        """
        Compute the analytical Jacobian.
        
        Returns:
            Analytical Jacobian matrix
        """
        if not self._computed:
            J_geo = self.geometric_jacobian.compute()
            T_end = self.geometric_jacobian.robot.forward_kinematics(
                self.geometric_jacobian.joint_config
            )
            
            # Position part remains the same
            J_pos = J_geo[:3, :]
            
            # Orientation part depends on representation
            if self.orientation_repr == 'quaternion':
                J_ori = self._quaternion_jacobian(J_geo[3:, :], T_end.rotation)
            elif self.orientation_repr == 'euler':
                J_ori = self._euler_jacobian(J_geo[3:, :], T_end.rotation)
            elif self.orientation_repr == 'axis_angle':
                J_ori = self._axis_angle_jacobian(J_geo[3:, :], T_end.rotation)
            else:
                raise KinematicsError(f"Unsupported orientation representation: {self.orientation_repr}")
            
            self._analytical_jacobian = np.vstack([J_pos, J_ori])
            self._computed = True
        
        return self._analytical_jacobian.copy()
    
    def _quaternion_jacobian(self, J_omega: np.ndarray, R: np.ndarray) -> np.ndarray:
        """Compute quaternion Jacobian."""
        # Convert rotation matrix to quaternion
        from .transforms import rotation_matrix_to_quaternion
        q = rotation_matrix_to_quaternion(R)
        w, x, y, z = q
        
        # Quaternion Jacobian matrix
        E = np.array([
            [-x, -y, -z],
            [w, -z, y],
            [z, w, -x],
            [-y, x, w]
        ])
        
        return 0.5 * E @ J_omega
    
    def _euler_jacobian(self, J_omega: np.ndarray, R: np.ndarray) -> np.ndarray:
        """Compute Euler angle Jacobian."""
        from .transforms import rotation_matrix_to_euler
        euler = rotation_matrix_to_euler(R)
        rx, ry, rz = euler
        
        # Euler angle Jacobian matrix
        cx, cy, cz = np.cos(euler)
        sx, sy, sz = np.sin(euler)
        
        # For XYZ convention
        T = np.array([
            [1, sx*sy/cy, cx*sy/cy],
            [0, cx, -sx],
            [0, sx/cy, cx/cy]
        ])
        
        return T @ J_omega
    
    def _axis_angle_jacobian(self, J_omega: np.ndarray, R: np.ndarray) -> np.ndarray:
        """Compute axis-angle Jacobian."""
        from .transforms import rotation_matrix_to_axis_angle
        axis, angle = rotation_matrix_to_axis_angle(R)
        
        if abs(angle) < 1e-6:
            # Near zero rotation, use identity
            return J_omega
        
        # Axis-angle Jacobian matrix
        x, y, z = axis
        T = np.array([
            [x*x, x*y, x*z],
            [y*x, y*y, y*z],
            [z*x, z*y, z*z]
        ])
        
        return (np.eye(3) - T) @ J_omega


class JacobianAnalyzer:
    """Advanced Jacobian analysis tools."""
    
    def __init__(self, jacobian: Jacobian):
        self.jacobian = jacobian
    
    def singular_value_decomposition(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Perform SVD of the Jacobian.
        
        Returns:
            Tuple of (U, s, Vt)
        """
        J = self.jacobian.compute()
        return np.linalg.svd(J)
    
    def singularity_analysis(self) -> dict:
        """
        Comprehensive singularity analysis.
        
        Returns:
            Dictionary with singularity metrics
        """
        U, s, Vt = self.singular_value_decomposition()
        
        return {
            'singular_values': s,
            'condition_number': self.jacobian.condition_number(),
            'manipulability': self.jacobian.manipulability(),
            'distance_to_singularity': self.jacobian.distance_to_singularity(),
            'is_singular': self.jacobian.is_singular(),
            'rank': np.sum(s > 1e-10),
            'null_space_dimension': len(s) - np.sum(s > 1e-10)
        }
    
    def workspace_analysis(self, joint_limits: List[Tuple[float, float]], 
                          n_samples: int = 1000) -> dict:
        """
        Analyze workspace characteristics using Jacobian.
        
        Args:
            joint_limits: List of (min, max) joint limits
            n_samples: Number of random samples
            
        Returns:
            Workspace analysis results
        """
        manipulabilities = []
        condition_numbers = []
        
        for _ in range(n_samples):
            # Random joint configuration within limits
            q = np.array([
                np.random.uniform(lim[0], lim[1]) for lim in joint_limits
            ])
            
            # Update Jacobian for this configuration
            self.jacobian.joint_config = q
            self.jacobian._computed = False
            
            manipulabilities.append(self.jacobian.manipulability())
            condition_numbers.append(self.jacobian.condition_number())
        
        return {
            'mean_manipulability': np.mean(manipulabilities),
            'std_manipulability': np.std(manipulabilities),
            'min_manipulability': np.min(manipulabilities),
            'max_manipulability': np.max(manipulabilities),
            'mean_condition_number': np.mean(condition_numbers),
            'std_condition_number': np.std(condition_numbers)
        }


# Thread-safe Jacobian cache
class JacobianCache:
    """Thread-safe cache for computed Jacobians."""
    
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Optional[np.ndarray]:
        """Get cached Jacobian."""
        with self.lock:
            return self.cache.get(key)
    
    def set(self, key: str, jacobian: np.ndarray):
        """Set cached Jacobian."""
        with self.lock:
            if len(self.cache) >= self.max_size:
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
            self.cache[key] = jacobian.copy()
    
    def clear(self):
        """Clear cache."""
        with self.lock:
            self.cache.clear()


# Global Jacobian cache
_jacobian_cache = JacobianCache() 