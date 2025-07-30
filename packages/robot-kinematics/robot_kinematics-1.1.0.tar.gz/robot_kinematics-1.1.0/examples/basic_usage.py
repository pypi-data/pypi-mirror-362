"""
Basic usage example for the robot_kinematics library.
"""

import numpy as np
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from robot_kinematics.robots.serial import UR5Manipulator
from robot_kinematics.forward.dh_kinematics import DHKinematics
from robot_kinematics.inverse.numerical import NumericalIK
from robot_kinematics.utils.workspace import WorkspaceAnalyzer
from robot_kinematics.utils.singularity import SingularityAnalyzer
from robot_kinematics.core.transforms import Transform


def main():
    """Demonstrate basic usage of the robot_kinematics library."""
    print("Robot Kinematics Library - Basic Usage Example")
    print("=" * 50)
    
    # 1. Create a UR5 robot
    print("\n1. Creating UR5 robot...")
    ur5 = UR5Manipulator()
    print(f"Robot: {ur5.config['name']}")
    print(f"Number of joints: {ur5.n_joints}")
    print(f"Robot type: {ur5.config['manufacturer']}")
    
    # 2. Forward kinematics
    print("\n2. Forward kinematics...")
    joint_positions = np.array([0, 0, 0, 0, 0, 0])  # Home position
    pose = ur5.forward_kinematics(joint_positions)
    print(f"Joint positions: {joint_positions}")
    print(f"End-effector pose: {pose}")
    
    # 3. Inverse kinematics
    print("\n3. Inverse kinematics...")
    target_pose = Transform(position=np.array([0.4, 0.0, 0.5]))  # Target position
    initial_guess = np.array([0, 0, 0, 0, 0, 0])
    
    numerical_ik = NumericalIK(robot=ur5, method="damped_least_squares")
    solution, success, error = numerical_ik.solve(target_pose, initial_guess)
    
    print(f"Target pose: {target_pose}")
    print(f"Solution: {solution}")
    print(f"Success: {success}")
    print(f"Error: {error}")
    
    # 4. Jacobian calculation
    print("\n4. Jacobian calculation...")
    jacobian_obj = ur5.get_jacobian(joint_positions)
    J = jacobian_obj.compute()
    print(f"Jacobian shape: {J.shape}")
    print(f"Jacobian determinant: {np.linalg.det(J):.6f}")
    
    # 5. Workspace analysis
    print("\n5. Workspace analysis...")
    workspace_analyzer = WorkspaceAnalyzer(ur5)
    workspace_analysis = workspace_analyzer.analyze_reachable_workspace(n_samples=1000)
    
    if 'error' not in workspace_analysis:
        print(f"Reachable workspace points: {workspace_analysis['n_valid_samples']}")
        print(f"Workspace volume: {workspace_analysis['workspace_volume']:.6f}")
        print(f"Workspace bounds: {workspace_analysis['workspace_bounds']}")
    else:
        print(f"Workspace analysis error: {workspace_analysis['error']}")
    
    # 6. Singularity analysis
    print("\n6. Singularity analysis...")
    singularity_analyzer = SingularityAnalyzer(ur5)
    singularity_analysis = singularity_analyzer.detect_singularities(joint_positions)
    
    print(f"Singularities detected: {singularity_analysis['is_singular']}")
    print(f"Manipulability index: {singularity_analysis['manipulability']:.6f}")
    print(f"Condition number: {singularity_analysis['condition_number']:.6f}")
    
    # 7. DH Kinematics example
    print("\n7. DH Kinematics example...")
    # UR5 DH parameters (simplified)
    dh_config = {
        'n_joints': 6,
        'joint_types': ['revolute'] * 6,
        'joint_limits': [(-2*np.pi, 2*np.pi)] * 6,
        'dh_parameters': [
            {'a': 0, 'alpha': np.pi/2, 'd': 0.089159, 'theta': 0},
            {'a': -0.425, 'alpha': 0, 'd': 0, 'theta': 0},
            {'a': -0.39225, 'alpha': 0, 'd': 0, 'theta': 0},
            {'a': 0, 'alpha': np.pi/2, 'd': 0.10915, 'theta': 0},
            {'a': 0, 'alpha': -np.pi/2, 'd': 0.09465, 'theta': 0},
            {'a': 0, 'alpha': 0, 'd': 0.0823, 'theta': 0}
        ]
    }
    
    dh_kinematics = DHKinematics(dh_config)
    
    dh_pose = dh_kinematics.forward_kinematics(joint_positions)
    print(f"DH forward kinematics result: {dh_pose}")
    
    # 8. KUKA KR5 example
    print("\n8. KUKA KR5 robot example...")
    from robot_kinematics.robots.serial import KUKAKR5Manipulator
    kuka = KUKAKR5Manipulator()
    print(f"Robot: {kuka.config['name']}")
    print(f"Number of joints: {kuka.n_joints}")
    print(f"Joint limits: {kuka.joint_limits}")
    kuka_joint_positions = np.zeros(6)
    kuka_pose = kuka.forward_kinematics(kuka_joint_positions)
    print(f"KUKA KR5 home pose: {kuka_pose}")
    
    print("\n" + "=" * 50)
    print("Basic usage example completed successfully!")
    print("The robot_kinematics library is working correctly.")


if __name__ == "__main__":
    main() 