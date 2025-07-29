from robotics_numpy.models import Generic
import numpy as np

# Create your custom robot (exactly like your example)
robot = Generic(
    dofs=4,
    a=[0, -0.5, -0.5, -0.5],
    d=[0.5, 0, 0, 0],
    alpha=[np.pi / 2, 0, 0, 0],
    offset=[0, -np.pi / 2, 0, 0],
    qlim=[
        [-np.pi, np.pi],
        [-np.pi / 2, np.pi / 2],
        [-np.pi / 3, np.pi / 3],
        [-np.pi / 6, np.pi / 6],
    ],
    name="GenericRobot",
)

# Forward kinematics
T = robot.fkine(robot.qz)
print(f"End-effector position: {T.t}")
print(robot.qlim.shape)

# 3D visualization (if plotly installed)
robot.plotly(q=[0, 0, 0, 0], show=True)
