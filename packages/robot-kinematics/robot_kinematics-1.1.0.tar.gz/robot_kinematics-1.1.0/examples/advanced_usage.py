"""
Advanced usage example for the robot_kinematics library.
Demonstrates complex features like trajectory planning, performance optimization,
and advanced analysis techniques.
"""

import numpy as np
import sys
import os
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from robot_kinematics.robots.serial import UR5Manipulator, PandaManipulator
from robot_kinematics.robots.parallel import StewartPlatform
from robot_kinematics.forward.dh_kinematics import DHKinematics
from robot_kinematics.inverse.numerical import NumericalIK
from robot_kinematics.inverse.analytical import AnalyticalIK
from robot_kinematics.inverse.hybrid import HybridIK
from robot_kinematics.utils.workspace import WorkspaceAnalyzer
from robot_kinematics.utils.singularity import SingularityAnalyzer
from robot_kinematics.utils.performance import PerformanceOptimizer
from robot_kinematics.core.transforms import Transform


def trajectory_planning_example():
    """Demonstrate trajectory planning with inverse kinematics."""
    print("\n=== Trajectory Planning Example ===")
    
    # Create robot
    robot = UR5Manipulator()
    
    # Define trajectory points (circular path) - reduced radius to ensure reachability
    center = np.array([0.4, 0.0, 0.5])
    radius = 0.05  # Reduced from 0.1 to 0.05
    num_points = 20
    angles = np.linspace(0, 2*np.pi, num_points)
    
    trajectory = []
    for angle in angles:
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        z = center[2]
        pose = Transform(position=np.array([x, y, z]))  # Use Transform object
        trajectory.append(pose)
    
    # Solve inverse kinematics for each point
    ik_solver = NumericalIK(robot=robot, method="damped_least_squares")
    joint_trajectory = []
    initial_guess = np.array([0, 0, 0, 0, 0, 0])
    
    for i, target_pose in enumerate(trajectory):
        solution, success, error = ik_solver.solve(target_pose, initial_guess, max_iterations=500, tolerance=1e-3)
        if success:
            joint_trajectory.append(solution)
            initial_guess = solution  # Use solution as next initial guess
            print(f"Point {i+1}/{num_points}: Success (error: {error:.6f})")
        else:
            print(f"Point {i+1}/{num_points}: Failed (error: {error:.6f})")
    
    print(f"Trajectory planning completed: {len(joint_trajectory)}/{num_points} points solved")
    return joint_trajectory


def performance_comparison_example():
    """Compare performance of different IK methods."""
    print("\n=== Performance Comparison Example ===")
    
    robot = UR5Manipulator()
    target_pose = Transform(position=np.array([0.4, 0.0, 0.5]))  # Use Transform object
    initial_guess = np.array([0, 0, 0, 0, 0, 0])
    
    methods = {
        "Damped Least Squares": NumericalIK(robot=robot, method="damped_least_squares"),
        "Levenberg-Marquardt": NumericalIK(robot=robot, method="levenberg_marquardt"),
        "Hybrid": HybridIK(robot=robot)
    }
    
    results = {}
    for name, solver in methods.items():
        start_time = time.time()
        if name == "Hybrid":
            try:
                solution = solver.solve(target_pose, initial_guess, max_iterations=500, tolerance=1e-3)
                # Try to compute error and success
                final_pose = robot.forward_kinematics(solution)
                error = float(np.linalg.norm(final_pose.position - target_pose.position))
                success = error < 1e-2
            except Exception as e:
                solution = None
                error = float('inf')
                success = False
        else:
            solution, success, error = solver.solve(target_pose, initial_guess, max_iterations=500, tolerance=1e-3)
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
    
    return results


def workspace_visualization_example():
    """Demonstrate workspace analysis and visualization."""
    print("\n=== Workspace Visualization Example ===")
    
    robot = UR5Manipulator()
    analyzer = WorkspaceAnalyzer(robot)
    
    print("Analyzing workspace... (this may take a moment)")
    workspace_data = analyzer.generate_workspace_report()
    
    # Extract points for visualization
    if 'reachable_workspace' in workspace_data:
        reachable_points = np.array(workspace_data['reachable_workspace']['positions'])
    else:
        reachable_points = np.array([])
    
    if 'dexterous_workspace' in workspace_data and 'dexterous_positions' in workspace_data['dexterous_workspace']:
        dexterous_points = np.array(workspace_data['dexterous_workspace']['dexterous_positions'])
    else:
        dexterous_points = np.array([])
    
    print(f"Reachable points: {len(reachable_points)}")
    print(f"Dexterous points: {len(dexterous_points)}")
    print(f"Workspace summary: {workspace_data.get('summary', {})}")
    
    # Create 3D visualization
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    if len(reachable_points) > 0:
        ax.scatter(reachable_points[:, 0], reachable_points[:, 1], reachable_points[:, 2], 
                  c='blue', alpha=0.6, s=1, label='Reachable Workspace')
    
    if len(dexterous_points) > 0:
        ax.scatter(dexterous_points[:, 0], dexterous_points[:, 1], dexterous_points[:, 2], 
                  c='red', alpha=0.8, s=2, label='Dexterous Workspace')
    
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Robot Workspace Analysis')
    ax.legend()
    
    # Save the plot
    plt.savefig('workspace_visualization.png', dpi=300, bbox_inches='tight')
    print("Workspace visualization saved as 'workspace_visualization.png'")
    
    return workspace_data


