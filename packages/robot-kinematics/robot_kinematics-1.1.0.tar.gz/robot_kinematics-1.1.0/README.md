# Robot Kinematics Library

A comprehensive, production-ready robotics kinematics library for Python that provides forward and inverse kinematics, Jacobian calculations, and advanced robotics analysis tools with URDF and PyBullet integration.

**Author:** Sherin Joseph Roy  
**Email:** sherin.joseph2217@gmail.com  
**Repository:** https://github.com/Sherin-SEF-AI/robot-kinematics

## Features

- **Forward Kinematics**: DH parameters, URDF parsing, multiple robot configurations
- **Inverse Kinematics**: Numerical, analytical, and hybrid solvers
- **Jacobian Analysis**: Geometric and analytical Jacobians, singularity detection
- **Robot Types**: UR5, Panda, SCARA, Delta, KUKA KR5, Stewart platform, mobile manipulators
- **Advanced Features**: Workspace analysis, singularity avoidance, performance optimization
- **Integration**: URDF import/export, PyBullet visualization and animation
- **High Performance**: JIT compilation, caching, vectorized operations

## Installation

### Basic Installation
```bash
pip install robot-kinematics
```

### With Visualization Support
```bash
pip install robot-kinematics[visualization]
```

### Full Installation (All Dependencies)
```bash
pip install robot-kinematics[full]
```

## Quick Start

```python
import numpy as np
from robot_kinematics.robots.serial import UR5Manipulator, KUKAKR5Manipulator
from robot_kinematics.inverse.numerical import NumericalIK
from robot_kinematics.core.transforms import Transform

# Create a UR5 robot
ur5 = UR5Manipulator()
print(f"Robot: {ur5.config['name']}")
print(f"Number of joints: {ur5.n_joints}")

# Forward kinematics
joint_config = np.array([0, 0, 0, 0, 0, 0])  # Home position
pose = ur5.forward_kinematics(joint_config)
print(f"End-effector position: {pose.position}")

# Inverse kinematics
target_pose = Transform(position=np.array([0.4, 0.0, 0.5]))
ik_solver = NumericalIK(robot=ur5, method="damped_least_squares")
solution, success, error = ik_solver.solve(target_pose, joint_config)

if success:
    print(f"IK solution: {solution}")
    print(f"Error: {error}")

# Create KUKA KR5 robot
kuka = KUKAKR5Manipulator()
print(f"KUKA KR5 robot: {kuka.config['name']}")
```

## URDF Integration

```python
from robot_kinematics.integration.urdf_utils import load_robot_from_urdf
from robot_kinematics.robots.serial import SerialManipulator

# Load robot from URDF file
config = load_robot_from_urdf("robot.urdf")
robot = SerialManipulator(config)
```

## PyBullet Visualization

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

## Documentation

For detailed documentation, examples, and API reference, visit our [documentation](https://robotkinematics.readthedocs.io/).

## Supported Robot Types

- **Serial Manipulators**: UR5, Panda, SCARA, Delta, KUKA KR5
- **Parallel Robots**: Stewart platform, Delta parallel
- **Mobile Manipulators**: Dual-arm systems, mobile bases

## Performance Features

- **JIT Compilation**: Using Numba for accelerated computations
- **Caching**: Thread-safe caching for repeated calculations
- **Vectorization**: Optimized NumPy operations
- **Memory Management**: Efficient memory usage for large-scale operations

## Examples

Check the `examples/` directory for comprehensive examples:
- `basic_usage.py` - Basic kinematics operations
- `simple_advanced_example.py` - Trajectory planning and analysis
- `pybullet_kuka_kr5_demo.py` - PyBullet visualization demo
- `urdf_import_export_demo.py` - URDF integration demo

## Testing

Run the test suite:

```bash
pytest tests/
```

## Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this library in your research, please cite:

```bibtex
@software{robot_kinematics,
  title={Robot Kinematics Library},
  author={Sherin Joseph Roy},
  year={2024},
  url={https://github.com/Sherin-SEF-AI/robot-kinematics}
}
``` 