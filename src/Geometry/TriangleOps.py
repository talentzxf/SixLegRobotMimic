import math

eps = 0.00001


# calculate the length of an triangle, given other two edge length and the other angle
def cosine_law(theta, l1, l2):
    return math.sqrt(l1 * l1 + l2 * l2 - 2 * math.cos(theta) * l1 * l2)


# Use sine law to find the angle
def sine_law(l1, l2, theta):
    return math.asin(l1 / l2 * math.sin(theta))


# deg to radian
def degToRad(deg):
    return math.pi * deg / 180.0


def radToDeg(rad):
    return rad / math.pi * 180.0


def vector_length(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)


def vector_normalize(v):
    v_len = vector_length(v)
    return [v[0] / v_len, v[1] / v_len]


def vector_angle(v1, v2):
    normalized_v1 = vector_normalize(v1)
    normalized_v2 = vector_normalize(v2)
    dot = normalized_v1[0] * normalized_v2[0] + normalized_v1[1] * normalized_v2[1]

    return math.acos(dot)


def vector_dir(v1, v2):
    cross_z = (v1[0] * v2[1] - v1[1] * v2[0])
    if cross_z > 0:
        return 1;
    elif cross_z == 0:
        return 0;
    return -1


# Get the intersection of two circles
def get_intersections(x0, y0, r0, x1, y1, r1):
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
