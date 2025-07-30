# Robot Kinematics Library - API Reference

## Overview

The Robot Kinematics Library provides comprehensive tools for forward and inverse kinematics, Jacobian analysis, workspace analysis, and singularity detection for various types of robotic manipulators.

## Core Modules

### Core Base Classes

#### `RobotKinematicsBase`

Base class for all robot kinematics implementations.

```python
from robot_kinematics.core.base import RobotKinematicsBase

class RobotKinematicsBase:
    def __init__(self, config: Dict[str, Any])
    def forward_kinematics(self, joint_config: np.ndarray) -> Transform
    def inverse_kinematics(self, target_pose: Transform, initial_guess: Optional[np.ndarray] = None) -> np.ndarray
    def get_jacobian(self, joint_config: np.ndarray) -> Jacobian
    def get_joint_limits(self) -> List[Tuple[float, float]]
```

**Parameters:**
- `config`: Robot configuration dictionary containing joint limits, DH parameters, etc.

**Methods:**
- `forward_kinematics()`: Compute forward kinematics for given joint configuration
- `inverse_kinematics()`: Compute inverse kinematics for target pose
- `get_jacobian()`: Get Jacobian matrix for given joint configuration
- `get_joint_limits()`: Get joint limits for the robot

#### `Transform`

Represents 3D transformations (position and orientation).

```python
from robot_kinematics.core.transforms import Transform

class Transform:
    def __init__(self, position: np.ndarray, rotation: Optional[np.ndarray] = None)
    def compose(self, other: Transform) -> Transform
    def inverse(self) -> Transform
    def to_matrix(self) -> np.ndarray
    def from_matrix(self, matrix: np.ndarray) -> Transform
```

**Parameters:**
- `position`: 3D position vector [x, y, z]
- `rotation`: 3x3 rotation matrix or quaternion (optional)

#### `Jacobian`

Jacobian matrix computation and analysis.

```python
from robot_kinematics.core.jacobian import Jacobian

class Jacobian:
    def __init__(self, matrix: np.ndarray)
    def compute(self) -> np.ndarray
    def pseudo_inverse(self, damping: float = 0.0) -> np.ndarray
    def condition_number(self) -> float
    def manipulability(self) -> float
    def distance_to_singularity(self) -> float
```

## Forward Kinematics

### DH Kinematics

#### `DHKinematics`

Denavit-Hartenberg parameter-based forward kinematics.

```python
from robot_kinematics.forward.dh_kinematics import DHKinematics

class DHKinematics:
    def __init__(self, config: Dict[str, Any])
    def forward_kinematics(self, joint_config: np.ndarray) -> Transform
    def get_joint_transform(self, joint_idx: int, joint_config: np.ndarray) -> Transform
    def inverse_kinematics(self, target_pose: Transform, initial_guess: Optional[np.ndarray] = None) -> np.ndarray
```

**Configuration:**
```python
config = {
    'n_joints': 6,
    'joint_types': ['revolute'] * 6,
    'dh_parameters': [
        {'a': 0, 'alpha': np.pi/2, 'd': 0.089159, 'theta': 0},
        # ... more DH parameters
    ],
    'joint_limits': [
        (-2*np.pi, 2*np.pi), (-2*np.pi, 2*np.pi), # ... joint limits
    ]
}
```

### URDF Kinematics

#### `URDFKinematics`

URDF-based forward kinematics.

```python
from robot_kinematics.forward.urdf_kinematics import URDFKinematics

class URDFKinematics:
    def __init__(self, urdf_file: str)
    def forward_kinematics(self, joint_config: np.ndarray) -> Transform
    def get_joint_transform(self, joint_name: str, joint_config: np.ndarray) -> Transform
```

## Inverse Kinematics

### Numerical IK

#### `NumericalIK`

Numerical inverse kinematics solvers.

```python
from robot_kinematics.inverse.numerical import NumericalIK

class NumericalIK:
    def __init__(self, robot: RobotKinematicsBase, method: str = "damped_least_squares")
    def solve(self, target_pose: Transform, initial_guess: np.ndarray, **kwargs) -> Tuple[np.ndarray, bool, float]
```

**Methods:**
- `"damped_least_squares"`: Damped least squares method
- `"levenberg_marquardt"`: Levenberg-Marquardt algorithm
- `"gradient_descent"`: Gradient descent optimization

