"""
Numerical inverse kinematics solvers.

This module implements various numerical methods for solving inverse kinematics
including Jacobian-based methods, optimization-based approaches, and hybrid methods.
"""

import numpy as np
from typing import Optional, Dict, Any, Tuple, List, Union
from scipy.optimize import minimize, least_squares
from scipy.linalg import pinv
import threading
from ..core.base import RobotKinematicsBase
from ..core.transforms import Transform
from ..core.exceptions import ConvergenceError, KinematicsError, JointLimitError


class NumericalIK:
    """
    Numerical inverse kinematics solver.
    
    This class implements various numerical methods for solving inverse kinematics
    including Jacobian-based methods and optimization-based approaches.
    """
    
    def __init__(self, robot: RobotKinematicsBase, method: str = 'damped_least_squares'):
        """
        Initialize numerical IK solver.
        
        Args:
            robot: Robot kinematics instance
            method: Solution method ('damped_least_squares', 'levenberg_marquardt', 
                    'newton_raphson', 'optimization')
        """
        self.robot = robot
        self.method = method
        self._lock = threading.Lock()
        
        # Default parameters
        self.max_iterations = 200  # Increased from 100
        self.tolerance = 1e-4      # Relaxed from 1e-6
        self.damping = 0.01        # Reduced from 0.1 for better convergence
        self.step_size = 0.5       # Increased from 0.1 for faster convergence
    
    def solve(self, target_pose: Union[Transform, np.ndarray], 
              initial_guess: Optional[np.ndarray] = None,
              **kwargs) -> Tuple[np.ndarray, bool, float]:
        """
        Solve inverse kinematics.
        
        Args:
            target_pose: Target end-effector pose (Transform object or numpy array)
            initial_guess: Initial joint configuration guess
            **kwargs: Additional solver parameters
            
        Returns:
            Tuple of (joint_configuration, success, error)
        """
        # Convert target_pose to Transform if it's a numpy array
        if isinstance(target_pose, np.ndarray):
            if len(target_pose) == 3:
                # Position only
                target_transform = Transform(position=target_pose)
            elif len(target_pose) == 7:
                # Position + quaternion [x, y, z, w, qx, qy, qz]
                position = target_pose[:3]
                quaternion = target_pose[3:]  # [w, x, y, z]
                # Convert quaternion to rotation matrix
                from ..core.transforms import quaternion_to_rotation_matrix
                rotation_matrix = quaternion_to_rotation_matrix(quaternion)
                target_transform = Transform(position=position, rotation=rotation_matrix)
            else:
                raise KinematicsError("Target pose must be 3D position or 7D pose (position + quaternion)")
        else:
            target_transform = target_pose
        
        # Update parameters from kwargs
        max_iter = kwargs.get('max_iterations', self.max_iterations)
        tol = kwargs.get('tolerance', self.tolerance)
        damping = kwargs.get('damping', self.damping)
        step_size = kwargs.get('step_size', self.step_size)
        
        # Set initial guess
        if initial_guess is None:
            q = np.zeros(self.robot.n_joints)
        else:
            q = np.asarray(initial_guess).flatten()
            if len(q) != self.robot.n_joints:
                raise KinematicsError("Initial guess length must match number of joints")
        
        # Check joint limits for initial guess
        if not self.robot.check_joint_limits(q):
            q = self.robot.enforce_joint_limits(q)
        
        try:
            # Solve using selected method
            if self.method == 'damped_least_squares':
                solution = self._damped_least_squares(target_transform, q, max_iter, tol, damping)
            elif self.method == 'levenberg_marquardt':
                solution = self._levenberg_marquardt(target_transform, q, max_iter, tol, damping)
            elif self.method == 'newton_raphson':
                solution = self._newton_raphson(target_transform, q, max_iter, tol)
            elif self.method == 'optimization':
                solution = self._optimization_based(target_transform, q, max_iter, tol)
            else:
                raise KinematicsError(f"Unknown method: {self.method}")
            
            # Calculate final error
            final_pose = self.robot.forward_kinematics(solution)
            final_error = float(np.linalg.norm(self._compute_error(final_pose, target_transform)))
            
            return solution, True, final_error
            
        except ConvergenceError as e:
            # Return the best solution found so far
            final_pose = self.robot.forward_kinematics(q)
            final_error = float(np.linalg.norm(self._compute_error(final_pose, target_transform)))
            return q, False, final_error
    
    def _damped_least_squares(self, target_pose: Transform, q: np.ndarray,
                             max_iter: int, tol: float, damping: float) -> np.ndarray:
        """
        Damped least squares method.
        
        Args:
            target_pose: Target pose
            q: Initial joint configuration
            max_iter: Maximum iterations
            tol: Convergence tolerance
            damping: Damping factor
            
        Returns:
            Joint configuration
        """
        for iteration in range(max_iter):
            # Current pose
            current_pose = self.robot.forward_kinematics(q)
            
            # Error
            error = self._compute_error(current_pose, target_pose)
            error_norm = np.linalg.norm(error)
            
            if error_norm < tol:
                return q
            
            # Jacobian
            jacobian = self.robot.get_jacobian(q)
            J = jacobian.compute()
            
            # Damped least squares solution
            J_damped = J.T @ (J @ J.T + damping * np.eye(J.shape[0]))
            delta_q = J_damped @ error
            
            # Update joint configuration
            q_new = q + self.step_size * delta_q
            
            # Enforce joint limits
            q_new = self.robot.enforce_joint_limits(q_new)
            
            # Check if new configuration is better
            new_pose = self.robot.forward_kinematics(q_new)
            new_error = self._compute_error(new_pose, target_pose)
            new_error_norm = np.linalg.norm(new_error)
            
            if new_error_norm < error_norm:
                q = q_new
            else:
                # Reduce step size
                self.step_size *= 0.5
                if self.step_size < 1e-6:
                    break
        
        raise ConvergenceError(f"Failed to converge after {max_iter} iterations", 
                             max_iterations=max_iter, final_error=error_norm)
    
    def _levenberg_marquardt(self, target_pose: Transform, q: np.ndarray,
                            max_iter: int, tol: float, damping: float) -> np.ndarray:
        """
        Levenberg-Marquardt method.
        
        Args:
            target_pose: Target pose
            q: Initial joint configuration
            max_iter: Maximum iterations
            tol: Convergence tolerance
            damping: Initial damping factor
            
        Returns:
            Joint configuration
        """
        lambda_val = damping
        
        for iteration in range(max_iter):
            # Current pose
            current_pose = self.robot.forward_kinematics(q)
            
            # Error
            error = self._compute_error(current_pose, target_pose)
            error_norm = np.linalg.norm(error)
            
            if error_norm < tol:
                return q
            
            # Jacobian
            jacobian = self.robot.get_jacobian(q)
            J = jacobian.compute()
            
            # Levenberg-Marquardt update
            H = J.T @ J + lambda_val * np.eye(J.shape[1])
            g = J.T @ error
            
            try:
                delta_q = np.linalg.solve(H, g)
            except np.linalg.LinAlgError:
                # Fallback to pseudo-inverse
                delta_q = pinv(H) @ g
            
            # Update joint configuration
            q_new = q + delta_q
            q_new = self.robot.enforce_joint_limits(q_new)
            
            # Check if new configuration is better
            new_pose = self.robot.forward_kinematics(q_new)
            new_error = self._compute_error(new_pose, target_pose)
            new_error_norm = np.linalg.norm(new_error)
            
            if new_error_norm < error_norm:
                q = q_new
                lambda_val *= 0.1  # Reduce damping
            else:
                lambda_val *= 10.0  # Increase damping
                if lambda_val > 1e6:
                    break
        
        raise ConvergenceError(f"Failed to converge after {max_iter} iterations",
                             max_iterations=max_iter, final_error=error_norm)
    
    def _newton_raphson(self, target_pose: Transform, q: np.ndarray,
                       max_iter: int, tol: float) -> np.ndarray:
        """
        Newton-Raphson method.
        
        Args:
            target_pose: Target pose
            q: Initial joint configuration
            max_iter: Maximum iterations
            tol: Convergence tolerance
            
        Returns:
            Joint configuration
        """
        for iteration in range(max_iter):
            # Current pose
            current_pose = self.robot.forward_kinematics(q)
            
            # Error
            error = self._compute_error(current_pose, target_pose)
            error_norm = np.linalg.norm(error)
            
            if error_norm < tol:
                return q
            
            # Jacobian
            jacobian = self.robot.get_jacobian(q)
            J = jacobian.compute()
            
            # Newton-Raphson update
            try:
                delta_q = np.linalg.solve(J, error)
            except np.linalg.LinAlgError:
                # Fallback to pseudo-inverse
                delta_q = pinv(J) @ error
            
            # Update joint configuration
            q_new = q + self.step_size * delta_q
            q_new = self.robot.enforce_joint_limits(q_new)
            
            # Check if new configuration is better
            new_pose = self.robot.forward_kinematics(q_new)
            new_error = self._compute_error(new_pose, target_pose)
            new_error_norm = np.linalg.norm(new_error)
            
            if new_error_norm < error_norm:
                q = q_new
            else:
                # Reduce step size
                self.step_size *= 0.5
                if self.step_size < 1e-6:
                    break
        
        raise ConvergenceError(f"Failed to converge after {max_iter} iterations",
                             max_iterations=max_iter, final_error=error_norm)
    
    def _optimization_based(self, target_pose: Transform, q: np.ndarray,
                           max_iter: int, tol: float) -> np.ndarray:
        """
        Optimization-based method using scipy.optimize.
        
        Args:
            target_pose: Target pose
            q: Initial joint configuration
            max_iter: Maximum iterations
            tol: Convergence tolerance
            
        Returns:
            Joint configuration
        """
        def objective_function(q_vec):
            """Objective function for optimization."""
            try:
                current_pose = self.robot.forward_kinematics(q_vec)
                error = self._compute_error(current_pose, target_pose)
                return np.sum(error**2)
            except:
                return np.inf
        
        def constraint_function(q_vec):
            """Constraint function for joint limits."""
            return np.array([
                q_vec[i] - self.robot.joint_limits[i][1] for i in range(len(q_vec))
            ] + [
                self.robot.joint_limits[i][0] - q_vec[i] for i in range(len(q_vec))
            ])
        
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
            q,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': max_iter, 'ftol': tol}
        )
        
        if not result.success:
            raise ConvergenceError(f"Optimization failed: {result.message}",
                                 max_iterations=max_iter, final_error=result.fun)
        
        return result.x
    
    def _compute_error(self, current_pose: Transform, target_pose: Transform) -> np.ndarray:
        """
        Compute error between current and target poses.
        
        Args:
            current_pose: Current end-effector pose
            target_pose: Target end-effector pose
            
        Returns:
            Error vector [position_error, orientation_error]
        """
        # Position error
        pos_error = target_pose.position - current_pose.position
        
        # Orientation error (using quaternion difference)
        from ..core.transforms import rotation_matrix_to_quaternion
        q_current = rotation_matrix_to_quaternion(current_pose.rotation)
        q_target = rotation_matrix_to_quaternion(target_pose.rotation)
        
        # Ensure shortest path
        if np.dot(q_current, q_target) < 0:
            q_target = -q_target
        
        # Quaternion error
        q_error = q_target - q_current
        
        return np.concatenate([pos_error, q_error[1:]])  # Exclude w component
    
    def solve_multiple_solutions(self, target_pose: Transform, 
                                n_solutions: int = 8,
                                **kwargs) -> List[np.ndarray]:
        """
        Find multiple IK solutions.
        
        Args:
            target_pose: Target end-effector pose
            n_solutions: Number of solutions to find
            **kwargs: Additional solver parameters
            
        Returns:
            List of joint configurations
        """
        solutions = []
        
        # Try different initial guesses
        for i in range(n_solutions):
            # Random initial guess within joint limits
            initial_guess = np.array([
                np.random.uniform(lim[0], lim[1]) for lim in self.robot.joint_limits
            ])
            
            try:
                solution, success, error = self.solve(target_pose, initial_guess, **kwargs)
                
                if not success:
                    continue
                
                # Check if solution is unique
                is_unique = True
                for existing_solution in solutions:
                    if np.linalg.norm(solution - existing_solution) < 0.1:
                        is_unique = False
                        break
                
                if is_unique:
                    solutions.append(solution)
                    
                    if len(solutions) >= n_solutions:
                        break
                        
            except ConvergenceError:
                continue
        
        return solutions
    
    def solve_with_constraints(self, target_pose: Transform,
                              joint_constraints: Optional[Dict[int, float]] = None,
                              orientation_weight: float = 1.0,
                              position_weight: float = 1.0,
                              **kwargs) -> np.ndarray:
        """
        Solve IK with additional constraints.
        
        Args:
            target_pose: Target end-effector pose
            joint_constraints: Dictionary of joint index -> target value
            orientation_weight: Weight for orientation error
            position_weight: Weight for position error
            **kwargs: Additional solver parameters
            
        Returns:
            Joint configuration
        """
        # Modify error computation to include weights and constraints
        original_compute_error = self._compute_error
        
        def weighted_error(current_pose, target_pose):
            error = original_compute_error(current_pose, target_pose)
            
            # Apply weights
            pos_error = error[:3] * position_weight
            ori_error = error[3:] * orientation_weight
            
            return np.concatenate([pos_error, ori_error])
        
        self._compute_error = weighted_error
        
        try:
            solution, success, error = self.solve(target_pose, **kwargs)
            if not success:
                raise ConvergenceError(f"Failed to converge: error = {error}")
            return solution
        finally:
            # Restore original error function
            self._compute_error = original_compute_error
        
        return solution


