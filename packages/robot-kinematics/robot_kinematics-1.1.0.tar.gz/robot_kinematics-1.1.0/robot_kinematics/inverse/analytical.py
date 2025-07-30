"""
Analytical inverse kinematics solvers.

This module implements analytical solutions for inverse kinematics of common
robot configurations including 6-DOF manipulators, SCARA robots, and others.
"""

import numpy as np
from typing import List, Tuple, Optional, Dict, Any
import math
from ..core.base import RobotKinematicsBase
from ..core.transforms import Transform
from ..core.exceptions import KinematicsError, SingularityError


class AnalyticalIK:
    """
    Analytical inverse kinematics solver.
    
    This class provides analytical solutions for inverse kinematics of common
    robot configurations where closed-form solutions exist.
    """
    
    def __init__(self, robot: RobotKinematicsBase):
        """
        Initialize analytical IK solver.
        
        Args:
            robot: Robot kinematics instance
        """
        self.robot = robot
        self.n_joints = robot.n_joints
    
    def solve(self, target_pose: Transform, **kwargs) -> List[np.ndarray]:
        """
        Solve inverse kinematics analytically.
        
        Args:
            target_pose: Target end-effector pose
            **kwargs: Additional parameters
            
        Returns:
            List of joint configurations (multiple solutions)
        """
        if self.n_joints == 6:
            return self._solve_6dof(target_pose, **kwargs)
        elif self.n_joints == 4:
            return self._solve_scara(target_pose, **kwargs)
        elif self.n_joints == 3:
            return self._solve_3dof(target_pose, **kwargs)
        else:
            raise KinematicsError(f"Analytical IK not implemented for {self.n_joints}-DOF robot")
    
    def _solve_6dof(self, target_pose: Transform, **kwargs) -> List[np.ndarray]:
        """
        Solve IK for 6-DOF manipulator (Pieper's method).
        
        Args:
            target_pose: Target end-effector pose
            
        Returns:
            List of joint configurations
        """
        # Extract position and orientation
        p_target = target_pose.position
        R_target = target_pose.rotation
        
        # Apply tool transform
        tool_inv = self.robot.tool_transform.inverse()
        p_tool = tool_inv.position
        R_tool = tool_inv.rotation
        
        # Transform target to wrist center
        p_wrist = p_target - R_target @ p_tool
        
        # Solve for first 3 joints (position)
        solutions_123 = self._solve_position_3dof(p_wrist)
        
        all_solutions = []
        
        for q1, q2, q3 in solutions_123:
            # Get transformation to joint 3
            T_03 = self.robot.get_joint_transform(2, [q1, q2, q3, 0, 0, 0])
            R_03 = T_03.rotation
            
            # Solve for last 3 joints (orientation)
            R_36 = R_03.T @ R_target @ R_tool.T
            
            try:
                solutions_456 = self._solve_orientation_3dof(R_36)
                
                for q4, q5, q6 in solutions_456:
                    solution = np.array([q1, q2, q3, q4, q5, q6])
                    
                    # Check joint limits
                    if self.robot.check_joint_limits(solution):
                        all_solutions.append(solution)
                        
            except SingularityError:
                continue
        
        return all_solutions
    
    def _solve_position_3dof(self, p_target: np.ndarray) -> List[Tuple[float, float, float]]:
        """
        Solve position IK for first 3 joints.
        
        Args:
            p_target: Target position
            
        Returns:
            List of (q1, q2, q3) solutions
        """
        # This is a simplified implementation
        # In practice, this would depend on the specific robot geometry
        
        # For now, return a basic solution
        # This should be implemented based on the specific robot's DH parameters
        
        # Example for a typical 6-DOF manipulator
        x, y, z = p_target
        
        # Solve for q1 (base rotation)
        q1 = math.atan2(y, x)
        
        # Solve for q2, q3 (shoulder and elbow)
        # This is a simplified approach - actual implementation depends on link lengths
        r = math.sqrt(x**2 + y**2)
        d = z
        
        # Assuming link lengths (should be extracted from DH parameters)
        l1 = 0.5  # Link 1 length
        l2 = 0.5  # Link 2 length
        
        # Solve using cosine law
        cos_q3 = (r**2 + d**2 - l1**2 - l2**2) / (2 * l1 * l2)
        
        if abs(cos_q3) > 1:
            raise SingularityError("Target position out of reach")
        
        q3_1 = math.acos(cos_q3)
        q3_2 = -q3_1
        
        solutions = []
        
        for q3 in [q3_1, q3_2]:
            # Solve for q2
            k1 = l1 + l2 * math.cos(q3)
            k2 = l2 * math.sin(q3)
            
            q2 = math.atan2(d, r) - math.atan2(k2, k1)
            
            solutions.append((q1, q2, q3))
        
        return solutions
    
    def _solve_orientation_3dof(self, R_target: np.ndarray) -> List[Tuple[float, float, float]]:
        """
        Solve orientation IK for last 3 joints.
        
        Args:
            R_target: Target rotation matrix
            
        Returns:
            List of (q4, q5, q6) solutions
        """
        # Extract Euler angles (ZYX convention)
        sy = R_target[0, 2]
        
        if abs(sy) < 1e-6:
            # Singularity case
            raise SingularityError("Wrist singularity encountered")
        
        q5_1 = math.asin(sy)
        q5_2 = math.pi - q5_1
        
        solutions = []
        
        for q5 in [q5_1, q5_2]:
            q4 = math.atan2(-R_target[1, 2], R_target[2, 2])
            q6 = math.atan2(-R_target[0, 1], R_target[0, 0])
            
            solutions.append((q4, q5, q6))
        
        return solutions
    
    def _solve_scara(self, target_pose: Transform, **kwargs) -> List[np.ndarray]:
        """
        Solve IK for SCARA robot.
        
        Args:
            target_pose: Target end-effector pose
            
        Returns:
            List of joint configurations
        """
        p_target = target_pose.position
        x, y, z = p_target
        
        # SCARA has 4 joints: 2 revolute (shoulder, elbow) + 1 prismatic (vertical) + 1 revolute (wrist)
        
        # Solve for q1, q2 (shoulder and elbow)
        # Assuming link lengths
        l1 = 0.4  # Link 1 length
        l2 = 0.3  # Link 2 length
        
        r = math.sqrt(x**2 + y**2)
        
        if r > l1 + l2 or r < abs(l1 - l2):
            raise SingularityError("Target position out of reach")
        
        # Solve using cosine law
        cos_q2 = (r**2 - l1**2 - l2**2) / (2 * l1 * l2)
        q2_1 = math.acos(cos_q2)
        q2_2 = -q2_1
        
        solutions = []
        
        for q2 in [q2_1, q2_2]:
            # Solve for q1
            k1 = l1 + l2 * math.cos(q2)
            k2 = l2 * math.sin(q2)
            
            q1 = math.atan2(y, x) - math.atan2(k2, k1)
            
            # Solve for q3 (prismatic joint)
            q3 = z  # Assuming z is the prismatic joint value
            
            # Solve for q4 (wrist rotation)
            # Extract yaw angle from target orientation
            q4 = math.atan2(target_pose.rotation[1, 0], target_pose.rotation[0, 0])
            
            solution = np.array([q1, q2, q3, q4])
            
            if self.robot.check_joint_limits(solution):
                solutions.append(solution)
        
        return solutions
    
    def _solve_3dof(self, target_pose: Transform, **kwargs) -> List[np.ndarray]:
        """
        Solve IK for 3-DOF planar robot.
        
        Args:
            target_pose: Target end-effector pose
            
        Returns:
            List of joint configurations
        """
        p_target = target_pose.position
        x, y, _ = p_target  # Ignore z for planar robot
        
        # Assuming link lengths
        l1 = 0.3  # Link 1 length
        l2 = 0.3  # Link 2 length
        l3 = 0.1  # Link 3 length (end effector)
        
        # Solve for q1, q2
        r = math.sqrt(x**2 + y**2)
        
        if r > l1 + l2 + l3 or r < abs(l1 - l2 - l3):
            raise SingularityError("Target position out of reach")
        
        # Solve using cosine law
        cos_q2 = (r**2 - l1**2 - l2**2) / (2 * l1 * l2)
        q2_1 = math.acos(cos_q2)
        q2_2 = -q2_1
        
        solutions = []
        
        for q2 in [q2_1, q2_2]:
            # Solve for q1
            k1 = l1 + l2 * math.cos(q2)
            k2 = l2 * math.sin(q2)
            
            q1 = math.atan2(y, x) - math.atan2(k2, k1)
            
            # Solve for q3 (end effector orientation)
            q3 = 0  # For planar robot, this is typically 0 or fixed
            
            solution = np.array([q1, q2, q3])
            
            if self.robot.check_joint_limits(solution):
                solutions.append(solution)
        
        return solutions


