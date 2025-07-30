# Robot Kinematics Library - Quick Start Guide

## Installation

### From PyPI (Recommended)

```bash
pip install robot-kinematics
```

### From Source

```bash
git clone <repository-url>
cd robot-kinematics
pip install -e .
```

## Basic Usage

### 1. Create a Robot

```python
import numpy as np
from robot_kinematics.robots.serial import UR5Manipulator
from robot_kinematics.core.transforms import Transform

# Create a UR5 robot
robot = UR5Manipulator()

print(f"Robot: {robot.name}")
print(f"Number of joints: {robot.n_joints}")
print(f"Joint limits: {robot.get_joint_limits()}")
```

### 2. Forward Kinematics

```python
# Define joint configuration (home position)
joint_config = np.array([0, 0, 0, 0, 0, 0])

# Compute forward kinematics
pose = robot.forward_kinematics(joint_config)

print(f"End-effector position: {pose.position}")
print(f"End-effector orientation: {pose.rotation}")
```

### 3. Inverse Kinematics

```python
from robot_kinematics.inverse.numerical import NumericalIK

# Create IK solver
ik_solver = NumericalIK(robot=robot, method="damped_least_squares")

# Define target pose
target_pose = Transform(position=np.array([0.4, 0.0, 0.5]))

# Initial guess
initial_guess = np.array([0, 0, 0, 0, 0, 0])

# Solve IK
solution, success, error = ik_solver.solve(target_pose, initial_guess)

if success:
    print(f"Solution found: {solution}")
    print(f"Error: {error}")
else:
    print("No solution found")
```

### 4. Jacobian Analysis

```python
# Get Jacobian matrix
jacobian = robot.get_jacobian(joint_config)

# Analyze Jacobian properties
condition_number = jacobian.condition_number()
manipulability = jacobian.manipulability()
distance_to_singularity = jacobian.distance_to_singularity()

print(f"Condition number: {condition_number}")
print(f"Manipulability: {manipulability}")
print(f"Distance to singularity: {distance_to_singularity}")
```

## Advanced Features

### Workspace Analysis

```python
from robot_kinematics.utils.workspace import WorkspaceAnalyzer

# Create workspace analyzer
analyzer = WorkspaceAnalyzer(robot)

# Generate workspace report
report = analyzer.generate_workspace_report(n_samples=5000)

print(f"Workspace analysis completed:")
print(f"Reachable workspace volume: {report['summary'].get('reachable_volume', 'N/A')}")
print(f"Dexterous workspace volume: {report['summary'].get('dexterous_volume', 'N/A')}")
```

### Singularity Analysis

```python
from robot_kinematics.utils.singularity import SingularityAnalyzer

# Create singularity analyzer
analyzer = SingularityAnalyzer(robot)

# Test a joint configuration
joint_config = np.array([0, np.pi/2, 0, 0, 0, 0])
analysis = analyzer.detect_singularities(joint_config)

print(f"Is singular: {analysis['is_singular']}")
print(f"Manipulability: {analysis['manipulability']}")
```

### Trajectory Planning

```python
import numpy as np
from robot_kinematics.inverse.numerical import NumericalIK

# Define trajectory points
waypoints = [
    Transform(position=np.array([0.4, 0.0, 0.5])),
    Transform(position=np.array([0.4, 0.1, 0.5])),
    Transform(position=np.array([0.4, 0.1, 0.6])),
    Transform(position=np.array([0.4, 0.0, 0.6]))
]

# Create IK solver
ik_solver = NumericalIK(robot=robot, method="damped_least_squares")

# Solve IK for each waypoint
joint_trajectory = []
initial_guess = np.array([0, 0, 0, 0, 0, 0])

for i, waypoint in enumerate(waypoints):
    solution, success, error = ik_solver.solve(waypoint, initial_guess)
    if success:
        joint_trajectory.append(solution)
        initial_guess = solution  # Use solution as next initial guess
        print(f"Waypoint {i+1}: Success")
    else:
        print(f"Waypoint {i+1}: Failed")

print(f"Trajectory planning completed: {len(joint_trajectory)}/{len(waypoints)} waypoints")
```

