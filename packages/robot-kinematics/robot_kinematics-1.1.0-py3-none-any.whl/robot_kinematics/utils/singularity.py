"""
Singularity analysis utilities for robotics kinematics.

This module provides tools for detecting, analyzing, and avoiding singularities
in robotic manipulators.
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from ..core.base import RobotKinematicsBase
from ..core.jacobian import Jacobian
from ..core.exceptions import SingularityError


class SingularityAnalyzer:
    """
    Singularity analysis for robotic manipulators.
    
    This class provides comprehensive tools for detecting and analyzing
    singularities in robot kinematics.
    """
    
    def __init__(self, robot: RobotKinematicsBase):
        """
        Initialize singularity analyzer.
        
        Args:
            robot: Robot kinematics instance
        """
        self.robot = robot
        self.n_joints = robot.n_joints
    
    def detect_singularities(self, joint_config: np.ndarray, 
                           threshold: float = 1e-6) -> Dict[str, Any]:
        """
        Detect singularities in a joint configuration.
        
        Args:
            joint_config: Joint configuration vector
            threshold: Singularity detection threshold
            
        Returns:
            Singularity analysis results
        """
        jacobian = self.robot.get_jacobian(joint_config)
        
        # Compute singular values
        U, s, Vt = np.linalg.svd(jacobian.compute())
        
        # Detect singularities
        singular_indices = np.where(s < threshold)[0]
        is_singular = len(singular_indices) > 0
        
        # Compute singularity metrics
        condition_number = jacobian.condition_number()
        manipulability = jacobian.manipulability()
        distance_to_singularity = jacobian.distance_to_singularity()
        
        # Analyze singularity type
        singularity_type = self._classify_singularity(s, singular_indices)
        
        return {
            'is_singular': is_singular,
            'singular_values': s,
            'singular_indices': singular_indices,
            'condition_number': condition_number,
            'manipulability': manipulability,
            'distance_to_singularity': distance_to_singularity,
            'singularity_type': singularity_type,
            'rank_deficiency': len(singular_indices),
            'null_space_dimension': len(singular_indices)
        }
    
    def analyze_singularity_manifold(self, n_samples: int = 1000) -> Dict[str, Any]:
        """
        Analyze singularity manifold in joint space.
        
        Args:
            n_samples: Number of random samples
            
        Returns:
            Singularity manifold analysis
        """
        singular_configs = []
        singularity_metrics = []
        
        for _ in range(n_samples):
            # Random joint configuration
            q = np.array([
                np.random.uniform(lim[0], lim[1]) for lim in self.robot.joint_limits
            ])
            
            try:
                # Detect singularities
                analysis = self.detect_singularities(q)
                
                if analysis['is_singular']:
                    singular_configs.append(q)
                    singularity_metrics.append({
                        'condition_number': analysis['condition_number'],
                        'manipulability': analysis['manipulability'],
                        'distance_to_singularity': analysis['distance_to_singularity'],
                        'singularity_type': analysis['singularity_type']
                    })
                    
            except Exception:
                continue
        
        if not singular_configs:
            return {'error': 'No singularities found in sample'}
        
        singular_configs = np.array(singular_configs)
        
        # Analyze singularity distribution
        singularity_distribution = self._analyze_singularity_distribution(singularity_metrics)
        
        return {
            'singular_configs': singular_configs,
            'singularity_metrics': singularity_metrics,
            'n_singularities': len(singular_configs),
            'singularity_ratio': len(singular_configs) / n_samples,
            'singularity_distribution': singularity_distribution
        }
    
    def find_singularity_free_path(self, start_config: np.ndarray, 
                                  end_config: np.ndarray,
                                  n_waypoints: int = 50,
                                  singularity_threshold: float = 1e-6) -> Optional[np.ndarray]:
        """
        Find a singularity-free path between two configurations.
        
        Args:
            start_config: Starting joint configuration
            end_config: Ending joint configuration
            n_waypoints: Number of waypoints in the path
            singularity_threshold: Threshold for singularity detection
            
        Returns:
            Path waypoints or None if no path found
        """
        # Linear interpolation in joint space
        path = np.linspace(start_config, end_config, n_waypoints)
        
        # Check for singularities along the path
        for i, waypoint in enumerate(path):
            try:
                analysis = self.detect_singularities(waypoint, singularity_threshold)
                if analysis['is_singular']:
                    # Try to find alternative path
                    return self._find_alternative_path(start_config, end_config, n_waypoints)
            except Exception:
                continue
        
        return path
    
    def compute_singularity_avoidance_velocity(self, joint_config: np.ndarray,
                                             desired_velocity: np.ndarray,
                                             damping: float = 0.1) -> np.ndarray:
        """
        Compute velocity that avoids singularities.
        
        Args:
            joint_config: Current joint configuration
            desired_velocity: Desired end-effector velocity
            damping: Damping factor for singularity avoidance
            
        Returns:
            Modified joint velocity
        """
        jacobian = self.robot.get_jacobian(joint_config)
        
        # Use damped least squares
        J_damped = jacobian.pseudo_inverse(damping)
        
        # Compute joint velocity
        joint_velocity = J_damped @ desired_velocity
        
        return joint_velocity
    
    def _classify_singularity(self, singular_values: np.ndarray, 
                            singular_indices: np.ndarray) -> str:
        """
        Classify the type of singularity.
        
        Args:
            singular_values: Singular values of the Jacobian
            singular_indices: Indices of singular values
            
        Returns:
            Singularity type classification
        """
        if len(singular_indices) == 0:
            return 'none'
        
        # Analyze the pattern of singular values
        if len(singular_indices) == 1:
            return 'boundary'
        elif len(singular_indices) == 2:
            return 'interior'
        elif len(singular_indices) >= 3:
            return 'degenerate'
        else:
            return 'unknown'
    
    def _analyze_singularity_distribution(self, metrics: List[Dict]) -> Dict[str, Any]:
        """
        Analyze distribution of singularity metrics.
        
        Args:
            metrics: List of singularity metrics
            
        Returns:
            Distribution analysis
        """
        condition_numbers = [m['condition_number'] for m in metrics]
        manipulabilities = [m['manipulability'] for m in metrics]
        
        # Count singularity types
        type_counts = {}
        for m in metrics:
            singularity_type = m['singularity_type']
            type_counts[singularity_type] = type_counts.get(singularity_type, 0) + 1
        
        return {
            'mean_condition_number': np.mean(condition_numbers),
            'std_condition_number': np.std(condition_numbers),
            'mean_manipulability': np.mean(manipulabilities),
            'std_manipulability': np.std(manipulabilities),
            'singularity_type_distribution': type_counts
        }
    
    def _find_alternative_path(self, start_config: np.ndarray,
                             end_config: np.ndarray,
                             n_waypoints: int) -> Optional[np.ndarray]:
        """
        Find alternative path avoiding singularities.
        
        Args:
            start_config: Starting configuration
            end_config: Ending configuration
            n_waypoints: Number of waypoints
            
        Returns:
            Alternative path or None
        """
        # Simple approach: add intermediate waypoints
        # In practice, this would use more sophisticated path planning
        
        # Try different intermediate configurations
        for attempt in range(10):
            # Random intermediate configuration
            intermediate = np.array([
                np.random.uniform(lim[0], lim[1]) for lim in self.robot.joint_limits
            ])
            
            # Create path through intermediate point
            path1 = np.linspace(start_config, intermediate, n_waypoints // 2)
            path2 = np.linspace(intermediate, end_config, n_waypoints // 2)
            path = np.vstack([path1, path2])
            
            # Check if path is singularity-free
            is_valid = True
            for waypoint in path:
                try:
                    analysis = self.detect_singularities(waypoint)
                    if analysis['is_singular']:
                        is_valid = False
                        break
                except Exception:
                    is_valid = False
                    break
            
            if is_valid:
                return path
        
        return None


class SingularityAvoidance:
    """
    Advanced singularity avoidance strategies.
    
    This class provides various strategies for avoiding singularities
    during robot motion planning and control.
    """
    
    def __init__(self, robot: RobotKinematicsBase):
        """
        Initialize singularity avoidance.
        
        Args:
            robot: Robot kinematics instance
        """
        self.robot = robot
        self.analyzer = SingularityAnalyzer(robot)
    
    def compute_singularity_robust_jacobian(self, joint_config: np.ndarray,
                                          method: str = 'damped_least_squares',
                                          **kwargs) -> np.ndarray:
        """
        Compute singularity-robust Jacobian inverse.
        
        Args:
            joint_config: Joint configuration
            method: Method for singularity robustness
            **kwargs: Additional parameters
            
        Returns:
            Robust Jacobian inverse
        """
        jacobian = self.robot.get_jacobian(joint_config)
        J = jacobian.compute()
        
        if method == 'damped_least_squares':
            damping = kwargs.get('damping', 0.1)
            return jacobian.pseudo_inverse(damping)
        
        elif method == 'singular_value_filtering':
            threshold = kwargs.get('threshold', 1e-6)
            U, s, Vt = np.linalg.svd(J)
            
            # Filter singular values
            s_filtered = np.where(s > threshold, 1/s, 0)
            J_inv = Vt.T @ np.diag(s_filtered) @ U.T
            
            return J_inv
        
        elif method == 'truncated_svd':
            rank = kwargs.get('rank', None)
            U, s, Vt = np.linalg.svd(J)
            
            if rank is None:
                rank = np.sum(s > 1e-6)
            
            # Truncate to specified rank
            s_truncated = np.zeros_like(s)
            s_truncated[:rank] = 1/s[:rank]
            J_inv = Vt.T @ np.diag(s_truncated) @ U.T
            
            return J_inv
        
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def compute_null_space_motion(self, joint_config: np.ndarray,
                                primary_task: np.ndarray,
                                secondary_task: np.ndarray,
                                damping: float = 0.1) -> np.ndarray:
        """
        Compute null space motion for singularity avoidance.
        
        Args:
            joint_config: Joint configuration
            primary_task: Primary task velocity
            secondary_task: Secondary task velocity
            damping: Damping factor
            
        Returns:
            Joint velocity
        """
        jacobian = self.robot.get_jacobian(joint_config)
        return jacobian.redundancy_resolution(primary_task, secondary_task, damping)
    
    def optimize_for_manipulability(self, target_pose: np.ndarray,
                                  initial_guess: np.ndarray,
                                  **kwargs) -> np.ndarray:
        """
        Optimize joint configuration for maximum manipulability.
        
        Args:
            target_pose: Target end-effector pose
            initial_guess: Initial joint configuration guess
            **kwargs: Optimization parameters
            
        Returns:
            Optimized joint configuration
        """
        from scipy.optimize import minimize
        
        def objective_function(q):
            """Objective function: maximize manipulability."""
            try:
                jacobian = self.robot.get_jacobian(q)
                manipulability = jacobian.manipulability()
                return -manipulability  # Minimize negative manipulability
            except:
                return 1e6  # Large penalty for invalid configurations
        
        def constraint_function(q):
            """Constraint: end-effector pose error."""
            try:
                current_pose = self.robot.forward_kinematics(q)
                error = np.linalg.norm(current_pose.position - target_pose[:3])
                return 0.01 - error  # Error should be less than 1cm
            except:
                return -1.0  # Invalid configuration
        
        # Bounds for joint limits
        bounds = [(lim[0], lim[1]) for lim in self.robot.joint_limits]
        
        # Constraints
        constraints = {
            'type': 'ineq',
            'fun': constraint_function
        }
        
        # Optimize
        result = minimize(
            objective_function,
            initial_guess,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': kwargs.get('max_iterations', 100)}
        )
        
        if not result.success:
            raise SingularityError("Failed to optimize for manipulability")
        
        return result.x 