import numpy as np
from robot_kinematics.integration.pybullet_utils import connect_gui, disconnect, load_plane, create_kuka_kr5_pybullet, set_joint_positions, animate_trajectory
from robot_kinematics.robots.serial import KUKAKR5Manipulator
import time

def main():
    connect_gui()
    load_plane()
    robot_id = create_kuka_kr5_pybullet()
    kuka = KUKAKR5Manipulator()
    
    # Home position
    home = np.zeros(6)
    set_joint_positions(robot_id, home)
    time.sleep(1)
    
    # Simple trajectory: move joint 1 and 2
    n_steps = 50
    q_traj = []
    for t in np.linspace(0, np.pi/2, n_steps):
        q = np.zeros(6)
        q[0] = t
        q[1] = t/2
        q_traj.append(q)
    animate_trajectory(robot_id, q_traj, dt=0.03)
    
    time.sleep(2)
    disconnect()

if __name__ == "__main__":
    main() 