**Returns:**
- `solution`: Joint configuration solution
- `success`: Whether solution was found
- `error`: Final error value

### Analytical IK

#### `AnalyticalIK`

Analytical inverse kinematics for specific robot types.

```python
from robot_kinematics.inverse.analytical import AnalyticalIK

class AnalyticalIK:
    def __init__(self, robot: RobotKinematicsBase)
    def solve(self, target_pose: Transform) -> List[np.ndarray]
```

### Hybrid IK

#### `HybridIK`

Combines analytical and numerical methods.

```python
from robot_kinematics.inverse.hybrid import HybridIK

class HybridIK:
    def __init__(self, robot: RobotKinematicsBase)
    def solve(self, target_pose: Transform, initial_guess: np.ndarray) -> Tuple[np.ndarray, bool, float]
```

## Robot Implementations

### Serial Manipulators

#### `UR5Manipulator`

Universal Robots UR5 implementation.

```python
from robot_kinematics.robots.serial import UR5Manipulator

robot = UR5Manipulator()
# or with custom config
robot = UR5Manipulator(config={'payload': 10.0})
```

#### `PandaManipulator`

Franka Emika Panda implementation.

```python
from robot_kinematics.robots.serial import PandaManipulator

robot = PandaManipulator()
```

#### `SCARAManipulator`

SCARA robot implementation.

```python
from robot_kinematics.robots.serial import SCARAManipulator

robot = SCARAManipulator()
```

#### `KUKAKR5Manipulator`

KUKA KR5 sixx 850 industrial robot implementation.

```python
from robot_kinematics.robots.serial import KUKAKR5Manipulator

robot = KUKAKR5Manipulator()
# or with custom config
robot = KUKAKR5Manipulator(config={'payload': 7.0})
```

### Parallel Robots

#### `StewartPlatform`

Stewart platform parallel robot.

```python
from robot_kinematics.robots.parallel import StewartPlatform

config = {
    'base_radius': 0.2,
    'platform_radius': 0.1,
    'leg_length': 0.3,
    'n_legs': 6
}
stewart = StewartPlatform(config)
```

### Mobile Robots

#### `MobileManipulator`

Mobile manipulator with base and arm.

```python
from robot_kinematics.robots.mobile import MobileManipulator

config = {
    'base_type': 'differential_drive',
    'manipulator': UR5Manipulator(),
    'base_dimensions': [0.5, 0.3, 0.2]
}
mobile_robot = MobileManipulator(config)
```

## Utility Modules

### Workspace Analysis

#### `WorkspaceAnalyzer`

Workspace analysis and visualization.

```python
from robot_kinematics.utils.workspace import WorkspaceAnalyzer

analyzer = WorkspaceAnalyzer(robot)

# Analyze reachable workspace
reachable_data = analyzer.analyze_reachable_workspace(n_samples=10000)

# Analyze dexterous workspace
dexterous_data = analyzer.analyze_dexterous_workspace(n_samples=5000)

# Generate comprehensive report
report = analyzer.generate_workspace_report(n_samples=10000)

# Visualize workspace
analyzer.visualize_workspace(
    positions=reachable_data['positions'],
    dexterous_positions=dexterous_data['dexterous_positions'],
    save_path='workspace.png'
)
```

### Singularity Analysis

#### `SingularityAnalyzer`

Singularity detection and analysis.

```python
from robot_kinematics.utils.singularity import SingularityAnalyzer

analyzer = SingularityAnalyzer(robot)

# Detect singularities in a configuration
analysis = analyzer.detect_singularities(joint_config, threshold=1e-6)

# Analyze singularity manifold
manifold_data = analyzer.analyze_singularity_manifold(n_samples=1000)

# Find singularity-free path
path = analyzer.find_singularity_free_path(start_config, end_config)

# Compute singularity avoidance velocity
velocity = analyzer.compute_singularity_avoidance_velocity(
    joint_config, desired_velocity, damping=0.1
)
```

### Performance Optimization

#### `PerformanceOptimizer`

Performance optimization for robot configurations.

```python
from robot_kinematics.utils.performance import PerformanceOptimizer

optimizer = PerformanceOptimizer(robot)

# Optimize joint configuration
optimized_config, metrics = optimizer.optimize_joint_configuration(
    target_pose, initial_guess, objective='maximize_manipulability'
)

# Optimize trajectory
optimized_trajectory = optimizer.optimize_trajectory(
    waypoints, objective='minimize_joint_velocities'
)
```

