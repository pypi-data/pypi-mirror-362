"""
Simple Advanced Usage Example for the robot_kinematics library.
Demonstrates trajectory planning, performance comparison, and basic analysis.
"""

import numpy as np
import sys
import os
import time

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from robot_kinematics.robots.serial import UR5Manipulator
from robot_kinematics.inverse.numerical import NumericalIK
from robot_kinematics.inverse.hybrid import HybridIK
from robot_kinematics.utils.workspace import WorkspaceAnalyzer
from robot_kinematics.utils.singularity import SingularityAnalyzer
from robot_kinematics.core.transforms import Transform


def trajectory_planning_example():
    """Demonstrate trajectory planning with inverse kinematics."""
    print("\n=== Trajectory Planning Example ===")
    
    # Create robot
    robot = UR5Manipulator()
    
    # Define trajectory points (simpler path)
    trajectory = [
        Transform(position=np.array([0.4, 0.0, 0.5])),
        Transform(position=np.array([0.4, 0.05, 0.5])),
        Transform(position=np.array([0.4, 0.1, 0.5])),
        Transform(position=np.array([0.4, 0.1, 0.55])),
        Transform(position=np.array([0.4, 0.05, 0.55])),
        Transform(position=np.array([0.4, 0.0, 0.55]))
    ]
    num_points = len(trajectory)
    
    # Solve inverse kinematics for each point
    ik_solver = NumericalIK(robot=robot, method="damped_least_squares")
    joint_trajectory = []
    initial_guess = np.array([0, 0, 0, 0, 0, 0])
    
    for i, target_pose in enumerate(trajectory):
        try:
            solution, success, error = ik_solver.solve(target_pose, initial_guess)
            if success:
                joint_trajectory.append(solution)
                initial_guess = solution  # Use solution as next initial guess
                print(f"Point {i+1}/{num_points}: Success (error: {error:.6f})")
            else:
                print(f"Point {i+1}/{num_points}: Failed (error: {error:.6f})")
        except Exception as e:
            print(f"Point {i+1}/{num_points}: Error - {e}")
    
    print(f"Trajectory planning completed: {len(joint_trajectory)}/{num_points} points solved")
    return joint_trajectory


def performance_comparison_example():
    """Compare performance of different IK methods."""
    print("\n=== Performance Comparison Example ===")
    
    robot = UR5Manipulator()
    target_pose = Transform(position=np.array([0.4, 0.0, 0.5]))
    initial_guess = np.array([0, 0, 0, 0, 0, 0])
    
    methods = {
        "Damped Least Squares": NumericalIK(robot=robot, method="damped_least_squares"),
        "Levenberg-Marquardt": NumericalIK(robot=robot, method="levenberg_marquardt"),
        "Gradient Descent": NumericalIK(robot=robot, method="gradient_descent")
    }
    
    results = {}
    for name, solver in methods.items():
        start_time = time.time()
        try:
            solution, success, error = solver.solve(target_pose, initial_guess)
            end_time = time.time()
            
            results[name] = {
                'time': end_time - start_time,
                'success': success,
                'error': error,
                'solution': solution
            }
            
            print(f"{name}:")
            print(f"  Time: {results[name]['time']:.4f}s")
            print(f"  Success: {results[name]['success']}")
            print(f"  Error: {results[name]['error']:.6f}")
        except Exception as e:
            end_time = time.time()
            results[name] = {
                'time': end_time - start_time,
                'success': False,
                'error': float('inf'),
                'solution': None
            }
            print(f"{name}:")
            print(f"  Time: {results[name]['time']:.4f}s")
            print(f"  Success: False")
            print(f"  Error: Failed - {e}")
    
    return results


def workspace_analysis_example():
    """Demonstrate workspace analysis."""
    print("\n=== Workspace Analysis Example ===")
    
    robot = UR5Manipulator()
    analyzer = WorkspaceAnalyzer(robot)
    
    print("Analyzing workspace... (this may take a moment)")
    workspace_data = analyzer.generate_workspace_report(n_samples=1000)  # Reduced samples
    
    print(f"Workspace analysis completed:")
    if 'summary' in workspace_data:
        summary = workspace_data['summary']
        print(f"  Reachable workspace volume: {summary.get('reachable_volume', 'N/A')}")
        print(f"  Dexterous workspace volume: {summary.get('dexterous_volume', 'N/A')}")
        print(f"  Coverage ratio: {summary.get('coverage_ratio', 'N/A')}")
    
    return workspace_data


def singularity_analysis_example():
    """Demonstrate singularity analysis."""
    print("\n=== Singularity Analysis Example ===")
    
    robot = UR5Manipulator()
    analyzer = SingularityAnalyzer(robot)
    
    # Test a few joint configurations
    test_configs = [
        np.array([0, 0, 0, 0, 0, 0]),  # Home position
        np.array([np.pi/2, 0, 0, 0, 0, 0]),  # Joint 1 at 90 degrees
        np.array([0, np.pi/2, 0, 0, 0, 0]),  # Joint 2 at 90 degrees
        np.array([0, 0, np.pi/2, 0, 0, 0]),  # Joint 3 at 90 degrees
    ]
    
    for i, joint_config in enumerate(test_configs):
        print(f"\nTesting configuration {i+1}: {joint_config}")
        try:
            analysis = analyzer.detect_singularities(joint_config)
            print(f"  Is singular: {analysis['is_singular']}")
            print(f"  Manipulability: {analysis['manipulability']:.6f}")
            print(f"  Condition number: {analysis['condition_number']:.6f}")
        except Exception as e:
            print(f"  Analysis failed: {e}")
    
    return analyzer


def main():
    """Run all simple advanced examples."""
    print("Robot Kinematics Library - Simple Advanced Usage Examples")
    print("=" * 60)
    
    try:
        # Run examples
        trajectory_planning_example()
        performance_comparison_example()
        workspace_analysis_example()
        singularity_analysis_example()
        
        print("\n" + "=" * 60)
        print("All simple advanced examples completed successfully!")
        
    except Exception as e:
        print(f"Error in advanced examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 