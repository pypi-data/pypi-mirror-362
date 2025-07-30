"""
Transformation utilities for robotics kinematics.

This module provides comprehensive tools for handling homogeneous transformations,
rotation representations, and pose interpolation.
"""

import numpy as np
from typing import Union, Tuple, Optional, List
from abc import ABC, abstractmethod
import threading
from .exceptions import TransformError


class Rotation(ABC):
    """Abstract base class for rotation representations."""
    
    @abstractmethod
    def to_rotation_matrix(self) -> np.ndarray:
        """Convert to 3x3 rotation matrix."""
        pass
    
    @abstractmethod
    def to_quaternion(self) -> np.ndarray:
        """Convert to unit quaternion [w, x, y, z]."""
        pass
    
    @abstractmethod
    def to_euler(self, convention: str = 'xyz') -> np.ndarray:
        """Convert to Euler angles."""
        pass
    
    @abstractmethod
    def to_axis_angle(self) -> Tuple[np.ndarray, float]:
        """Convert to axis-angle representation."""
        pass


class RotationMatrix(Rotation):
    """3x3 rotation matrix representation."""
    
    def __init__(self, matrix: np.ndarray):
        if matrix.shape != (3, 3):
            raise TransformError("Rotation matrix must be 3x3")
        if not np.allclose(matrix @ matrix.T, np.eye(3)):
            raise TransformError("Matrix is not a valid rotation matrix")
        self.matrix = matrix.copy()
    
    def to_rotation_matrix(self) -> np.ndarray:
        return self.matrix.copy()
    
    def to_quaternion(self) -> np.ndarray:
        return rotation_matrix_to_quaternion(self.matrix)
    
    def to_euler(self, convention: str = 'xyz') -> np.ndarray:
        return rotation_matrix_to_euler(self.matrix, convention)
    
    def to_axis_angle(self) -> Tuple[np.ndarray, float]:
        return rotation_matrix_to_axis_angle(self.matrix)


class Transform:
    """Homogeneous transformation matrix (4x4)."""
    
    def __init__(self, matrix: Optional[np.ndarray] = None, 
                 position: Optional[np.ndarray] = None,
                 rotation: Optional[Union[np.ndarray, Rotation]] = None):
        """
        Initialize transformation.
        
        Args:
            matrix: 4x4 homogeneous transformation matrix
            position: 3D position vector
            rotation: 3x3 rotation matrix or Rotation object
        """
        if matrix is not None:
            if matrix.shape != (4, 4):
                raise TransformError("Transformation matrix must be 4x4")
            self.matrix = matrix.copy()
        else:
            self.matrix = np.eye(4)
            if position is not None:
                self.matrix[:3, 3] = np.asarray(position).flatten()
            if rotation is not None:
                if isinstance(rotation, Rotation):
                    rot_matrix = rotation.to_rotation_matrix()
                else:
                    rot_matrix = np.asarray(rotation)
                self.matrix[:3, :3] = rot_matrix
    
    @property
    def position(self) -> np.ndarray:
        """Get position vector."""
        return self.matrix[:3, 3].copy()
    
    @property
    def rotation(self) -> np.ndarray:
        """Get rotation matrix."""
        return self.matrix[:3, :3].copy()
    
    def __mul__(self, other: 'Transform') -> 'Transform':
        """Compose transformations."""
        return Transform(self.matrix @ other.matrix)
    
    def __invert__(self) -> 'Transform':
        """Invert transformation."""
        return Transform(np.linalg.inv(self.matrix))
    
    def inverse(self) -> 'Transform':
        """Invert transformation."""
        return ~self
    
    def __str__(self) -> str:
        return f"Transform(\n{self.matrix}\n)"


