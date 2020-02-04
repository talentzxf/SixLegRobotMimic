import numpy as np
import math

from Geometry.TriangleOps import radToDeg, cosine_law, degToRad, get_intersections, sine_law, vector_angle, \
    vector_length, vector_dir


class IKSolver:
    def __init__(self, minAngle=-90.0, maxAngle=90.0):
        self.prev_angles = None
        self.links = []
        self.minAngle = minAngle
        self.maxAngle = maxAngle

    def add_link(self, link):
        self.links.append(link)

    def isValidAngles(self, angles):
        for angle in angles:
            if angle > self.maxAngle or angle < self.minAngle:
                return False
        return True

    def getAngle(self, target_x, target_y, mid_x, mid_y):
        theta1_pre = math.atan2(mid_y, mid_x - self.links[0].getLength())
        l_prime_1 = vector_length([mid_x - self.links[0].getLength(), mid_y])
        theta1 = theta1_pre - sine_law(self.links[2].getLength(), l_prime_1,
                                       degToRad(180 - self.links[2].getInitTheta()))

        # Use vector to find theta2
        p_triangle_point = [self.links[1].getLength() * math.cos(theta1) + self.links[0].getLength(),
                            self.links[1].getLength() * math.sin(theta1)]
        vector1 = [mid_x - p_triangle_point[0], mid_y - p_triangle_point[1]]
        vector2 = [target_x - mid_x, target_y - mid_y]
        angle = vector_angle(vector1, vector2)

        l_prime_2 = vector_length([target_x - mid_x, target_y - mid_y])
        theta2_pre = sine_law(self.links[4].getLength(), l_prime_2, degToRad(180 - self.links[4].getInitTheta()))
        theta2 = angle - theta2_pre * vector_dir(vector1, vector2)

        return [radToDeg(theta1), radToDeg(theta2)]

    # TODO: This is hard coded, solve it using Newton's method
    def solve(self, p):
        theta0 = radToDeg(math.atan2(p[1], p[2]))
        p_conv_x = math.sqrt(p[1] * p[1] + p[2] * p[2])
        p_conv_y = p[0]

        x0 = self.links[0].getLength()
        y0 = 0
        r0 = cosine_law(degToRad(180.0 - self.links[2].getInitTheta()), self.links[1].getLength(),
                        self.links[2].getLength())

        x1 = p_conv_x
        y1 = p_conv_y
        r1 = cosine_law(degToRad(180.0 - self.links[4].getInitTheta()), self.links[3].getLength(),
                        self.links[4].getLength())

        try:
            intersect_points = get_intersections(x0, y0, r0, x1, y1, r1)
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
                self.getAngle(p_conv_x, p_conv_y, intersect_points[0][0], intersect_points[0][1]))
        else:
            mid_point_0 = intersect_points[0]
            mid_point_1 = intersect_points[1]
            candidate_angle_array.append(
                self.getAngle(p_conv_x, p_conv_y, mid_point_0[0], mid_point_0[1]))
            candidate_angle_array.append(
                self.getAngle(p_conv_x, p_conv_y, mid_point_1[0], mid_point_1[1]))

        valid_angles = []
        for candidate_angle in candidate_angle_array:
            if self.isValidAngles(candidate_angle):
                valid_angles.append(candidate_angle)

        if len(valid_angles) == 0:
            return None

        cur_candidate_angle = valid_angles[0]

        if self.prev_angles is not None:
            cur_min_dist = float("inf")
            for candidate_angle in valid_angles:
                curDiff = math.fabs(candidate_angle[0] - self.prev_angles[1]) + \
                          math.fabs(candidate_angle[1] - self.prev_angles[2])
                if cur_min_dist > curDiff:
                    cur_min_dist = curDiff
                    cur_candidate_angle = candidate_angle

        self.prev_angles = [theta0, cur_candidate_angle[0],
                            cur_candidate_angle[1]]
        return self.prev_angles

    # # If given 4 points, last linke has to be fixed.
    # def solve(self, p):  # Find the three angles
    #     isFourPoints = False
    #     if len(self.prev_angles) == 0 and len(self.l_array) != 0:
    #         for i in range(len(self.l_array)):
    #             self.prev_angles.append(0.0)
    #
    #     print("Target:" + str(p))
    #
    #     # theta0 is just rotation toward the target point in y-z plane
    #     theta0 = -180.0 * math.atan2(p[1], p[2]) / math.pi
    #
    #     # calculate other two angles in x-xp plane:
    #     p_conv_x = math.sqrt(p[1] * p[1] + p[2] * p[2])
    #     p_conv_y = p[0]
    #
    #     x0 = self.l_array[0]
    #     y0 = 0
    #     r0 = self.l_array[1]
    #
    #     x1 = p_conv_x
    #     y1 = p_conv_y
    #     if len(self.l_array) >= 4 and self.l_array[3] is not None and self.l_array[3] > 0:
    #         r1 = self.cosine_law(180 - self.start_angles[3], self.l_array[2], self.l_array[3])
    #         isFourPoints = True
    #     else:
    #         r1 = self.l_array[2]
    #
    #     try:
    #         intersect_points = get_intercetions(x0, y0, r0, x1, y1, r1)
    #     except ValueError:
    #         d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    #         a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
    #         print("x0:{} y0:{} r0:{}".format(x0, y0, r0))
    #         print("x1:{} y1:{} r1:{}".format(x1, y1, r1))
    #         print("d is:{}, a is:{} r0:{}".format(d, a, r0))
    #         return None
    #     if intersect_points is None:
    #         return None
    #
    #     candidate_angle_array = []
    #     if len(intersect_points) == 1:  # Only one point, just calculate the angle
    #         candidate_angle_array.append(
    #             self.getAngle(p_conv_x, p_conv_y, intersect_points[0][0], intersect_points[0][1], isFourPoints))
    #     else:
    #         mid_point_0 = intersect_points[0]
    #         mid_point_1 = intersect_points[1]
    #         candidate_angle_array.append(
    #             self.getAngle(p_conv_x, p_conv_y, mid_point_0[0], mid_point_0[1], isFourPoints))
    #         candidate_angle_array.append(
    #             self.getAngle(p_conv_x, p_conv_y, mid_point_1[0], mid_point_1[1], isFourPoints))
    #
    #     cur_candidate_angle = None
    #     for candidate_angle in candidate_angle_array:
    #         if self.isValidAngles(candidate_angle):
    #             cur_candidate_angle = candidate_angle
    #             break
    #
    #     # None of the angles in the array can satisfy the angle criteria,
    #     if cur_candidate_angle is None:
    #         return None
    #
    #     cur_min_dist = float("inf")
    #     for candidate_angle in candidate_angle_array:
    #         # Rule out all impossible angles:
    #         if self.isValidAngles(candidate_angle):
    #             curDiff = math.fabs(candidate_angle[0] - self.prev_angles[1]) + math.fabs(
    #                 candidate_angle[1] - self.prev_angles[2])
    #             if cur_min_dist > curDiff:
    #                 cur_min_dist = curDiff
    #                 cur_candidate_angle = candidate_angle
    #
    #     self.prev_angles = [theta0, cur_candidate_angle[0],
    #                         cur_candidate_angle[1]]
    #     return self.prev_angles