class GeometricIK:
    """
    Geometric inverse kinematics solver.
    
    This class implements geometric methods for solving inverse kinematics
    based on the robot's geometric structure.
    """
    
    def __init__(self, robot: RobotKinematicsBase):
        """
        Initialize geometric IK solver.
        
        Args:
            robot: Robot kinematics instance
        """
        self.robot = robot
    
    def solve(self, target_pose: Transform, **kwargs) -> List[np.ndarray]:
        """
        Solve inverse kinematics using geometric methods.
        
        Args:
            target_pose: Target end-effector pose
            **kwargs: Additional parameters
            
        Returns:
            List of joint configurations
        """
        # Extract DH parameters for geometric analysis
        if hasattr(self.robot, 'dh_params'):
            return self._solve_with_dh(target_pose, **kwargs)
        else:
            raise KinematicsError("Geometric IK requires DH parameters")
    
    def _solve_with_dh(self, target_pose: Transform, **kwargs) -> List[np.ndarray]:
        """
        Solve IK using DH parameters and geometric analysis.
        
        Args:
            target_pose: Target end-effector pose
            
        Returns:
            List of joint configurations
        """
        dh_params = self.robot.dh_params
        
        # Analyze robot structure
        structure = self._analyze_structure(dh_params)
        
        if structure['type'] == 'spherical_wrist':
            return self._solve_spherical_wrist(target_pose, dh_params, **kwargs)
        elif structure['type'] == 'planar':
            return self._solve_planar(target_pose, dh_params, **kwargs)
        else:
            raise KinematicsError(f"Geometric IK not implemented for structure type: {structure['type']}")
    
    def _analyze_structure(self, dh_params) -> Dict[str, Any]:
        """
        Analyze robot structure from DH parameters.
        
        Args:
            dh_params: List of DH parameters
            
        Returns:
            Structure analysis dictionary
        """
        n_joints = len(dh_params)
        
        # Check for spherical wrist (last 3 joints have intersecting axes)
        if n_joints >= 6:
            # Check if last 3 joints form a spherical wrist
            last_three = dh_params[-3:]
            if all(p.joint_type == 'revolute' for p in last_three):
                if abs(last_three[0].d) < 1e-6 and abs(last_three[1].d) < 1e-6:
                    return {'type': 'spherical_wrist', 'n_joints': n_joints}
        
        # Check for planar structure
        if n_joints <= 3:
            return {'type': 'planar', 'n_joints': n_joints}
        
        return {'type': 'unknown', 'n_joints': n_joints}
    
    def _solve_spherical_wrist(self, target_pose: Transform, dh_params, **kwargs) -> List[np.ndarray]:
        """
        Solve IK for robot with spherical wrist.
        
        Args:
            target_pose: Target end-effector pose
            dh_params: DH parameters
            
        Returns:
            List of joint configurations
        """
        # This is a simplified implementation
        # Full implementation would require detailed geometric analysis
        
        # For now, delegate to analytical solver
        analytical_solver = AnalyticalIK(self.robot)
        return analytical_solver.solve(target_pose, **kwargs)
    
    def _solve_planar(self, target_pose: Transform, dh_params, **kwargs) -> List[np.ndarray]:
        """
        Solve IK for planar robot.
        
        Args:
            target_pose: Target end-effector pose
            dh_params: DH parameters
            
        Returns:
            List of joint configurations
        """
        # This is a simplified implementation
        # Full implementation would require detailed geometric analysis
        
        # For now, delegate to analytical solver
        analytical_solver = AnalyticalIK(self.robot)
        return analytical_solver.solve(target_pose, **kwargs)