# Rotation conversion functions
def euler_to_rotation_matrix(euler: np.ndarray, convention: str = 'xyz') -> np.ndarray:
    """
    Convert Euler angles to rotation matrix.
    
    Args:
        euler: Euler angles [rx, ry, rz] in radians
        convention: Euler angle convention ('xyz', 'zyx', etc.)
        
    Returns:
        3x3 rotation matrix
    """
    euler = np.asarray(euler).flatten()
    if len(euler) != 3:
        raise TransformError("Euler angles must have 3 components")
    
    # Pre-computed trigonometric values for efficiency
    cx, cy, cz = np.cos(euler)
    sx, sy, sz = np.sin(euler)
    
    if convention.lower() == 'xyz':
        R = np.array([
            [cy*cz, sx*sy*cz - cx*sz, cx*sy*cz + sx*sz],
            [cy*sz, sx*sy*sz + cx*cz, cx*sy*sz - sx*cz],
            [-sy, sx*cy, cx*cy]
        ])
    elif convention.lower() == 'zyx':
        R = np.array([
            [cy*cz, cy*sz, -sy],
            [sx*sy*cz - cx*sz, sx*sy*sz + cx*cz, sx*cy],
            [cx*sy*cz + sx*sz, cx*sy*sz - sx*cz, cx*cy]
        ])
    else:
        raise TransformError(f"Unsupported Euler convention: {convention}")
    
    return R


def rotation_matrix_to_euler(R: np.ndarray, convention: str = 'xyz') -> np.ndarray:
    """
    Convert rotation matrix to Euler angles.
    
    Args:
        R: 3x3 rotation matrix
        convention: Euler angle convention
        
    Returns:
        Euler angles [rx, ry, rz] in radians
    """
    if convention.lower() == 'xyz':
        sy = -R[2, 0]
        if abs(sy) < 1e-6:  # Near singularity
            rx = np.arctan2(R[2, 1], R[2, 2])
            ry = 0
            rz = np.arctan2(R[1, 0], R[0, 0])
        else:
            rx = np.arctan2(R[2, 1], R[2, 2])
            ry = np.arcsin(sy)
            rz = np.arctan2(R[1, 0], R[0, 0])
    elif convention.lower() == 'zyx':
        sy = R[0, 2]
        if abs(sy) < 1e-6:  # Near singularity
            rx = np.arctan2(-R[1, 2], R[2, 2])
            ry = 0
            rz = np.arctan2(-R[0, 1], R[0, 0])
        else:
            rx = np.arctan2(-R[1, 2], R[2, 2])
            ry = np.arcsin(sy)
            rz = np.arctan2(-R[0, 1], R[0, 0])
    else:
        raise TransformError(f"Unsupported Euler convention: {convention}")
    
    return np.array([rx, ry, rz])


def quaternion_to_rotation_matrix(q: np.ndarray) -> np.ndarray:
    """
    Convert unit quaternion to rotation matrix.
    
    Args:
        q: Unit quaternion [w, x, y, z]
        
    Returns:
        3x3 rotation matrix
    """
    q = np.asarray(q).flatten()
    if len(q) != 4:
        raise TransformError("Quaternion must have 4 components")
    
    # Normalize quaternion
    q = q / np.linalg.norm(q)
    w, x, y, z = q
    
    R = np.array([
        [1 - 2*y*y - 2*z*z, 2*(x*y - w*z), 2*(x*z + w*y)],
        [2*(x*y + w*z), 1 - 2*x*x - 2*z*z, 2*(y*z - w*x)],
        [2*(x*z - w*y), 2*(y*z + w*x), 1 - 2*x*x - 2*y*y]
    ])
    
    return R


def rotation_matrix_to_quaternion(R: np.ndarray) -> np.ndarray:
    """
    Convert rotation matrix to unit quaternion.
    
    Args:
        R: 3x3 rotation matrix
        
    Returns:
        Unit quaternion [w, x, y, z]
    """
    trace = np.trace(R)
    
    if trace > 0:
        S = np.sqrt(trace + 1.0) * 2
        w = 0.25 * S
        x = (R[2, 1] - R[1, 2]) / S
        y = (R[0, 2] - R[2, 0]) / S
        z = (R[1, 0] - R[0, 1]) / S
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        S = np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2
        w = (R[2, 1] - R[1, 2]) / S
        x = 0.25 * S
        y = (R[0, 1] + R[1, 0]) / S
        z = (R[0, 2] + R[2, 0]) / S
    elif R[1, 1] > R[2, 2]:
        S = np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2
        w = (R[0, 2] - R[2, 0]) / S
        x = (R[0, 1] + R[1, 0]) / S
        y = 0.25 * S
        z = (R[1, 2] + R[2, 1]) / S
    else:
        S = np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2
        w = (R[1, 0] - R[0, 1]) / S
        x = (R[0, 2] + R[2, 0]) / S
        y = (R[1, 2] + R[2, 1]) / S
        z = 0.25 * S
    
    return np.array([w, x, y, z])


