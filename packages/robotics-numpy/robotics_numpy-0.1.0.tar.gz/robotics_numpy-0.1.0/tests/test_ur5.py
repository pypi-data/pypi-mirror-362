from robotics_numpy.models import Generic
import numpy as np

# Create your custom robot (exactly like your example)
robot = Generic(
    dofs=6,
    a=[0, -0.42500, -0.39225, 0, 0, 0],
    d=[0.089459, 0, 0, 0.10915, 0.09465, 0.0823],
    alpha=[np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2, 0],
    # offset=[0, -np.pi / 2, 0, 0],
    # qlim=[[-np.pi, np.pi], [-np.pi / 2, np.pi / 2],
    #       [-np.pi / 3, np.pi / 3], [-np.pi / 6, np.pi / 6],
    #       [-np.pi / 4, np.pi / 4], [-np.pi / 4, np.pi / 4]],
    name="UR5",
)

# Forward kinematics
T = robot.fkine(robot.qz)
print(f"End-effector position: {T.t}")

# 3D visualization (if plotly installed)
robot.plotly(
    q=[0, 0, 0, 0, 0, 0],
    show_z_axis=True,
    frame_size=0.05,
    show_all_axes=True,
    show=True,
)
