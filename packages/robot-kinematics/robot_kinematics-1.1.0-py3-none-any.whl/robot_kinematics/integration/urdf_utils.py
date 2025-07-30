"""
URDF import/export utilities for robot kinematics.

This module provides tools for loading robot configurations from URDF files
and converting between URDF and DH parameter representations.
"""

import xml.etree.ElementTree as ET
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from ..core.transforms import Transform
from ..core.exceptions import ConfigurationError


class URDFParser:
    """
    Parser for URDF (Unified Robot Description Format) files.
    
    This class provides utilities to extract robot configuration information
    from URDF files and convert them to formats usable by the kinematics library.
    """
    
    def __init__(self, urdf_file: str):
        """
        Initialize URDF parser.
        
        Args:
            urdf_file: Path to URDF file
        """
        self.urdf_file = urdf_file
        self.tree = ET.parse(urdf_file)
        self.root = self.tree.getroot()
        
        # Extract robot name
        self.robot_name = self.root.get('name', 'unknown_robot')
        
        # Parse joints and links
        self.joints = self._parse_joints()
        self.links = self._parse_links()
        
    def _parse_joints(self) -> List[Dict[str, Any]]:
        """Parse joint information from URDF."""
        joints = []
        
        for joint_elem in self.root.findall('joint'):
            joint = {
                'name': joint_elem.get('name'),
                'type': joint_elem.get('type'),
                'parent': joint_elem.find('parent').get('link') if joint_elem.find('parent') is not None else None,
                'child': joint_elem.find('child').get('link') if joint_elem.find('child') is not None else None,
            }
            
            # Parse origin
            origin_elem = joint_elem.find('origin')
            if origin_elem is not None:
                xyz = origin_elem.get('xyz', '0 0 0').split()
                rpy = origin_elem.get('rpy', '0 0 0').split()
                joint['origin'] = {
                    'xyz': [float(x) for x in xyz],
                    'rpy': [float(r) for r in rpy]
                }
            else:
                joint['origin'] = {'xyz': [0, 0, 0], 'rpy': [0, 0, 0]}
            
            # Parse axis
            axis_elem = joint_elem.find('axis')
            if axis_elem is not None:
                axis = axis_elem.get('xyz', '0 0 1').split()
                joint['axis'] = [float(a) for a in axis]
            else:
                joint['axis'] = [0, 0, 1]
            
            # Parse limits
            limit_elem = joint_elem.find('limit')
            if limit_elem is not None:
                joint['limits'] = {
                    'lower': float(limit_elem.get('lower', -np.pi)),
                    'upper': float(limit_elem.get('upper', np.pi)),
                    'effort': float(limit_elem.get('effort', 100.0)),
                    'velocity': float(limit_elem.get('velocity', 1.0))
                }
            else:
                joint['limits'] = {
                    'lower': -np.pi,
                    'upper': np.pi,
                    'effort': 100.0,
                    'velocity': 1.0
                }
            
            joints.append(joint)
        
        return joints
    
    def _parse_links(self) -> List[Dict[str, Any]]:
        """Parse link information from URDF."""
        links = []
        
        for link_elem in self.root.findall('link'):
            link = {
                'name': link_elem.get('name'),
                'visual': None,
                'collision': None,
                'inertial': None
            }
            
            # Parse visual geometry
            visual_elem = link_elem.find('visual')
            if visual_elem is not None:
                link['visual'] = self._parse_geometry(visual_elem)
            
            # Parse collision geometry
            collision_elem = link_elem.find('collision')
            if collision_elem is not None:
                link['collision'] = self._parse_geometry(collision_elem)
            
            # Parse inertial properties
            inertial_elem = link_elem.find('inertial')
            if inertial_elem is not None:
                link['inertial'] = self._parse_inertial(inertial_elem)
            
            links.append(link)
        
        return links
    
    def _parse_geometry(self, elem) -> Dict[str, Any]:
        """Parse geometry information from visual or collision element."""
        geometry = {}
        
        # Parse origin
        origin_elem = elem.find('origin')
        if origin_elem is not None:
            xyz = origin_elem.get('xyz', '0 0 0').split()
            rpy = origin_elem.get('rpy', '0 0 0').split()
            geometry['origin'] = {
                'xyz': [float(x) for x in xyz],
                'rpy': [float(r) for r in rpy]
            }
        else:
            geometry['origin'] = {'xyz': [0, 0, 0], 'rpy': [0, 0, 0]}
        
        # Parse geometry type and parameters
        geom_elem = elem.find('geometry')
        if geom_elem is not None:
            if geom_elem.find('box') is not None:
                box = geom_elem.find('box')
                size = box.get('size', '1 1 1').split()
                geometry['type'] = 'box'
                geometry['size'] = [float(s) for s in size]
            elif geom_elem.find('cylinder') is not None:
                cylinder = geom_elem.find('cylinder')
                geometry['type'] = 'cylinder'
                geometry['radius'] = float(cylinder.get('radius', 0.1))
                geometry['length'] = float(cylinder.get('length', 1.0))
            elif geom_elem.find('sphere') is not None:
                sphere = geom_elem.find('sphere')
                geometry['type'] = 'sphere'
                geometry['radius'] = float(sphere.get('radius', 0.1))
            elif geom_elem.find('mesh') is not None:
                mesh = geom_elem.find('mesh')
                geometry['type'] = 'mesh'
                geometry['filename'] = mesh.get('filename', '')
                scale = mesh.get('scale', '1 1 1').split()
                geometry['scale'] = [float(s) for s in scale]
        
        return geometry
    
    def _parse_inertial(self, elem) -> Dict[str, Any]:
        """Parse inertial properties."""
        inertial = {}
        
        mass_elem = elem.find('mass')
        if mass_elem is not None:
            inertial['mass'] = float(mass_elem.get('value', 1.0))
        
        inertia_elem = elem.find('inertia')
        if inertia_elem is not None:
            inertial['inertia'] = {
                'ixx': float(inertia_elem.get('ixx', 0.0)),
                'ixy': float(inertia_elem.get('ixy', 0.0)),
                'ixz': float(inertia_elem.get('ixz', 0.0)),
                'iyy': float(inertia_elem.get('iyy', 0.0)),
                'iyz': float(inertia_elem.get('iyz', 0.0)),
                'izz': float(inertia_elem.get('izz', 0.0))
            }
        
        return inertial
    
    def extract_dh_parameters(self) -> List[Dict[str, float]]:
        """
        Extract DH parameters from URDF joints.
        
        This is a simplified extraction that assumes standard DH convention.
        For complex robots, manual parameter adjustment may be needed.
        
        Returns:
            List of DH parameters for each joint
        """
        dh_params = []
        
        # Filter for revolute and prismatic joints only
        kinematic_joints = [j for j in self.joints if j['type'] in ['revolute', 'prismatic']]
        
        for joint in kinematic_joints:
            origin = joint['origin']
            axis = joint['axis']
            
            # Simplified DH parameter extraction
            # This is a basic implementation - real extraction requires more complex analysis
            dh_param = {
                'a': 0.0,  # Link length
                'alpha': 0.0,  # Link twist
                'd': origin['xyz'][2] if joint['type'] == 'prismatic' else 0.0,  # Link offset
                'theta': 0.0  # Joint angle
            }
            
            # Estimate alpha from axis orientation
            if abs(axis[0]) > 0.5:
                dh_param['alpha'] = np.pi/2
            elif abs(axis[1]) > 0.5:
                dh_param['alpha'] = np.pi/2
            else:
                dh_param['alpha'] = 0.0
            
            dh_params.append(dh_param)
        
        return dh_params
    
    def to_robot_config(self) -> Dict[str, Any]:
        """
        Convert URDF to robot configuration dictionary.
        
        Returns:
            Robot configuration compatible with the kinematics library
        """
        kinematic_joints = [j for j in self.joints if j['type'] in ['revolute', 'prismatic']]
        
        config = {
            'name': self.robot_name,
            'n_joints': len(kinematic_joints),
            'joint_types': [j['type'] for j in kinematic_joints],
            'joint_limits': [(j['limits']['lower'], j['limits']['upper']) for j in kinematic_joints],
            'dh_parameters': self.extract_dh_parameters(),
            'manufacturer': 'URDF_Import',
            'payload': 5.0,  # Default value
            'reach': 1000.0,  # Default value
        }
        
        return config
    
    def get_joint_names(self) -> List[str]:
        """Get list of joint names."""
        return [j['name'] for j in self.joints if j['type'] in ['revolute', 'prismatic']]
    
    def get_link_names(self) -> List[str]:
        """Get list of link names."""
        return [l['name'] for l in self.links]


