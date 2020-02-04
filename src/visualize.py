import matplotlib.pyplot as plt
from shapely import geometry

x0 = 0.5
y0 = 0
r0 = 0.6450581369148056

x1 = 0.42101068870041763
y1 = -1
r1 = 1.1424288100193785

begin = geometry.Point(x0, y0)
target = geometry.Point(x1, y1)
plt.scatter(begin.x, begin.y, s=10)
plt.scatter(target.x, target.y, s=10)

mid_point_0 = geometry.Point(-0.14501278799176803, -0.00764874676575146)
mid_point_1 = geometry.Point(1.1358129788333566, -0.10882029198202751)

# line1 = geometry.LineString([begin, target])
line = geometry.LineString([(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)])

plt.plot(line.xy)

p_triangle_point = [-0.03572222601921937, -0.12450580929825103]

plt.show()
