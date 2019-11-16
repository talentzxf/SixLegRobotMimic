import numpy as np
import math


def get_intercetions(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    # non intersecting
    if d > r0 + r1:
        return None
    # One circle within other
    if d < abs(r0 - r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(r0 ** 2 - a ** 2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d

        if x3 == x4 and y3 == y4:
            return [(x3, y3)]
        else:
            return [(x3, y3), (x4, y4)]


class IKSolver:
    def __init__(self, l_array, start_angles):
        self.l_array = l_array  # link length definition
        self.prev_angles = start_angles

    def getAngle(self, target_x, target_y, mid_x, mid_y):
        theta1 = math.atan2(mid_y, mid_x)
        theta1_2 = math.atan2(target_y - mid_y, target_x - mid_x)
        theta2 = theta1_2 - theta1
        return [-180*theta1/math.pi, -180*theta2/math.pi]

    # TODO: Currently, we only implement 3 link system. Can we do this for any number of links? hmmmmm
    def solve(self, p):  # Find the three angles
        # theta0 is just rotation toward the target point in y-z plane
        theta0 = -180.0 * math.atan2(p[1], p[2]) / math.pi

        # calculate other two angles in x-xp plane:
        p_conv_x = p[1] * p[1] + p[2] * p[2]
        p_conv_y = p[0]

        x0 = self.l_array[0]
        y0 = 0
        r0 = self.l_array[1]

        x1 = math.sqrt(p_conv_x)
        y1 = p_conv_y
        r1 = self.l_array[2]

        intersect_points = get_intercetions(x0, y0, r0, x1, y1, r1)
        if intersect_points is None:
            return None
        if len(intersect_points) == 1:  # Only one point, just calculate the angle
            angles = self.getAngle(p_conv_x, p_conv_y, intersect_points[0][0], intersect_points[0][1])
            self.prev_angles = [theta0, angles[1], angles[2]]
            return self.prev_angles

        mid_point_0 = intersect_points[0]
        mid_point_1 = intersect_points[1]
        angles_1 = self.getAngle(p_conv_x, p_conv_y, mid_point_0[0], mid_point_0[1])
        angles_2 = self.getAngle(p_conv_x, p_conv_y, mid_point_1[0], mid_point_1[1])

        diff1 = math.fabs(angles_1[0] - self.prev_angles[1]) + math.fabs(angles_1[1] - self.prev_angles[2])
        diff2 = math.fabs(angles_2[0] - self.prev_angles[1]) + math.fabs(angles_2[1] - self.prev_angles[2])
        if diff1 < diff2:
            self.prev_angles = [theta0, angles_1[0], angles_1[1]]
            return self.prev_angles
        self.prev_angles = [theta0, angles_2[0], angles_2[1]]
        return self.prev_angles


if __name__ == '__main__':
    print(get_intercetions(0, 0, 1, 2, 0, 1))
