"""
URDF Import/Export Demo

This example demonstrates how to:
1. Load a robot configuration from a URDF file
2. Create a URDF file from a robot configuration
3. Use the imported robot for kinematics calculations
"""

import numpy as np
import os
import tempfile
from robot_kinematics.integration.urdf_utils import load_robot_from_urdf, create_urdf_from_config
from robot_kinematics.robots.serial import SerialManipulator, KUKAKR5Manipulator
from robot_kinematics.inverse.numerical import NumericalIK
from robot_kinematics.core.transforms import Transform


def create_sample_urdf():
    """Create a sample URDF file for demonstration."""
    urdf_content = """<?xml version="1.0"?>
<robot name="sample_robot">
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.2"/>
      </geometry>
    </visual>
  </link>
  
  <joint name="joint_1" type="revolute">
    <parent link="base_link"/>
    <child link="link_1"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" effort="100" velocity="1"/>
  </joint>
  
  <link name="link_1">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.3"/>
      </geometry>
    </visual>
  </link>
  
  <joint name="joint_2" type="revolute">
    <parent link="link_1"/>
    <child link="link_2"/>
    <origin xyz="0 0 0.15" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-3.14" upper="3.14" effort="100" velocity="1"/>
  </joint>
  
  <link name="link_2">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.3"/>
      </geometry>
    </visual>
  </link>
  
  <joint name="joint_3" type="revolute">
    <parent link="link_2"/>
    <child link="link_3"/>
    <origin xyz="0 0 0.15" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-3.14" upper="3.14" effort="100" velocity="1"/>
  </joint>
  
  <link name="link_3">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.2"/>
      </geometry>
    </visual>
  </link>
</robot>"""
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.urdf', delete=False) as f:
        f.write(urdf_content)
        return f.name


def main():
    print("URDF Import/Export Demo")
    print("=" * 40)
    
    # 1. Create a sample URDF file
    print("\n1. Creating sample URDF file...")
    urdf_file = create_sample_urdf()
    print(f"Created URDF file: {urdf_file}")
    
    # 2. Load robot configuration from URDF
    print("\n2. Loading robot configuration from URDF...")
    try:
        config = load_robot_from_urdf(urdf_file)
        print(f"Robot name: {config['name']}")
        print(f"Number of joints: {config['n_joints']}")
        print(f"Joint types: {config['joint_types']}")
        print(f"Joint limits: {config['joint_limits']}")
        print(f"DH parameters: {config['dh_parameters']}")
    except Exception as e:
        print(f"Error loading URDF: {e}")
        return
    
    # 3. Create robot from imported configuration
    print("\n3. Creating robot from imported configuration...")
    try:
        robot = SerialManipulator(config)
        print(f"Robot created successfully: {robot.name}")
        
        # Test forward kinematics
        joint_config = np.array([0, 0, 0])
        pose = robot.forward_kinematics(joint_config)
        print(f"Home position: {pose.position}")
        
        # Test inverse kinematics
        target_pose = Transform(position=np.array([0.2, 0.0, 0.4]))
        ik_solver = NumericalIK(robot=robot, method="damped_least_squares")
        solution, success, error = ik_solver.solve(target_pose, joint_config)
        
        if success:
            print(f"IK solution: {solution}")
            print(f"IK error: {error}")
        else:
            print("IK failed to converge")
            
    except Exception as e:
        print(f"Error creating robot: {e}")
    
    # 4. Create URDF from KUKA KR5 configuration
    print("\n4. Creating URDF from KUKA KR5 configuration...")
    try:
        kuka = KUKAKR5Manipulator()
        kuka_config = {
            'name': kuka.name,
            'n_joints': kuka.n_joints,
            'joint_types': kuka.joint_types,
            'joint_limits': kuka.get_joint_limits(),
            'dh_parameters': kuka.dh_kinematics.dh_params
        }
        
        output_urdf = "kuka_kr5_generated.urdf"
        create_urdf_from_config(kuka_config, output_urdf)
        print(f"Generated URDF file: {output_urdf}")
        
        # Verify by loading back
        loaded_config = load_robot_from_urdf(output_urdf)
        print(f"Verified robot name: {loaded_config['name']}")
        print(f"Verified joints: {loaded_config['n_joints']}")
        
    except Exception as e:
        print(f"Error creating URDF: {e}")
    
    # 5. Cleanup
    print("\n5. Cleanup...")
    try:
        os.unlink(urdf_file)
        print(f"Removed temporary file: {urdf_file}")
    except:
        pass
    
    print("\n" + "=" * 40)
    print("URDF Import/Export Demo completed!")


if __name__ == "__main__":
    main() 