## Different Robot Types

### Panda Robot

```python
from robot_kinematics.robots.serial import PandaManipulator

panda = PandaManipulator()
print(f"Panda robot: {panda.name}")
print(f"Number of joints: {panda.n_joints}")  # 7 DOF
```

### SCARA Robot

```python
from robot_kinematics.robots.serial import SCARAManipulator

scara = SCARAManipulator()
print(f"SCARA robot: {scara.name}")
print(f"Joint types: {scara.joint_types}")  # ['revolute', 'revolute', 'prismatic', 'revolute']
```

### Stewart Platform

```python
from robot_kinematics.robots.parallel import StewartPlatform

config = {
    'base_radius': 0.2,
    'platform_radius': 0.1,
    'leg_length': 0.3,
    'n_legs': 6
}
stewart = StewartPlatform(config)

# Forward kinematics
leg_lengths = np.array([0.3, 0.3, 0.3, 0.3, 0.3, 0.3])
pose = stewart.forward_kinematics(leg_lengths)
print(f"Platform pose: {pose.position}")
```

### KUKA KR5 Robot

```python
from robot_kinematics.robots.serial import KUKAKR5Manipulator

kuka = KUKAKR5Manipulator()
print(f"KUKA KR5 robot: {kuka.name}")
print(f"Number of joints: {kuka.n_joints}")
```

## Error Handling

```python
from robot_kinematics.core.exceptions import KinematicsError, SingularityError

try:
    # Try to solve IK
    solution, success, error = ik_solver.solve(target_pose, initial_guess)
    if not success:
        print(f"IK failed with error: {error}")
except KinematicsError as e:
    print(f"Kinematics error: {e}")
except SingularityError as e:
    print(f"Singularity detected: {e}")
```

## Performance Tips

1. **Use appropriate IK methods:**
   - `"damped_least_squares"`: Good balance of speed and accuracy
   - `"levenberg_marquardt"`: More accurate but slower
   - `"gradient_descent"`: Fastest but may not converge

2. **Provide good initial guesses:**
   ```python
   # Use previous solution as initial guess for next point
   initial_guess = previous_solution
   ```

3. **Handle singularities:**
   ```python
   # Check manipulability before using solution
   if jacobian.manipulability() < 0.01:
       print("Warning: Near singularity")
   ```

4. **Batch processing:**
   ```python
   # Process multiple configurations efficiently
   joint_configs = np.array([config1, config2, config3])
   poses = [robot.forward_kinematics(config) for config in joint_configs]
   ```

## Next Steps

1. **Explore Examples:** Check the `examples/` directory for more detailed examples
2. **Read API Reference:** See `docs/API_REFERENCE.md` for complete documentation
3. **Run Tests:** Execute `python -m pytest tests/` to verify installation
4. **Custom Robots:** Create your own robot configurations using the base classes

## Common Issues

### Import Errors
- Make sure you've installed the package correctly
- Check that you're using the correct import paths

### IK Convergence Issues
- Try different initial guesses
- Use different IK methods
- Check if the target pose is reachable

### Performance Issues
- Reduce workspace analysis sample sizes
- Use faster IK methods for real-time applications
- Cache frequently used computations 

## Integration Examples

### URDF Import/Export

```python
from robot_kinematics.integration.urdf_utils import load_robot_from_urdf, create_urdf_from_config
from robot_kinematics.robots.serial import SerialManipulator

# Load robot from URDF
config = load_robot_from_urdf("robot.urdf")
robot = SerialManipulator(config)

# Create URDF from robot configuration
create_urdf_from_config(robot_config, "output.urdf")
```

### PyBullet Visualization

```python
from robot_kinematics.integration.pybullet_utils import connect_gui, create_kuka_kr5_pybullet, animate_trajectory

# Connect to PyBullet GUI
connect_gui()

# Load robot model
robot_id = create_kuka_kr5_pybullet()

# Animate trajectory
joint_trajectory = [q1, q2, q3, ...]  # List of joint configurations
animate_trajectory(robot_id, joint_trajectory, dt=0.05)
``` 