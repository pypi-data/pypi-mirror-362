"""
Workspace analysis utilities for robotics kinematics.

This module provides tools for analyzing robot workspaces, including
reachable workspace, dexterous workspace, and workspace visualization.
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull
from ..core.base import RobotKinematicsBase
from ..core.transforms import Transform
from ..core.exceptions import KinematicsError


class WorkspaceAnalyzer:
    """
    Workspace analysis for robotic manipulators.
    
    This class provides comprehensive workspace analysis tools including
    reachable workspace calculation, dexterous workspace analysis, and
    workspace visualization.
    """
    
    def __init__(self, robot: RobotKinematicsBase):
        """
        Initialize workspace analyzer.
        
        Args:
            robot: Robot kinematics instance
        """
        self.robot = robot
        self.n_joints = robot.n_joints
    
    def analyze_reachable_workspace(self, n_samples: int = 10000, 
                                  resolution: float = 0.01) -> Dict[str, Any]:
        """
        Analyze reachable workspace.
        
        Args:
            n_samples: Number of random samples
            resolution: Spatial resolution for workspace discretization
            
        Returns:
            Workspace analysis results
        """
        positions = []
        valid_configs = []
        
        # Generate random joint configurations
        for _ in range(n_samples):
            # Random joint configuration within limits
            q = np.array([
                np.random.uniform(lim[0], lim[1]) for lim in self.robot.joint_limits
            ])
            
            try:
                # Compute forward kinematics
                pose = self.robot.forward_kinematics(q)
                positions.append(pose.position)
                valid_configs.append(q)
            except KinematicsError:
                continue
        
        if not positions:
            return {'error': 'No valid configurations found'}
        
        positions = np.array(positions)
        
        # Compute workspace metrics
        workspace_volume = self._compute_workspace_volume(positions)
        workspace_bounds = self._compute_workspace_bounds(positions)
        workspace_center = np.mean(positions, axis=0)
        
        # Analyze workspace shape
        workspace_shape = self._analyze_workspace_shape(positions)
        
        return {
            'positions': positions,
            'valid_configs': valid_configs,
            'workspace_volume': workspace_volume,
            'workspace_bounds': workspace_bounds,
            'workspace_center': workspace_center,
            'workspace_shape': workspace_shape,
            'n_valid_samples': len(positions),
            'coverage_ratio': len(positions) / n_samples
        }
    
    def analyze_dexterous_workspace(self, n_samples: int = 5000,
                                  orientation_tolerance: float = 0.1) -> Dict[str, Any]:
        """
        Analyze dexterous workspace (workspace with full orientation capability).
        
        Args:
            n_samples: Number of random samples
            orientation_tolerance: Tolerance for orientation reachability
            
        Returns:
            Dexterous workspace analysis results
        """
        dexterous_positions = []
        dexterous_configs = []
        
        # Test orientations at each position
        test_orientations = self._generate_test_orientations()
        
        for _ in range(n_samples):
            # Random joint configuration
            q = np.array([
                np.random.uniform(lim[0], lim[1]) for lim in self.robot.joint_limits
            ])
            
            try:
                # Get current pose
                current_pose = self.robot.forward_kinematics(q)
                current_pos = current_pose.position
                
                # Test if all orientations are reachable at this position
                is_dexterous = True
                
                for target_orientation in test_orientations:
                    target_pose = Transform(
                        position=current_pos,
                        rotation=target_orientation
                    )
                    
                    try:
                        # Try to solve IK with more iterations and relaxed tolerance
                        ik_solution = self.robot.inverse_kinematics(
                            target_pose, 
                            initial_guess=q,
                            max_iterations=200,
                            tolerance=1e-2
                        )
                        # If the solution is a tuple/list, extract the first element if needed
                        if isinstance(ik_solution, (tuple, list)):
                            ik_solution = np.asarray(ik_solution[0])
                        else:
                            ik_solution = np.asarray(ik_solution)
                        # Only proceed if the solution is 1D and matches n_joints
                        if ik_solution.ndim != 1 or ik_solution.shape[0] != self.n_joints:
                            is_dexterous = False
                            break
                        # Check if solution is close enough
                        achieved_pose = self.robot.forward_kinematics(ik_solution)
                        orientation_error = self._compute_orientation_error(
                            achieved_pose.rotation, target_orientation
                        )
                        if orientation_error > orientation_tolerance:
                            is_dexterous = False
                            break
                            
                    except KinematicsError:
                        is_dexterous = False
                        break
                
                if is_dexterous:
                    dexterous_positions.append(current_pos)
                    dexterous_configs.append(q)
                    
            except KinematicsError:
                continue
        
        if not dexterous_positions:
            return {'error': 'No dexterous workspace found'}
        
        dexterous_positions = np.array(dexterous_positions)
        
        # Compute dexterous workspace metrics
        dexterous_volume = self._compute_workspace_volume(dexterous_positions)
        dexterous_bounds = self._compute_workspace_bounds(dexterous_positions)
        
        return {
            'dexterous_positions': dexterous_positions,
            'dexterous_configs': dexterous_configs,
            'dexterous_volume': dexterous_volume,
            'dexterous_bounds': dexterous_bounds,
            'n_dexterous_samples': len(dexterous_positions),
            'dexterity_ratio': len(dexterous_positions) / n_samples
        }
    
    def analyze_workspace_quality(self, positions: np.ndarray) -> Dict[str, Any]:
        """
        Analyze workspace quality metrics.
        
        Args:
            positions: Workspace positions
            
        Returns:
            Quality analysis results
        """
        if len(positions) == 0:
            return {'error': 'No positions provided'}
        
        # Compute manipulability at each position
        manipulabilities = []
        condition_numbers = []
        
        for pos in positions:
            try:
                # Find a joint configuration that reaches this position
                # This is a simplified approach - in practice, you'd need IK
                q = np.zeros(self.n_joints)
                pose = Transform(position=pos)
                
                try:
                    ik_solution = self.robot.inverse_kinematics(pose, q)
                    jacobian = self.robot.get_jacobian(ik_solution)
                    
                    manipulabilities.append(jacobian.manipulability())
                    condition_numbers.append(jacobian.condition_number())
                except KinematicsError:
                    manipulabilities.append(0.0)
                    condition_numbers.append(np.inf)
                    
            except Exception:
                manipulabilities.append(0.0)
                condition_numbers.append(np.inf)
        
        manipulabilities = np.array(manipulabilities)
        condition_numbers = np.array(condition_numbers)
        
        # Filter out invalid values
        valid_manip = manipulabilities[manipulabilities > 0]
        valid_cond = condition_numbers[condition_numbers < np.inf]
        
        return {
            'mean_manipulability': np.mean(valid_manip) if len(valid_manip) > 0 else 0.0,
            'std_manipulability': np.std(valid_manip) if len(valid_manip) > 0 else 0.0,
            'min_manipulability': np.min(valid_manip) if len(valid_manip) > 0 else 0.0,
            'max_manipulability': np.max(valid_manip) if len(valid_manip) > 0 else 0.0,
            'mean_condition_number': np.mean(valid_cond) if len(valid_cond) > 0 else np.inf,
            'std_condition_number': np.std(valid_cond) if len(valid_cond) > 0 else 0.0,
            'workspace_uniformity': self._compute_uniformity(positions),
            'workspace_compactness': self._compute_compactness(positions)
        }
    
    def visualize_workspace(self, positions: np.ndarray, 
                           dexterous_positions: Optional[np.ndarray] = None,
                           save_path: Optional[str] = None) -> None:
        """
        Visualize workspace.
        
        Args:
            positions: All workspace positions
            dexterous_positions: Dexterous workspace positions
            save_path: Path to save the plot
        """
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot reachable workspace
        if len(positions) > 0:
            ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], 
                      c='blue', alpha=0.6, s=1, label='Reachable Workspace')
        
        # Plot dexterous workspace
        if dexterous_positions is not None and len(dexterous_positions) > 0:
            ax.scatter(dexterous_positions[:, 0], dexterous_positions[:, 1], 
                      dexterous_positions[:, 2], c='red', alpha=0.8, s=2, 
                      label='Dexterous Workspace')
        
        # Plot robot base
        ax.scatter([0], [0], [0], c='black', s=100, marker='s', label='Robot Base')
        
        # Set labels and title
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title(f'Workspace Analysis - {self.robot.__class__.__name__}')
        
        # Set equal aspect ratio
        ax.set_box_aspect([1, 1, 1])
        
        # Add legend
        ax.legend()
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def generate_workspace_report(self, n_samples: int = 10000) -> Dict[str, Any]:
        """
        Generate comprehensive workspace report.
        
        Args:
            n_samples: Number of samples for analysis
            
        Returns:
            Complete workspace report
        """
        # Analyze reachable workspace
        reachable_analysis = self.analyze_reachable_workspace(n_samples)
        
        if 'error' in reachable_analysis:
            return reachable_analysis
        
        # Analyze dexterous workspace
        dexterous_analysis = self.analyze_dexterous_workspace(n_samples // 2)
        
        # Analyze workspace quality
        quality_analysis = self.analyze_workspace_quality(reachable_analysis['positions'])
        
        # Combine results
        report = {
            'robot_info': self.robot.get_robot_info(),
            'reachable_workspace': reachable_analysis,
            'dexterous_workspace': dexterous_analysis,
            'workspace_quality': quality_analysis,
            'summary': self._generate_summary(reachable_analysis, dexterous_analysis, quality_analysis)
        }
        
        return report
    
    def _compute_workspace_volume(self, positions: np.ndarray) -> float:
        """Compute workspace volume using convex hull."""
        if len(positions) < 4:
            return 0.0
        
        try:
            hull = ConvexHull(positions)
            return hull.volume
        except:
            # Fallback: bounding box volume
            ranges = np.ptp(positions, axis=0)
            return np.prod(ranges)
    
    def _compute_workspace_bounds(self, positions: np.ndarray) -> Dict[str, Tuple[float, float]]:
        """Compute workspace bounds."""
        if len(positions) == 0:
            return {'x': (0, 0), 'y': (0, 0), 'z': (0, 0)}
        
        bounds = {
            'x': (np.min(positions[:, 0]), np.max(positions[:, 0])),
            'y': (np.min(positions[:, 1]), np.max(positions[:, 1])),
            'z': (np.min(positions[:, 2]), np.max(positions[:, 2]))
        }
        
        return bounds
    
    def _analyze_workspace_shape(self, positions: np.ndarray) -> Dict[str, Any]:
        """Analyze workspace shape characteristics."""
        if len(positions) < 3:
            return {'type': 'unknown', 'aspect_ratio': 1.0}
        
        # Compute principal components
        centered = positions - np.mean(positions, axis=0)
        cov_matrix = np.cov(centered.T)
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
        
        # Sort eigenvalues in descending order
        sorted_indices = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[sorted_indices]
        eigenvectors = eigenvectors[:, sorted_indices]
        
        # Determine shape type
        aspect_ratios = eigenvalues / np.max(eigenvalues)
        
        if aspect_ratios[1] > 0.8:
            shape_type = 'spherical'
        elif aspect_ratios[2] < 0.3:
            shape_type = 'planar'
        else:
            shape_type = 'cylindrical'
        
        return {
            'type': shape_type,
            'aspect_ratios': aspect_ratios,
            'principal_axes': eigenvectors,
            'eigenvalues': eigenvalues
        }
    
    def _generate_test_orientations(self) -> List[np.ndarray]:
        """Generate test orientations for dexterity analysis."""
        orientations = []
        
        # Generate orientations around different axes
        for axis in [[1, 0, 0], [0, 1, 0], [0, 0, 1]]:
            for angle in np.linspace(0, 2*np.pi, 8):
                # Create rotation matrix
                c, s = np.cos(angle), np.sin(angle)
                R = np.array([
                    [c + axis[0]**2*(1-c), axis[0]*axis[1]*(1-c) - axis[2]*s, axis[0]*axis[2]*(1-c) + axis[1]*s],
                    [axis[1]*axis[0]*(1-c) + axis[2]*s, c + axis[1]**2*(1-c), axis[1]*axis[2]*(1-c) - axis[0]*s],
                    [axis[2]*axis[0]*(1-c) - axis[1]*s, axis[2]*axis[1]*(1-c) + axis[0]*s, c + axis[2]**2*(1-c)]
                ])
                orientations.append(R)
        
        return orientations
    
    def _compute_orientation_error(self, R1: np.ndarray, R2: np.ndarray) -> float:
        """Compute orientation error between two rotation matrices."""
        error_matrix = R1.T @ R2
        trace = np.trace(error_matrix)
        error = np.arccos(np.clip((trace - 1) / 2, -1, 1))
        return abs(error)
    
    def _compute_uniformity(self, positions: np.ndarray) -> float:
        """Compute workspace uniformity."""
        if len(positions) < 2:
            return 0.0
        
        # Compute nearest neighbor distances
        from scipy.spatial.distance import cdist
        distances = cdist(positions, positions)
        
        # Remove self-distances
        np.fill_diagonal(distances, np.inf)
        min_distances = np.min(distances, axis=1)
        
        # Uniformity is inverse of standard deviation of nearest neighbor distances
        uniformity = 1.0 / (1.0 + np.std(min_distances))
        return uniformity
    
    def _compute_compactness(self, positions: np.ndarray) -> float:
        """Compute workspace compactness."""
        if len(positions) < 2:
            return 0.0
        
        # Compactness is volume / surface area ratio
        volume = self._compute_workspace_volume(positions)
        
        try:
            hull = ConvexHull(positions)
            surface_area = hull.area
            compactness = volume / surface_area if surface_area > 0 else 0.0
        except:
            compactness = 0.0
        
        return compactness
    
    def _generate_summary(self, reachable: Dict, dexterous: Dict, quality: Dict) -> Dict[str, Any]:
        """Generate workspace summary."""
        return {
            'total_workspace_volume': reachable.get('workspace_volume', 0.0),
            'dexterous_workspace_volume': dexterous.get('dexterous_volume', 0.0),
            'dexterity_ratio': dexterous.get('dexterity_ratio', 0.0),
            'mean_manipulability': quality.get('mean_manipulability', 0.0),
            'workspace_uniformity': quality.get('workspace_uniformity', 0.0),
            'workspace_compactness': quality.get('workspace_compactness', 0.0)
        }


class WorkspaceOptimizer:
    """
    Workspace optimization tools.
    
    This class provides tools for optimizing robot placement and configuration
    to maximize workspace coverage and quality.
    """
    
    def __init__(self, robot: RobotKinematicsBase):
        """
        Initialize workspace optimizer.
        
        Args:
            robot: Robot kinematics instance
        """
        self.robot = robot
        self.analyzer = WorkspaceAnalyzer(robot)
    
    def optimize_base_placement(self, target_workspace: np.ndarray,
                               n_trials: int = 100) -> Dict[str, Any]:
        """
        Optimize robot base placement for maximum workspace coverage.
        
        Args:
            target_workspace: Target workspace points
            n_trials: Number of optimization trials
            
        Returns:
            Optimization results
        """
        best_placement = None
        best_coverage = 0.0
        
        for trial in range(n_trials):
            # Random base placement
            base_position = np.random.uniform(-1.0, 1.0, 3)
            base_rotation = np.random.uniform(-np.pi/4, np.pi/4, 3)
            
            # Create base transformation
            from ..core.transforms import euler_to_rotation_matrix
            base_rotation_matrix = euler_to_rotation_matrix(base_rotation)
            base_transform = Transform(position=base_position, rotation=base_rotation_matrix)
            
            # Update robot base
            original_base = self.robot.base_transform
            self.robot.base_transform = base_transform
            
            # Analyze workspace
            try:
                analysis = self.analyzer.analyze_reachable_workspace(n_samples=1000)
                
                if 'error' not in analysis:
                    # Compute coverage of target workspace
                    coverage = self._compute_target_coverage(
                        analysis['positions'], target_workspace
                    )
                    
                    if coverage > best_coverage:
                        best_coverage = coverage
                        best_placement = {
                            'position': base_position,
                            'rotation': base_rotation,
                            'transform': base_transform,
                            'coverage': coverage
                        }
            except:
                pass
            
            # Restore original base
            self.robot.base_transform = original_base
        
        return {
            'best_placement': best_placement,
            'best_coverage': best_coverage,
            'n_trials': n_trials
        }
    
    def _compute_target_coverage(self, workspace_positions: np.ndarray, 
                               target_positions: np.ndarray) -> float:
        """Compute coverage of target workspace."""
        if len(workspace_positions) == 0 or len(target_positions) == 0:
            return 0.0
        
        # Compute distances from target points to workspace
        from scipy.spatial.distance import cdist
        distances = cdist(target_positions, workspace_positions)
        min_distances = np.min(distances, axis=1)
        
        # Count points within reach (assuming 0.1m tolerance)
        tolerance = 0.1
        covered_points = np.sum(min_distances < tolerance)
        coverage = covered_points / len(target_positions)
        
        return coverage 