def load_robot_from_urdf(urdf_file: str) -> Dict[str, Any]:
    """
    Load robot configuration from URDF file.
    
    Args:
        urdf_file: Path to URDF file
        
    Returns:
        Robot configuration dictionary
    """
    parser = URDFParser(urdf_file)
    return parser.to_robot_config()


def create_urdf_from_config(config: Dict[str, Any], output_file: str) -> None:
    """
    Create URDF file from robot configuration.
    
    Args:
        config: Robot configuration dictionary
        output_file: Output URDF file path
    """
    # This is a basic implementation - real URDF generation would be more complex
    urdf_content = f"""<?xml version="1.0"?>
<robot name="{config.get('name', 'robot')}">
"""
    
    # Add base link
    urdf_content += f"""  <link name="base_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.2"/>
      </geometry>
    </visual>
  </link>
"""
    
    # Add joints and links
    for i in range(config['n_joints']):
        joint_name = f"joint_{i+1}"
        link_name = f"link_{i+1}"
        parent_link = f"link_{i}" if i > 0 else "base_link"
        
        # Add joint
        joint_type = config['joint_types'][i]
        limits = config['joint_limits'][i]
        
        urdf_content += f"""  <joint name="{joint_name}" type="{joint_type}">
    <parent link="{parent_link}"/>
    <child link="{link_name}"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="{limits[0]}" upper="{limits[1]}" effort="100" velocity="1"/>
  </joint>
"""
        
        # Add link
        urdf_content += f"""  <link name="{link_name}">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.3"/>
      </geometry>
    </visual>
  </link>
"""
    
    urdf_content += "</robot>"
    
    with open(output_file, 'w') as f:
        f.write(urdf_content) 