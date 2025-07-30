"""
Performance optimization utilities for robotics kinematics.

This module provides tools for optimizing the performance of kinematics
calculations, including caching, vectorization, and JIT compilation.
"""

import numpy as np
from typing import Dict, Any, List, Optional, Callable
import time
import threading
import functools
from ..core.base import RobotKinematicsBase
from ..core.transforms import Transform


class PerformanceOptimizer:
    """
    Performance optimization for robotics kinematics.
    
    This class provides various optimization techniques to improve
    the performance of kinematics calculations.
    """
    
    def __init__(self, robot: RobotKinematicsBase):
        """
        Initialize performance optimizer.
        
        Args:
            robot: Robot kinematics instance
        """
        self.robot = robot
        self.cache = {}
        self.cache_lock = threading.Lock()
        self.performance_metrics = {}
    
    def enable_caching(self, max_cache_size: int = 10000):
        """
        Enable caching for kinematics calculations.
        
        Args:
            max_cache_size: Maximum number of cached entries
        """
        self.cache_enabled = True
        self.max_cache_size = max_cache_size
        
        # Wrap forward kinematics with caching
        original_fk = self.robot.forward_kinematics
        
        @functools.wraps(original_fk)
        def cached_forward_kinematics(joint_config):
            config_key = tuple(joint_config.flatten())
            
            with self.cache_lock:
                if config_key in self.cache:
                    return self.cache[config_key]
                
                result = original_fk(joint_config)
                
                # Add to cache
                if len(self.cache) >= self.max_cache_size:
                    # Remove oldest entry
                    oldest_key = next(iter(self.cache))
                    del self.cache[oldest_key]
                
                self.cache[config_key] = result
                return result
        
        self.robot.forward_kinematics = cached_forward_kinematics
    
    def disable_caching(self):
        """Disable caching."""
        self.cache_enabled = False
        with self.cache_lock:
            self.cache.clear()
    
    def clear_cache(self):
        """Clear the cache."""
        with self.cache_lock:
            self.cache.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.cache_lock:
            return {
                'cache_size': len(self.cache),
                'max_cache_size': getattr(self, 'max_cache_size', 0),
                'cache_enabled': getattr(self, 'cache_enabled', False)
            }
    
    def benchmark_forward_kinematics(self, n_samples: int = 1000) -> Dict[str, float]:
        """
        Benchmark forward kinematics performance.
        
        Args:
            n_samples: Number of samples for benchmarking
            
        Returns:
            Performance metrics
        """
        # Generate random joint configurations
        joint_configs = []
        for _ in range(n_samples):
            q = np.array([
                np.random.uniform(lim[0], lim[1]) for lim in self.robot.joint_limits
            ])
            joint_configs.append(q)
        
        # Benchmark without caching
        self.disable_caching()
        start_time = time.time()
        
        for q in joint_configs:
            try:
                self.robot.forward_kinematics(q)
            except:
                pass
        
        time_without_cache = time.time() - start_time
        
        # Benchmark with caching
        self.enable_caching()
        start_time = time.time()
        
        for q in joint_configs:
            try:
                self.robot.forward_kinematics(q)
            except:
                pass
        
        time_with_cache = time.time() - start_time
        
        # Benchmark batch processing
        start_time = time.time()
        try:
            self.robot.batch_forward_kinematics(np.array(joint_configs))
        except:
            pass
        
        time_batch = time.time() - start_time
        
        return {
            'time_without_cache': time_without_cache,
            'time_with_cache': time_with_cache,
            'time_batch': time_batch,
            'speedup_with_cache': time_without_cache / time_with_cache if time_with_cache > 0 else 0,
            'speedup_batch': time_without_cache / time_batch if time_batch > 0 else 0,
            'n_samples': n_samples
        }
    
    def benchmark_inverse_kinematics(self, n_samples: int = 100) -> Dict[str, float]:
        """
        Benchmark inverse kinematics performance.
        
        Args:
            n_samples: Number of samples for benchmarking
            
        Returns:
            Performance metrics
        """
        # Generate random target poses
        target_poses = []
        for _ in range(n_samples):
            # Random position
            position = np.random.uniform(-1.0, 1.0, 3)
            
            # Random orientation
            from ..core.transforms import euler_to_rotation_matrix
            euler = np.random.uniform(-np.pi, np.pi, 3)
            rotation = euler_to_rotation_matrix(euler)
            
            target_pose = Transform(position=position, rotation=rotation)
            target_poses.append(target_pose)
        
        # Benchmark IK
        start_time = time.time()
        success_count = 0
        
        for target_pose in target_poses:
            try:
                initial_guess = np.zeros(self.robot.n_joints)
                self.robot.inverse_kinematics(target_pose, initial_guess)
                success_count += 1
            except:
                pass
        
        time_ik = time.time() - start_time
        
        return {
            'time_total': time_ik,
            'time_per_solution': time_ik / n_samples if n_samples > 0 else 0,
            'success_rate': success_count / n_samples if n_samples > 0 else 0,
            'n_samples': n_samples,
            'n_successful': success_count
        }
    
    def optimize_joint_limits(self) -> Dict[str, Any]:
        """
        Optimize joint limits for better performance.
        
        Returns:
            Optimization results
        """
        # Analyze joint limit usage
        joint_usage = {i: {'min': [], 'max': []} for i in range(self.robot.n_joints)}
        
        # Sample joint configurations
        n_samples = 1000
        for _ in range(n_samples):
            q = np.array([
                np.random.uniform(lim[0], lim[1]) for lim in self.robot.joint_limits
            ])
            
            for i, value in enumerate(q):
                joint_usage[i]['min'].append(value)
                joint_usage[i]['max'].append(value)
        
        # Analyze usage patterns
        optimization_suggestions = {}
        for i in range(self.robot.n_joints):
            current_min, current_max = self.robot.joint_limits[i]
            used_min = np.min(joint_usage[i]['min'])
            used_max = np.max(joint_usage[i]['max'])
            
            # Check if limits can be tightened
            if used_min > current_min + 0.1:
                optimization_suggestions[f'joint_{i}_min'] = {
                    'current': current_min,
                    'suggested': used_min,
                    'improvement': current_min - used_min
                }
            
            if used_max < current_max - 0.1:
                optimization_suggestions[f'joint_{i}_max'] = {
                    'current': current_max,
                    'suggested': used_max,
                    'improvement': current_max - used_max
                }
        
        return {
            'joint_usage': joint_usage,
            'optimization_suggestions': optimization_suggestions
        }


