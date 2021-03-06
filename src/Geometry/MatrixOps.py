import numpy as np
import math as m


def translate_matrix(x, y, z):
    return np.matrix(
        [[1, 0, 0, x],
         [0, 1, 0, y],
         [0, 0, 1, z],
         [0, 0, 0, 1]])


def rotate_matrix(angle_theta, axis):
    # Use right hand rule !!!
    # convert theta into radian
    theta = angle_theta / 180 * m.pi
    s = m.sin(theta)
    c = m.cos(theta)
    verst = 1 - c

    a0 = axis[0]
    a1 = axis[1]
    a2 = axis[2]

    ax2 = axis[0] * axis[0]
    ay2 = axis[1] * axis[1]
    az2 = axis[2] * axis[2]
    axy = axis[0] * axis[1]
    ayz = axis[1] * axis[2]
    axz = axis[0] * axis[2]

    return np.matrix(
        [[c + ax2 * verst, axy * verst - a2 * s, axz * verst + a1 * s, 0, ],
         [axy * verst + a2 * s, c + ay2 * verst, ayz * verst - a0 * s, 0],
         [axz * verst - a1 * s, ayz * verst + a0 * s, c + az2 * verst, 0],
         [0, 0, 0, 1]]
    )