def singularity_analysis_example():
    """Demonstrate singularity analysis across joint space."""
    print("\n=== Singularity Analysis Example ===")
    
    robot = UR5Manipulator()
    analyzer = SingularityAnalyzer(robot)
    
    # Sample joint configurations
    joint_samples = []
    for i in range(10):
        for j in range(10):
            for k in range(5):
                joint_config = np.array([
                    i * np.pi/5, j * np.pi/5, k * np.pi/10, 0, 0, 0
                ])
                joint_samples.append(joint_config)
    
    singularity_data = []
    manipulability_scores = []
    
    for i, joint_config in enumerate(joint_samples):
        analysis = analyzer.detect_singularities(joint_config)
        singularity_data.append(analysis)
        manipulability_scores.append(analysis['manipulability'])
        
        if i % 50 == 0:
            print(f"Analyzed {i+1}/{len(joint_samples)} configurations")
    
    # Find configurations with low manipulability
    low_manipulability = [i for i, score in enumerate(manipulability_scores) if score < 0.01]
    
    print(f"Total configurations analyzed: {len(joint_samples)}")
    print(f"Configurations with low manipulability: {len(low_manipulability)}")
    print(f"Average manipulability: {np.mean(manipulability_scores):.6f}")
    print(f"Min manipulability: {np.min(manipulability_scores):.6f}")
    
    return singularity_data, manipulability_scores


def parallel_robot_example():
    """Demonstrate parallel robot kinematics."""
    print("\n=== Parallel Robot Example ===")
    
    # Create Stewart platform
    stewart_config = {
        'n_joints': 6,  # Add the required n_joints parameter
        'joint_types': ['prismatic'] * 6,  # Add joint types
        'joint_limits': [(0.2, 0.4)] * 6,  # Add joint limits
        'base_radius': 0.2,
        'platform_radius': 0.1,
        'leg_length': 0.3,
        'n_legs': 6
    }
    stewart = StewartPlatform(stewart_config)
    
    print(f"Stewart Platform created:")
    print(f"  Base radius: {stewart_config['base_radius']}m")
    print(f"  Platform radius: {stewart_config['platform_radius']}m")
    print(f"  Leg length: {stewart_config['leg_length']}m")
    print(f"  Number of legs: {stewart_config['n_legs']}")
    
    # Forward kinematics
    from robot_kinematics.core.transforms import Transform
    platform_pose = Transform(position=np.array([0, 0, 0.25]))
    leg_lengths = stewart.inverse_kinematics(platform_pose)
    
    print(f"Platform pose: {platform_pose.position}")
    print(f"Required leg lengths: {leg_lengths}")
    
    # Verify with forward kinematics
    calculated_pose = stewart.forward_kinematics(leg_lengths)
    print(f"Calculated pose: {calculated_pose.position}")
    
    return stewart, leg_lengths


def optimization_example():
    """Demonstrate performance optimization."""
    print("\n=== Performance Optimization Example ===")
    
    robot = UR5Manipulator()
    optimizer = PerformanceOptimizer(robot)
    
    # Benchmark forward kinematics
    print("\nBenchmarking forward kinematics...")
    fk_metrics = optimizer.benchmark_forward_kinematics(n_samples=100)
    print(f"FK Performance metrics: {fk_metrics}")
    
    # Benchmark inverse kinematics
    print("\nBenchmarking inverse kinematics...")
    ik_metrics = optimizer.benchmark_inverse_kinematics(n_samples=10)
    print(f"IK Performance metrics: {ik_metrics}")
    
    # Test caching
    print("\nTesting caching...")
    optimizer.enable_caching(max_cache_size=1000)
    cache_stats = optimizer.get_cache_stats()
    print(f"Cache stats: {cache_stats}")
    
    # Test vectorized operations
    print("\nTesting vectorized operations...")
    from robot_kinematics.utils.performance import VectorizedKinematics
    vectorized = VectorizedKinematics(robot)
    
    # Generate test configurations
    joint_configs = np.random.uniform(-np.pi, np.pi, (10, robot.n_joints))
    
    try:
        poses = vectorized.vectorized_forward_kinematics(joint_configs)
        print(f"Vectorized FK completed: {len(poses)} poses calculated")
    except Exception as e:
        print(f"Vectorized FK failed: {e}")
    
    return optimizer


def main():
    """Run all advanced examples."""
    print("Robot Kinematics Library - Advanced Usage Examples")
    print("=" * 60)
    
    try:
        # Run examples
        trajectory_planning_example()
        performance_comparison_example()
        workspace_visualization_example()
        singularity_analysis_example()
        parallel_robot_example()
        optimization_example()
        
        print("\n" + "=" * 60)
        print("All advanced examples completed successfully!")
        print("Check 'workspace_visualization.png' for workspace visualization.")
        
    except Exception as e:
        print(f"Error in advanced examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 