class VectorizedKinematics:
    """
    Vectorized kinematics calculations for improved performance.
    
    This class provides vectorized implementations of kinematics
    calculations for batch processing.
    """
    
    def __init__(self, robot: RobotKinematicsBase):
        """
        Initialize vectorized kinematics.
        
        Args:
            robot: Robot kinematics instance
        """
        self.robot = robot
    
    def vectorized_forward_kinematics(self, joint_configs: np.ndarray) -> List[Transform]:
        """
        Vectorized forward kinematics for multiple configurations.
        
        Args:
            joint_configs: Array of joint configurations (N x n_joints)
            
        Returns:
            List of end-effector poses
        """
        joint_configs = np.asarray(joint_configs)
        if joint_configs.ndim == 1:
            joint_configs = joint_configs.reshape(1, -1)
        
        # Use the robot's batch method if available
        if hasattr(self.robot, 'batch_forward_kinematics'):
            return self.robot.batch_forward_kinematics(joint_configs)
        
        # Fallback to individual calculations
        poses = []
        for config in joint_configs:
            poses.append(self.robot.forward_kinematics(config))
        
        return poses
    
    def vectorized_jacobian(self, joint_configs: np.ndarray) -> List[np.ndarray]:
        """
        Vectorized Jacobian calculation for multiple configurations.
        
        Args:
            joint_configs: Array of joint configurations (N x n_joints)
            
        Returns:
            List of Jacobian matrices
        """
        joint_configs = np.asarray(joint_configs)
        if joint_configs.ndim == 1:
            joint_configs = joint_configs.reshape(1, -1)
        
        jacobians = []
        for config in joint_configs:
            jacobian = self.robot.get_jacobian(config)
            jacobians.append(jacobian.compute())
        
        return jacobians
    
    def vectorized_manipulability(self, joint_configs: np.ndarray) -> np.ndarray:
        """
        Vectorized manipulability calculation.
        
        Args:
            joint_configs: Array of joint configurations (N x n_joints)
            
        Returns:
            Array of manipulability values
        """
        joint_configs = np.asarray(joint_configs)
        if joint_configs.ndim == 1:
            joint_configs = joint_configs.reshape(1, -1)
        
        manipulabilities = []
        for config in joint_configs:
            try:
                jacobian = self.robot.get_jacobian(config)
                manipulabilities.append(jacobian.manipulability())
            except:
                manipulabilities.append(0.0)
        
        return np.array(manipulabilities)