def axis_angle_to_rotation_matrix(axis: np.ndarray, angle: float) -> np.ndarray:
    """
    Convert axis-angle representation to rotation matrix.
    
    Args:
        axis: Unit axis vector
        angle: Rotation angle in radians
        
    Returns:
        3x3 rotation matrix
    """
    axis = np.asarray(axis).flatten()
    axis = axis / np.linalg.norm(axis)
    
    c = np.cos(angle)
    s = np.sin(angle)
    x, y, z = axis
    
    R = np.array([
        [c + x*x*(1-c), x*y*(1-c) - z*s, x*z*(1-c) + y*s],
        [y*x*(1-c) + z*s, c + y*y*(1-c), y*z*(1-c) - x*s],
        [z*x*(1-c) - y*s, z*y*(1-c) + x*s, c + z*z*(1-c)]
    ])
    
    return R


def rotation_matrix_to_axis_angle(R: np.ndarray) -> Tuple[np.ndarray, float]:
    """
    Convert rotation matrix to axis-angle representation.
    
    Args:
        R: 3x3 rotation matrix
        
    Returns:
        Tuple of (axis, angle)
    """
    trace = np.trace(R)
    angle = np.arccos(np.clip((trace - 1) / 2, -1, 1))
    
    if abs(angle) < 1e-6:
        return np.array([0, 0, 1]), 0
    
    axis = np.array([
        R[2, 1] - R[1, 2],
        R[0, 2] - R[2, 0],
        R[1, 0] - R[0, 1]
    ])
    axis = axis / (2 * np.sin(angle))
    
    return axis, angle


def pose_interpolation(pose1: Transform, pose2: Transform, t: float) -> Transform:
    """
    Interpolate between two poses.
    
    Args:
        pose1: First pose
        pose2: Second pose
        t: Interpolation parameter [0, 1]
        
    Returns:
        Interpolated pose
    """
    t = np.clip(t, 0, 1)
    
    # Linear interpolation for position
    pos = (1 - t) * pose1.position + t * pose2.position
    
    # Spherical linear interpolation (SLERP) for rotation
    q1 = rotation_matrix_to_quaternion(pose1.rotation)
    q2 = rotation_matrix_to_quaternion(pose2.rotation)
    
    # Ensure shortest path
    if np.dot(q1, q2) < 0:
        q2 = -q2
    
    # SLERP
    if abs(np.dot(q1, q2)) > 0.9995:
        # Quaternions are very close, use linear interpolation
        q_interp = (1 - t) * q1 + t * q2
    else:
        theta = np.arccos(np.clip(np.dot(q1, q2), -1, 1))
        q_interp = (np.sin((1 - t) * theta) * q1 + np.sin(t * theta) * q2) / np.sin(theta)
    
    q_interp = q_interp / np.linalg.norm(q_interp)
    rot_interp = quaternion_to_rotation_matrix(q_interp)
    
    return Transform(position=pos, rotation=rot_interp)


# Thread-safe transformation cache
class TransformCache:
    """Thread-safe cache for pre-computed transformations."""
    
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Transform]:
        """Get cached transformation."""
        with self.lock:
            return self.cache.get(key)
    
    def set(self, key: str, transform: Transform):
        """Set cached transformation."""
        with self.lock:
            if len(self.cache) >= self.max_size:
                # Remove oldest entry (simple FIFO)
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
            self.cache[key] = transform
    
    def clear(self):
        """Clear cache."""
        with self.lock:
            self.cache.clear()


# Global transformation cache
_transform_cache = TransformCache() 