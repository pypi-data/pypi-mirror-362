"""
Custom exceptions for the RobotKinematics library.
"""


class KinematicsError(Exception):
    """Base exception for all kinematics-related errors."""
    pass


class SingularityError(KinematicsError):
    """Raised when a singularity is encountered during calculations."""
    
    def __init__(self, message="Singularity encountered", singularity_type=None, joint_config=None):
        super().__init__(message)
        self.singularity_type = singularity_type
        self.joint_config = joint_config


class JointLimitError(KinematicsError):
    """Raised when joint limits are violated."""
    
    def __init__(self, message="Joint limit violation", joint_idx=None, value=None, limits=None):
        super().__init__(message)
        self.joint_idx = joint_idx
        self.value = value
        self.limits = limits


class ConvergenceError(KinematicsError):
    """Raised when numerical methods fail to converge."""
    
    def __init__(self, message="Failed to converge", max_iterations=None, final_error=None):
        super().__init__(message)
        self.max_iterations = max_iterations
        self.final_error = final_error


class ConfigurationError(KinematicsError):
    """Raised when robot configuration is invalid."""
    
    def __init__(self, message="Invalid configuration", config_type=None, details=None):
        super().__init__(message)
        self.config_type = config_type
        self.details = details


class URDFError(KinematicsError):
    """Raised when there are issues with URDF parsing or loading."""
    
    def __init__(self, message="URDF error", file_path=None, element=None):
        super().__init__(message)
        self.file_path = file_path
        self.element = element


class TransformError(KinematicsError):
    """Raised when transformation operations fail."""
    
    def __init__(self, message="Transform error", transform_type=None, source=None, target=None):
        super().__init__(message)
        self.transform_type = transform_type
        self.source = source
        self.target = target 