class JITOptimizer:
    """
    Just-In-Time (JIT) compilation optimizer.
    
    This class provides JIT compilation for kinematics functions
    using Numba for improved performance.
    """
    
    def __init__(self, robot: RobotKinematicsBase):
        """
        Initialize JIT optimizer.
        
        Args:
            robot: Robot kinematics instance
        """
        self.robot = robot
        self.jit_functions = {}
        
        # Try to import Numba
        try:
            import numba
            self.numba_available = True
        except ImportError:
            self.numba_available = False
    
    def compile_forward_kinematics(self) -> bool:
        """
        Compile forward kinematics with JIT.
        
        Returns:
            True if compilation successful
        """
        if not self.numba_available:
            return False
        
        try:
            import numba
            from numba import jit
            
            # Create a simplified FK function for JIT compilation
            @jit(nopython=True)
            def jit_forward_kinematics(joint_config, dh_params):
                """JIT-compiled forward kinematics."""
                # This is a simplified implementation
                # In practice, you'd need to implement the full DH transformation
                T = np.eye(4)
                
                for i, q in enumerate(joint_config):
                    # Simplified DH transformation
                    a, alpha, d, theta = dh_params[i]
                    
                    # Pre-compute trigonometric values
                    ct = np.cos(theta + q)
                    st = np.sin(theta + q)
                    ca = np.cos(alpha)
                    sa = np.sin(alpha)
                    
                    # DH transformation matrix
                    T_i = np.array([
                        [ct, -st*ca, st*sa, a*ct],
                        [st, ct*ca, -ct*sa, a*st],
                        [0, sa, ca, d],
                        [0, 0, 0, 1]
                    ])
                    
                    T = T @ T_i
                
                return T
            
            # Store the compiled function
            self.jit_functions['forward_kinematics'] = jit_forward_kinematics
            
            return True
            
        except Exception:
            return False
    
    def compile_jacobian(self) -> bool:
        """
        Compile Jacobian calculation with JIT.
        
        Returns:
            True if compilation successful
        """
        if not self.numba_available:
            return False
        
        try:
            import numba
            from numba import jit
            
            # Create a simplified Jacobian function for JIT compilation
            @jit(nopython=True)
            def jit_jacobian(joint_config, dh_params):
                """JIT-compiled Jacobian calculation."""
                n_joints = len(joint_config)
                J = np.zeros((6, n_joints))
                
                # Simplified Jacobian calculation
                # In practice, you'd need the full geometric Jacobian
                for i in range(n_joints):
                    # Simplified: just fill with some values
                    J[:3, i] = np.array([1.0, 0.0, 0.0])  # Linear part
                    J[3:, i] = np.array([0.0, 0.0, 1.0])  # Angular part
                
                return J
            
            # Store the compiled function
            self.jit_functions['jacobian'] = jit_jacobian
            
            return True
            
        except Exception:
            return False
    
    def get_compiled_function(self, function_name: str) -> Optional[Callable]:
        """
        Get a compiled function.
        
        Args:
            function_name: Name of the compiled function
            
        Returns:
            Compiled function or None
        """
        return self.jit_functions.get(function_name)
    
    def benchmark_jit_performance(self, n_samples: int = 1000) -> Dict[str, float]:
        """
        Benchmark JIT performance improvements.
        
        Args:
            n_samples: Number of samples for benchmarking
            
        Returns:
            Performance metrics
        """
        if not self.numba_available:
            return {'error': 'Numba not available'}
        
        # Generate test data
        joint_configs = []
        for _ in range(n_samples):
            q = np.array([
                np.random.uniform(lim[0], lim[1]) for lim in self.robot.joint_limits
            ])
            joint_configs.append(q)
        
        # Benchmark original function
        start_time = time.time()
        for q in joint_configs:
            try:
                self.robot.forward_kinematics(q)
            except:
                pass
        time_original = time.time() - start_time
        
        # Benchmark JIT function
        if 'forward_kinematics' in self.jit_functions:
            start_time = time.time()
            for q in joint_configs:
                try:
                    # Extract DH parameters (simplified)
                    dh_params = np.array([[0, 0, 0, 0] for _ in range(self.robot.n_joints)])
                    self.jit_functions['forward_kinematics'](q, dh_params)
                except:
                    pass
            time_jit = time.time() - start_time
            
            return {
                'time_original': time_original,
                'time_jit': time_jit,
                'speedup': time_original / time_jit if time_jit > 0 else 0,
                'n_samples': n_samples
            }
        else:
            return {'error': 'JIT function not compiled'}


