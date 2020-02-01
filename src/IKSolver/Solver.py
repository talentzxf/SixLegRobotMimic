import numpy as np
import math

eps = 0.00001


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

    # Two tangent circle:
    if math.fabs(d - r0 - r1) < eps:
        x3 = r0 / (r0 + r1) * (x1 - x0) + x0
        y3 = r0 / (r0 + r1) * (y1 - y0) + y0
        return [(x3, y3)]
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
    def __init__(self, l_array, start_angles, minAngle = -90.0, maxAngle = 90.0):
        self.l_array = l_array  # link length definition
        self.prev_angles = []
        self.start_angles = start_angles
        self.minAngle = minAngle
        self.maxAngle = maxAngle

    def getAngle(self, target_x, target_y, mid_x, mid_y, isFourPoints=False):
        theta1 = math.atan2(mid_y, mid_x - self.l_array[0])
        theta1_2 = math.atan2(target_y - mid_y, target_x - mid_x)
        theta2 = theta1_2 - theta1

        if not isFourPoints:
            return [180 * theta1 / math.pi, 180 * theta2 / math.pi - self.start_angles[2]]

        l_prime = math.sqrt((target_x - mid_x) * (target_x - mid_x) + (target_y - mid_y) * (target_y - mid_y))
        # Use sine law to find the angle
        triangle_theta = math.asin(self.l_array[3] / l_prime * math.sin(self.start_angles[3] / 180 * math.pi))

        theta2_1 = theta2 - triangle_theta
        return [180 * theta1 / math.pi, 180 * theta2_1 / math.pi - self.start_angles[2]]

    # calculate the length of an triangle, given other two edge length and the other angle
    def cosine_law(self, theta, l1, l2):
        radian = theta / 180 * math.pi
        return math.sqrt(l1 * l1 + l2 * l2 - 2 * math.cos(radian) * l1 * l2)

    def isValidAngles(self, angles):
        for angle in angles:
            if angle > self.maxAngle or angle < self.minAngle:
                return False
        return True

    # If given 4 points, last linke has to be fixed.
    def solve(self, p):  # Find the three angles
        isFourPoints = False
        if len(self.prev_angles) == 0 and len(self.l_array) != 0:
            for i in range(len(self.l_array)):
                self.prev_angles.append(0.0)

        print("Target:" + str(p))

        # theta0 is just rotation toward the target point in y-z plane
        theta0 = -180.0 * math.atan2(p[1], p[2]) / math.pi

        # calculate other two angles in x-xp plane:
        p_conv_x = math.sqrt(p[1] * p[1] + p[2] * p[2])
        p_conv_y = p[0]

        x0 = self.l_array[0]
        y0 = 0
        r0 = self.l_array[1]

        x1 = p_conv_x
        y1 = p_conv_y
        if len(self.l_array) >= 4 and self.l_array[3] is not None and self.l_array[3] > 0:
            r1 = self.cosine_law(180 - self.start_angles[3], self.l_array[2], self.l_array[3])
            isFourPoints = True
        else:
            r1 = self.l_array[2]

        try:
            intersect_points = get_intercetions(x0, y0, r0, x1, y1, r1)
        except ValueError:
            d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
            print("x0:{} y0:{} r0:{}".format(x0, y0, r0))
            print("x1:{} y1:{} r1:{}".format(x1, y1, r1))
            print("d is:{}, a is:{} r0:{}".format(d, a, r0))
            return None
        if intersect_points is None:
            return None

        candidate_angle_array = []
        if len(intersect_points) == 1:  # Only one point, just calculate the angle
            candidate_angle_array.append(
                self.getAngle(p_conv_x, p_conv_y, intersect_points[0][0], intersect_points[0][1], isFourPoints))
        else:
            mid_point_0 = intersect_points[0]
            mid_point_1 = intersect_points[1]
            candidate_angle_array.append(
                self.getAngle(p_conv_x, p_conv_y, mid_point_0[0], mid_point_0[1], isFourPoints))
            candidate_angle_array.append(
                self.getAngle(p_conv_x, p_conv_y, mid_point_1[0], mid_point_1[1], isFourPoints))

        cur_candidate_angle = None
        for candidate_angle in candidate_angle_array:
            if self.isValidAngles(candidate_angle):
                cur_candidate_angle = candidate_angle
                break

        # None of the angles in the array can satisfy the angle criteria,
        if cur_candidate_angle is None:
            return None

        cur_min_dist = float("inf")
        for candidate_angle in candidate_angle_array:
            # Rule out all impossible angles:
            if self.isValidAngles(candidate_angle):
                curDiff = math.fabs(candidate_angle[0] - self.prev_angles[1]) + math.fabs(
                    candidate_angle[1] - self.prev_angles[2])
                if cur_min_dist > curDiff:
                    cur_min_dist = curDiff
                    cur_candidate_angle = candidate_angle

        self.prev_angles = [theta0, cur_candidate_angle[0],
                            cur_candidate_angle[1]]
        return self.prev_angles


if __name__ == '__main__':
    # print(get_intercetions(0, 0, 1, 2, 0, 1))
    # solver = IKSolver([1., 1., 1.], [0., 0., 0.])
    # print(solver.solve([0, 0, 2]))
    print(get_intercetions(0.05, 0, 0.2, 0.45, 0, 0.2))