if __name__ == '__main__':
    # print(get_intercetions(0, 0, 1, 2, 0, 1))
    # solver = IKSolver([1., 1., 1.], [0., 0., 0.])
    # print(solver.solve([0, 0, 2]))
    print(get_intercetions(0.05, 0, 0.2, 0.45, 0, 0.2))
import numpy as np
import math

from Geometry.TriangleOps import radToDeg, cosine_law, degToRad, get_intersections, sine_law, vector_angle, \
    vector_length, vector_dir


class IKSolver:
    def __init__(self, minAngle=-90.0, maxAngle=90.0):
        self.prev_angles = None
        self.links = []
        self.minAngle = minAngle
        self.maxAngle = maxAngle

    def add_link(self, link):
        self.links.append(link)

    def isValidAngle(self, angle):
        if angle > self.maxAngle or angle < self.minAngle:
            return False
        return True

    def isValidAngles(self, angles):
        for angle in angles:
            if not self.isValidAngle(angle):
                return False
        return True

    def getAngle(self, target_x, target_y, mid_x, mid_y):
        theta1_pre = math.atan2(mid_y, mid_x - self.links[0].getLength())
        l_prime_1 = vector_length([mid_x - self.links[0].getLength(), mid_y])
        theta1 = theta1_pre - sine_law(self.links[2].getLength(), l_prime_1,
                                       degToRad(180 - self.links[2].getInitTheta()))

        # Use vector to find theta2
        p_triangle_point = [self.links[1].getLength() * math.cos(theta1) + self.links[0].getLength(),
                            self.links[1].getLength() * math.sin(theta1)]
        vector1 = [mid_x - p_triangle_point[0], mid_y - p_triangle_point[1]]
        vector2 = [target_x - mid_x, target_y - mid_y]
        angle = vector_angle(vector1, vector2)

        l_prime_2 = vector_length([target_x - mid_x, target_y - mid_y])
        theta2_pre = sine_law(self.links[4].getLength(), l_prime_2, degToRad(180 - self.links[4].getInitTheta()))

        if vector_dir(vector1, vector2) == -1:
            theta2 = -angle - theta2_pre
        else:
            theta2 = angle - theta2_pre

        return [radToDeg(theta1), radToDeg(theta2)]

    # TODO: This is hard coded, solve it using Newton's method
    def solve(self, p):
        theta0 = radToDeg(-math.atan2(p[1], p[2]))
        if not self.isValidAngle(theta0):
            return None
        p_conv_x = math.sqrt(p[1] * p[1] + p[2] * p[2])
        p_conv_y = p[0]

        x0 = self.links[0].getLength()
        y0 = 0
        r0 = cosine_law(degToRad(180.0 - self.links[2].getInitTheta()), self.links[1].getLength(),
                        self.links[2].getLength())

        x1 = p_conv_x
        y1 = p_conv_y
        r1 = cosine_law(degToRad(180.0 - self.links[4].getInitTheta()), self.links[3].getLength(),
                        self.links[4].getLength())

        try:
            intersect_points = get_intersections(x0, y0, r0, x1, y1, r1)
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
                self.getAngle(p_conv_x, p_conv_y, intersect_points[0][0], intersect_points[0][1]))
        else:
            mid_point_0 = intersect_points[0]
            mid_point_1 = intersect_points[1]
            candidate_angle_array.append(
                self.getAngle(p_conv_x, p_conv_y, mid_point_0[0], mid_point_0[1]))
            candidate_angle_array.append(
                self.getAngle(p_conv_x, p_conv_y, mid_point_1[0], mid_point_1[1]))

        valid_angles = []
        for candidate_angle in candidate_angle_array:
            if self.isValidAngles(candidate_angle):
                valid_angles.append(candidate_angle)

        if len(valid_angles) == 0:
            return None

        cur_candidate_angle = valid_angles[0]

        if self.prev_angles is not None:
            cur_min_dist = float("inf")
            for candidate_angle in valid_angles:
                curDiff = math.fabs(candidate_angle[0] - self.prev_angles[1]) + \
                          math.fabs(candidate_angle[1] - self.prev_angles[2])
                if cur_min_dist > curDiff:
                    cur_min_dist = curDiff
                    cur_candidate_angle = candidate_angle

        self.prev_angles = [theta0, cur_candidate_angle[0],
                            cur_candidate_angle[1]]
        return self.prev_angles

    # # If given 4 points, last linke has to be fixed.
    # def solve(self, p):  # Find the three angles
    #     isFourPoints = False
    #     if len(self.prev_angles) == 0 and len(self.l_array) != 0:
    #         for i in range(len(self.l_array)):
    #             self.prev_angles.append(0.0)
    #
    #     print("Target:" + str(p))
    #
    #     # theta0 is just rotation toward the target point in y-z plane
    #     theta0 = -180.0 * math.atan2(p[1], p[2]) / math.pi
    #
    #     # calculate other two angles in x-xp plane:
    #     p_conv_x = math.sqrt(p[1] * p[1] + p[2] * p[2])
    #     p_conv_y = p[0]
    #
    #     x0 = self.l_array[0]
    #     y0 = 0
    #     r0 = self.l_array[1]
    #
    #     x1 = p_conv_x
    #     y1 = p_conv_y
    #     if len(self.l_array) >= 4 and self.l_array[3] is not None and self.l_array[3] > 0:
    #         r1 = self.cosine_law(180 - self.start_angles[3], self.l_array[2], self.l_array[3])
    #         isFourPoints = True
    #     else:
    #         r1 = self.l_array[2]
    #
    #     try:
    #         intersect_points = get_intercetions(x0, y0, r0, x1, y1, r1)
    #     except ValueError:
    #         d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    #         a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
    #         print("x0:{} y0:{} r0:{}".format(x0, y0, r0))
    #         print("x1:{} y1:{} r1:{}".format(x1, y1, r1))
    #         print("d is:{}, a is:{} r0:{}".format(d, a, r0))
    #         return None
    #     if intersect_points is None:
    #         return None
    #
    #     candidate_angle_array = []
    #     if len(intersect_points) == 1:  # Only one point, just calculate the angle
    #         candidate_angle_array.append(
    #             self.getAngle(p_conv_x, p_conv_y, intersect_points[0][0], intersect_points[0][1], isFourPoints))
    #     else:
    #         mid_point_0 = intersect_points[0]
    #         mid_point_1 = intersect_points[1]
    #         candidate_angle_array.append(
    #             self.getAngle(p_conv_x, p_conv_y, mid_point_0[0], mid_point_0[1], isFourPoints))
    #         candidate_angle_array.append(
    #             self.getAngle(p_conv_x, p_conv_y, mid_point_1[0], mid_point_1[1], isFourPoints))
    #
    #     cur_candidate_angle = None
    #     for candidate_angle in candidate_angle_array:
    #         if self.isValidAngles(candidate_angle):
    #             cur_candidate_angle = candidate_angle
    #             break
    #
    #     # None of the angles in the array can satisfy the angle criteria,
    #     if cur_candidate_angle is None:
    #         return None
    #
    #     cur_min_dist = float("inf")
    #     for candidate_angle in candidate_angle_array:
    #         # Rule out all impossible angles:
    #         if self.isValidAngles(candidate_angle):
    #             curDiff = math.fabs(candidate_angle[0] - self.prev_angles[1]) + math.fabs(
    #                 candidate_angle[1] - self.prev_angles[2])
    #             if cur_min_dist > curDiff:
    #                 cur_min_dist = curDiff
    #                 cur_candidate_angle = candidate_angle
    #
    #     self.prev_angles = [theta0, cur_candidate_angle[0],
    #                         cur_candidate_angle[1]]
    #     return self.prev_angles


if __name__ == '__main__':
    # print(get_intercetions(0, 0, 1, 2, 0, 1))
    # solver = IKSolver([1., 1., 1.], [0., 0., 0.])
    # print(solver.solve([0, 0, 2]))
    print(get_intercetions(0.05, 0, 0.2, 0.45, 0, 0.2))