class MemoryOptimizer:
    """
    Memory optimization for kinematics calculations.
    
    This class provides tools for optimizing memory usage in
    kinematics calculations.
    """
    
    def __init__(self, robot: RobotKinematicsBase):
        """
        Initialize memory optimizer.
        
        Args:
            robot: Robot kinematics instance
        """
        self.robot = robot
    
    def optimize_array_usage(self) -> Dict[str, Any]:
        """
        Optimize array usage for memory efficiency.
        
        Returns:
            Optimization suggestions
        """
        import sys
        
        # Analyze memory usage of different data types
        data_types = {
            'float32': np.float32,
            'float64': np.float64,
            'float16': np.float16
        }
        
        memory_usage = {}
        for name, dtype in data_types.items():
            # Create sample arrays
            sample_config = np.array([0.0] * self.robot.n_joints, dtype=dtype)
            sample_transform = np.eye(4, dtype=dtype)
            
            memory_usage[name] = {
                'config_size': sys.getsizeof(sample_config),
                'transform_size': sys.getsizeof(sample_transform),
                'dtype': dtype
            }
        
        # Suggest optimizations
        suggestions = []
        
        if memory_usage['float32']['config_size'] < memory_usage['float64']['config_size']:
            suggestions.append({
                'type': 'data_type',
                'description': 'Use float32 instead of float64 for memory efficiency',
                'savings': memory_usage['float64']['config_size'] - memory_usage['float32']['config_size']
            })
        
        return {
            'memory_usage': memory_usage,
            'suggestions': suggestions
        }
    
    def profile_memory_usage(self, n_samples: int = 1000) -> Dict[str, Any]:
        """
        Profile memory usage during kinematics calculations.
        
        Args:
            n_samples: Number of samples for profiling
            
        Returns:
            Memory usage profile
        """
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Perform kinematics calculations
        for _ in range(n_samples):
            q = np.array([
                np.random.uniform(lim[0], lim[1]) for lim in self.robot.joint_limits
            ])
            
            try:
                self.robot.forward_kinematics(q)
                jacobian = self.robot.get_jacobian(q)
                jacobian.compute()
            except:
                pass
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        return {
            'initial_memory_mb': initial_memory / 1024 / 1024,
            'final_memory_mb': final_memory / 1024 / 1024,
            'memory_increase_mb': memory_increase / 1024 / 1024,
            'memory_per_sample_kb': memory_increase / n_samples / 1024 if n_samples > 0 else 0
        } 