class IKOptimizer:
    """Advanced IK optimization with multiple objectives."""
    
    def __init__(self, robot: RobotKinematicsBase):
        self.robot = robot
    
    def solve_with_objectives(self, target_pose: Transform,
                             objectives: List[Dict[str, Any]],
                             **kwargs) -> np.ndarray:
        """
        Solve IK with multiple objectives.
        
        Args:
            target_pose: Target end-effector pose
            objectives: List of objective dictionaries
            **kwargs: Additional parameters
            
        Returns:
            Joint configuration
        """
        def multi_objective_function(q):
            """Multi-objective function."""
            total_cost = 0
            
            for objective in objectives:
                obj_type = objective['type']
                weight = objective.get('weight', 1.0)
                
                if obj_type == 'pose_error':
                    current_pose = self.robot.forward_kinematics(q)
                    error = self._compute_pose_error(current_pose, target_pose)
                    total_cost += weight * np.sum(error**2)
                
                elif obj_type == 'joint_limits':
                    cost = self._compute_joint_limit_cost(q)
                    total_cost += weight * cost
                
                elif obj_type == 'singularity_avoidance':
                    jacobian = self.robot.get_jacobian(q)
                    cost = 1.0 / (jacobian.manipulability() + 1e-6)
                    total_cost += weight * cost
                
                elif obj_type == 'joint_smoothness':
                    if 'previous_config' in objective:
                        prev_q = objective['previous_config']
                        cost = np.sum((q - prev_q)**2)
                        total_cost += weight * cost
            
            return total_cost
        
        # Initial guess
        initial_guess = kwargs.get('initial_guess', np.zeros(self.robot.n_joints))
        
        # Bounds
        bounds = [(lim[0], lim[1]) for lim in self.robot.joint_limits]
        
        # Optimize
        result = minimize(
            multi_objective_function,
            initial_guess,
            method='SLSQP',
            bounds=bounds,
            options={'maxiter': kwargs.get('max_iterations', 100)}
        )
        
        if not result.success:
            raise ConvergenceError(f"Multi-objective optimization failed: {result.message}")
        
        return result.x
    
    def _compute_pose_error(self, current_pose: Transform, target_pose: Transform) -> np.ndarray:
        """Compute pose error."""
        pos_error = target_pose.position - current_pose.position
        
        from ..core.transforms import rotation_matrix_to_quaternion
        q_current = rotation_matrix_to_quaternion(current_pose.rotation)
        q_target = rotation_matrix_to_quaternion(target_pose.rotation)
        
        if np.dot(q_current, q_target) < 0:
            q_target = -q_target
        
        q_error = q_target - q_current
        
        return np.concatenate([pos_error, q_error[1:]])
    
    def _compute_joint_limit_cost(self, q: np.ndarray) -> float:
        """Compute joint limit violation cost."""
        cost = 0
        for i, (q_val, (min_val, max_val)) in enumerate(zip(q, self.robot.joint_limits)):
            if q_val < min_val:
                cost += (min_val - q_val)**2
            elif q_val > max_val:
                cost += (q_val - max_val)**2
        return cost 