class IKSelector:
    """
    IK solution selector.
    
    This class helps select the best IK solution from multiple candidates
    based on various criteria.
    """
    
    def __init__(self, robot: RobotKinematicsBase):
        """
        Initialize IK selector.
        
        Args:
            robot: Robot kinematics instance
        """
        self.robot = robot
    
    def select_best_solution(self, solutions: List[np.ndarray], 
                           criteria: str = 'joint_limits',
                           **kwargs) -> np.ndarray:
        """
        Select the best IK solution.
        
        Args:
            solutions: List of joint configurations
            criteria: Selection criteria
            **kwargs: Additional parameters
            
        Returns:
            Best joint configuration
        """
        if not solutions:
            raise KinematicsError("No IK solutions available")
        
        if criteria == 'joint_limits':
            return self._select_by_joint_limits(solutions)
        elif criteria == 'manipulability':
            return self._select_by_manipulability(solutions)
        elif criteria == 'distance':
            reference = kwargs.get('reference_config', np.zeros(self.robot.n_joints))
            return self._select_by_distance(solutions, reference)
        elif criteria == 'singularity_avoidance':
            return self._select_by_singularity_avoidance(solutions)
        else:
            raise KinematicsError(f"Unknown selection criteria: {criteria}")
    
    def _select_by_joint_limits(self, solutions: List[np.ndarray]) -> np.ndarray:
        """Select solution with best joint limit margins."""
        best_solution = None
        best_margin = -np.inf
        
        for solution in solutions:
            margin = self._compute_joint_limit_margin(solution)
            if margin > best_margin:
                best_margin = margin
                best_solution = solution
        
        return best_solution
    
    def _select_by_manipulability(self, solutions: List[np.ndarray]) -> np.ndarray:
        """Select solution with highest manipulability."""
        best_solution = None
        best_manipulability = -np.inf
        
        for solution in solutions:
            jacobian = self.robot.get_jacobian(solution)
            manipulability = jacobian.manipulability()
            
            if manipulability > best_manipulability:
                best_manipulability = manipulability
                best_solution = solution
        
        return best_solution
    
    def _select_by_distance(self, solutions: List[np.ndarray], 
                          reference: np.ndarray) -> np.ndarray:
        """Select solution closest to reference configuration."""
        best_solution = None
        min_distance = np.inf
        
        for solution in solutions:
            distance = np.linalg.norm(solution - reference)
            if distance < min_distance:
                min_distance = distance
                best_solution = solution
        
        return best_solution
    
    def _select_by_singularity_avoidance(self, solutions: List[np.ndarray]) -> np.ndarray:
        """Select solution furthest from singularities."""
        best_solution = None
        max_distance = -np.inf
        
        for solution in solutions:
            jacobian = self.robot.get_jacobian(solution)
            distance = jacobian.distance_to_singularity()
            
            if distance > max_distance:
                max_distance = distance
                best_solution = solution
        
        return best_solution
    
    def _compute_joint_limit_margin(self, solution: np.ndarray) -> float:
        """Compute joint limit margin for a solution."""
        margin = np.inf
        
        for i, (q, (min_val, max_val)) in enumerate(zip(solution, self.robot.joint_limits)):
            joint_margin = min(q - min_val, max_val - q)
            margin = min(margin, joint_margin)
        
        return margin 