import pybullet as p
import pybullet_data
import numpy as np
import time


def connect_gui():
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.resetSimulation()
    p.setGravity(0, 0, -9.81)

def disconnect():
    p.disconnect()

def load_plane():
    return p.loadURDF("plane.urdf")

def create_kuka_kr5_pybullet():
    """Load a simple KUKA KR5 model in PyBullet using DH parameters (visual only)."""
    # For demonstration, use a simple chain of links
    # For real robots, use URDF files
    base_position = [0, 0, 0]
    base_orientation = p.getQuaternionFromEuler([0, 0, 0])
    kuka_urdf = pybullet_data.getDataPath() + "/kuka_iiwa/model.urdf"  # Placeholder
    robot_id = p.loadURDF(kuka_urdf, base_position, base_orientation, useFixedBase=True)
    return robot_id

def set_joint_positions(robot_id, joint_positions):
    n_joints = p.getNumJoints(robot_id)
    for i in range(n_joints):
        p.resetJointState(robot_id, i, joint_positions[i])

def animate_trajectory(robot_id, trajectory, dt=0.05):
    for q in trajectory:
        set_joint_positions(robot_id, q)
        p.stepSimulation()
        time.sleep(dt) 