"""
URDF-based kinematics implementation.

This module provides kinematics calculations based on URDF (Unified Robot Description Format)
files, which are commonly used in ROS and other robotics frameworks.
"""

import numpy as np
from typing import Dict, Any, List, Optional
import xml.etree.ElementTree as ET
from ..core.base import RobotKinematicsBase
from ..core.transforms import Transform
from ..core.exceptions import URDFError, KinematicsError


class URDFKinematics(RobotKinematicsBase):
    """
    URDF-based kinematics implementation.
    
    This class provides forward and inverse kinematics calculations
    based on URDF robot descriptions.
    """
    
    def __init__(self, urdf_file: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize URDF kinematics.
        
        Args:
            urdf_file: Path to URDF file
            config: Additional configuration parameters
        """
        if config is None:
            config = {}
        
        # Parse URDF file
        self.urdf_data = self._parse_urdf(urdf_file)
        
        # Extract robot information
        robot_info = self._extract_robot_info()
        config.update(robot_info)
        
        super().__init__(config)
        
        # Build kinematic chain
        self.kinematic_chain = self._build_kinematic_chain()
    
    def _parse_urdf(self, urdf_file: str) -> ET.Element:
        """
        Parse URDF file.
        
        Args:
            urdf_file: Path to URDF file
            
        Returns:
            Parsed URDF XML element
        """
        try:
            tree = ET.parse(urdf_file)
            root = tree.getroot()
            
            # Validate that this is a robot description
            if root.tag != 'robot':
                raise URDFError("URDF file must contain a 'robot' root element")
            
            return root
            
        except ET.ParseError as e:
            raise URDFError(f"Failed to parse URDF file: {e}")
        except FileNotFoundError:
            raise URDFError(f"URDF file not found: {urdf_file}")
    
    def _extract_robot_info(self) -> Dict[str, Any]:
        """
        Extract robot information from URDF.
        
        Returns:
            Robot configuration dictionary
        """
        # Extract robot name
        robot_name = self.urdf_data.get('name', 'unknown')
        
        # Find all joints
        joints = self.urdf_data.findall('joint')
        
        # Extract joint information
        joint_types = []
        joint_limits = []
        joint_names = []
        
        for joint in joints:
            joint_name = joint.get('name')
            joint_type = joint.get('type')
            
            if joint_type in ['revolute', 'prismatic']:
                joint_names.append(joint_name)
                joint_types.append(joint_type)
                
                # Extract joint limits
                limit_elem = joint.find('limit')
                if limit_elem is not None:
                    lower = float(limit_elem.get('lower', -np.pi))
                    upper = float(limit_elem.get('upper', np.pi))
                    joint_limits.append((lower, upper))
                else:
                    # Default limits
                    if joint_type == 'revolute':
                        joint_limits.append((-np.pi, np.pi))
                    else:
                        joint_limits.append((0.0, 1.0))
        
        return {
            'name': robot_name,
            'n_joints': len(joint_types),
            'joint_types': joint_types,
            'joint_limits': joint_limits,
            'joint_names': joint_names
        }
    
    def _build_kinematic_chain(self) -> List[Dict[str, Any]]:
        """
        Build kinematic chain from URDF.
        
        Returns:
            List of link transformations
        """
        chain = []
        
        # Find all links
        links = self.urdf_data.findall('link')
        joints = self.urdf_data.findall('joint')
        
        # Build link-to-joint mapping
        link_joint_map = {}
        for joint in joints:
            parent = joint.find('parent')
            child = joint.find('child')
            
            if parent is not None and child is not None:
                parent_link = parent.get('link')
                child_link = child.get('link')
                link_joint_map[child_link] = joint
        
        # Find base link (link with no parent joint)
        base_link = None
        for link in links:
            link_name = link.get('name')
            if link_name not in link_joint_map:
                base_link = link_name
                break
        
        if base_link is None:
            raise URDFError("Could not find base link in URDF")
        
        # Build chain starting from base
        current_link = base_link
        while current_link in link_joint_map:
            joint = link_joint_map[current_link]
            
            # Extract joint information
            joint_info = self._extract_joint_info(joint)
            chain.append(joint_info)
            
            # Move to child link
            child_elem = joint.find('child')
            if child_elem is not None:
                current_link = child_elem.get('link')
            else:
                break
        
        return chain
    
    def _extract_joint_info(self, joint_elem: ET.Element) -> Dict[str, Any]:
        """
        Extract joint information from URDF joint element.
        
        Args:
            joint_elem: Joint XML element
            
        Returns:
            Joint information dictionary
        """
        joint_info = {
            'name': joint_elem.get('name'),
            'type': joint_elem.get('type'),
            'axis': [0, 0, 1],  # Default Z-axis
            'origin': np.eye(4),  # Default identity transformation
            'parent_link': None,
            'child_link': None
        }
        
        # Extract axis
        axis_elem = joint_elem.find('axis')
        if axis_elem is not None:
            xyz = axis_elem.get('xyz', '0 0 1')
            joint_info['axis'] = [float(x) for x in xyz.split()]
        
        # Extract origin transformation
        origin_elem = joint_elem.find('origin')
        if origin_elem is not None:
            xyz = origin_elem.get('xyz', '0 0 0')
            rpy = origin_elem.get('rpy', '0 0 0')
            
            # Parse position and orientation
            pos = [float(x) for x in xyz.split()]
            rpy_angles = [float(x) for x in rpy.split()]
            
            # Create transformation matrix
            from ..core.transforms import euler_to_rotation_matrix
            rot_matrix = euler_to_rotation_matrix(rpy_angles, convention='xyz')
            
            T = np.eye(4)
            T[:3, :3] = rot_matrix
            T[:3, 3] = pos
            
            joint_info['origin'] = T
        
        # Extract parent and child links
        parent_elem = joint_elem.find('parent')
        child_elem = joint_elem.find('child')
        
        if parent_elem is not None:
            joint_info['parent_link'] = parent_elem.get('link')
        if child_elem is not None:
            joint_info['child_link'] = child_elem.get('link')
        
        return joint_info
    
    def forward_kinematics(self, joint_config: np.ndarray) -> Transform:
        """
        Compute forward kinematics using URDF chain.
        
        Args:
            joint_config: Joint configuration vector
            
        Returns:
            End-effector pose
        """
        joint_config = np.asarray(joint_config).flatten()
        
        if len(joint_config) != self.n_joints:
            raise KinematicsError(f"Joint configuration length ({len(joint_config)}) must match number of joints ({self.n_joints})")
        
        # Start with base transformation
        T = self.base_transform.matrix.copy()
        
        # Apply transformations for each joint in the chain
        for i, joint_info in enumerate(self.kinematic_chain):
            if i >= len(joint_config):
                break
            
            # Get joint value
            q = joint_config[i]
            
            # Compute joint transformation
            T_joint = self._compute_joint_transform(joint_info, q)
            
            # Apply to chain
            T = T @ T_joint
        
        # Apply tool transformation
        T = T @ self.tool_transform.matrix
        
        return Transform(T)
    
    def _compute_joint_transform(self, joint_info: Dict[str, Any], joint_value: float) -> np.ndarray:
        """
        Compute transformation for a joint.
        
        Args:
            joint_info: Joint information dictionary
            joint_value: Joint value
            
        Returns:
            Joint transformation matrix
        """
        # Start with origin transformation
        T = joint_info['origin'].copy()
        
        # Apply joint transformation based on type
        joint_type = joint_info['type']
        axis = joint_info['axis']
        
        if joint_type == 'revolute':
            # Create rotation matrix around joint axis
            from ..core.transforms import axis_angle_to_rotation_matrix
            rot_matrix = axis_angle_to_rotation_matrix(axis, joint_value)
            
            # Apply rotation to origin transformation
            T_rot = np.eye(4)
            T_rot[:3, :3] = rot_matrix
            T = T @ T_rot
            
        elif joint_type == 'prismatic':
            # Create translation along joint axis
            translation = np.array(axis) * joint_value
            
            # Apply translation to origin transformation
            T[:3, 3] += translation
        
        return T
    
    def get_joint_transform(self, joint_idx: int, joint_config: np.ndarray) -> Transform:
        """
        Get transformation to a specific joint.
        
        Args:
            joint_idx: Joint index
            joint_config: Joint configuration vector
            
        Returns:
            Transformation to joint
        """
        if joint_idx < 0 or joint_idx >= len(self.kinematic_chain):
            raise KinematicsError(f"Invalid joint index: {joint_idx}")
        
        joint_config = np.asarray(joint_config).flatten()
        
        # Start with base transformation
        T = self.base_transform.matrix.copy()
        
        # Apply transformations up to the specified joint
        for i in range(joint_idx + 1):
            if i >= len(self.kinematic_chain):
                break
            
            joint_info = self.kinematic_chain[i]
            q = joint_config[i] if i < len(joint_config) else 0.0
            
            T_joint = self._compute_joint_transform(joint_info, q)
            T = T @ T_joint
        
        return Transform(T)
    
    def inverse_kinematics(self, target_pose: Transform, 
                          initial_guess: Optional[np.ndarray] = None,
                          **kwargs) -> np.ndarray:
        """
        Compute inverse kinematics (delegates to numerical solver).
        
        Args:
            target_pose: Target end-effector pose
            initial_guess: Initial joint configuration guess
            **kwargs: Additional solver parameters
            
        Returns:
            Joint configuration
        """
        # This is a placeholder - actual IK is implemented in inverse/ module
        from ..inverse.numerical import NumericalIK
        ik_solver = NumericalIK(self)
        return ik_solver.solve(target_pose, initial_guess, **kwargs)
    
    def get_urdf_info(self) -> Dict[str, Any]:
        """Get URDF-specific information."""
        return {
            'robot_name': self.urdf_data.get('name'),
            'kinematic_chain': self.kinematic_chain,
            'joint_names': [joint['name'] for joint in self.kinematic_chain],
            'link_names': [joint['child_link'] for joint in self.kinematic_chain]
        }


def load_urdf_robot(urdf_file: str, **kwargs) -> URDFKinematics:
    """
    Load robot from URDF file.
    
    Args:
        urdf_file: Path to URDF file
        **kwargs: Additional configuration parameters
        
    Returns:
        URDF kinematics instance
    """
    return URDFKinematics(urdf_file, kwargs) 