## Error Handling

### Exceptions

```python
from robot_kinematics.core.exceptions import (
    KinematicsError,
    SingularityError,
    ConvergenceError,
    ConfigurationError
)

try:
    solution = robot.inverse_kinematics(target_pose)
except KinematicsError as e:
    print(f"Kinematics error: {e}")
except SingularityError as e:
    print(f"Singularity detected: {e}")
except ConvergenceError as e:
    print(f"Convergence failed: {e}")
```

## Configuration Examples

### UR5 Configuration

```python
ur5_config = {
    'n_joints': 6,
    'joint_types': ['revolute'] * 6,
    'joint_limits': [
        (-2*np.pi, 2*np.pi), (-2*np.pi, 2*np.pi), (-2*np.pi, 2*np.pi),
        (-2*np.pi, 2*np.pi), (-2*np.pi, 2*np.pi), (-2*np.pi, 2*np.pi)
    ],
    'dh_parameters': [
        {'a': 0, 'alpha': np.pi/2, 'd': 0.089159, 'theta': 0},
        {'a': -0.425, 'alpha': 0, 'd': 0, 'theta': 0},
        {'a': -0.39225, 'alpha': 0, 'd': 0, 'theta': 0},
        {'a': 0, 'alpha': np.pi/2, 'd': 0.10915, 'theta': 0},
        {'a': 0, 'alpha': -np.pi/2, 'd': 0.09465, 'theta': 0},
        {'a': 0, 'alpha': 0, 'd': 0.0823, 'theta': 0}
    ],
    'name': 'UR5',
    'manufacturer': 'Universal Robots',
    'payload': 5.0,
    'reach': 850.0
}
```

### Stewart Platform Configuration

```python
stewart_config = {
    'base_radius': 0.2,
    'platform_radius': 0.1,
    'leg_length': 0.3,
    'n_legs': 6,
    'leg_angles': [0, 60, 120, 180, 240, 300],  # degrees
    'name': 'Stewart Platform',
    'workspace_type': 'parallel'
}
```

## Best Practices

1. **Always check return values** from IK solvers for success/failure
2. **Use appropriate initial guesses** for numerical IK methods
3. **Handle singularities** in trajectory planning
4. **Validate joint limits** before using solutions
5. **Use workspace analysis** to understand robot capabilities
6. **Optimize for performance** when real-time operation is required

## Performance Tips

1. **Pre-compute Jacobians** for frequently used configurations
2. **Use analytical IK** when available for better performance
3. **Cache workspace analysis** results for repeated use
4. **Choose appropriate IK method** based on requirements (speed vs accuracy)
5. **Use vectorized operations** for batch processing 

## Integration Modules

### URDF Integration

#### `URDFParser`

Parse and extract robot configuration from URDF files.

```python
from robot_kinematics.integration.urdf_utils import URDFParser

parser = URDFParser("robot.urdf")
config = parser.to_robot_config()
joint_names = parser.get_joint_names()
link_names = parser.get_link_names()
```

#### `load_robot_from_urdf`

Load robot configuration from URDF file.

```python
from robot_kinematics.integration.urdf_utils import load_robot_from_urdf

config = load_robot_from_urdf("robot.urdf")
robot = SerialManipulator(config)
```

#### `create_urdf_from_config`

Create URDF file from robot configuration.

```python
from robot_kinematics.integration.urdf_utils import create_urdf_from_config

create_urdf_from_config(robot_config, "output.urdf")
```

### PyBullet Integration

#### `connect_gui`

Connect to PyBullet GUI for visualization.

```python
from robot_kinematics.integration.pybullet_utils import connect_gui

connect_gui()
```

#### `create_kuka_kr5_pybullet`

Load KUKA KR5 model in PyBullet.

```python
from robot_kinematics.integration.pybullet_utils import create_kuka_kr5_pybullet

robot_id = create_kuka_kr5_pybullet()
```

#### `animate_trajectory`

Animate joint trajectory in PyBullet.

```python
from robot_kinematics.integration.pybullet_utils import animate_trajectory

animate_trajectory(robot_id, joint_trajectory, dt=0.05)
``` 