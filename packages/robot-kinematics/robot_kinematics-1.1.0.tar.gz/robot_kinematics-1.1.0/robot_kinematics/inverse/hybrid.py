"""
Hybrid inverse kinematics approaches.

This module provides hybrid IK solvers that combine analytical and numerical methods for improved robustness and performance.
"""

import numpy as np
from typing import Optional, Dict, Any, List
from ..core.base import RobotKinematicsBase
from ..core.transforms import Transform
from ..core.exceptions import KinematicsError
from .analytical import AnalyticalIK
from .numerical import NumericalIK


class HybridIK:
    """
    Hybrid inverse kinematics solver.
    
    This class combines analytical and numerical IK methods for improved robustness and performance.
    """
    def __init__(self, robot: RobotKinematicsBase, analytical_first: bool = True):
        self.robot = robot
        self.analytical_first = analytical_first
        self.analytical_solver = AnalyticalIK(robot)
        self.numerical_solver = NumericalIK(robot)

    def solve(self, target_pose: Transform, initial_guess: Optional[np.ndarray] = None, **kwargs) -> np.ndarray:
        """
        Solve IK using hybrid approach.
        """
        if self.analytical_first:
            try:
                solutions = self.analytical_solver.solve(target_pose, **kwargs)
                if solutions:
                    return solutions[0]
            except KinematicsError:
                pass
        # Fallback to numerical
        return self.numerical_solver.solve(target_pose, initial_guess, **kwargs)

    def solve_multiple(self, target_pose: Transform, n_solutions: int = 8, **kwargs) -> List[np.ndarray]:
        """
        Find multiple IK solutions using both analytical and numerical methods.
        """
        solutions = []
        try:
            analytical_solutions = self.analytical_solver.solve(target_pose, **kwargs)
            solutions.extend(analytical_solutions)
        except KinematicsError:
            pass
        # Use numerical solver to find more solutions if needed
        if len(solutions) < n_solutions:
            numerical_solutions = self.numerical_solver.solve_multiple_solutions(target_pose, n_solutions=n_solutions-len(solutions), **kwargs)
            solutions.extend(numerical_solutions)
        return solutions[:n_solutions] 