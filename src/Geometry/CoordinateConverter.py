from PyQt5.QtCore import Qt, QRect, QPoint, QSize
import numpy as np


class CoordinateConverter:
    scrWidth = 400
    scrHeight = 400
    scale = 200

    def __init__(self):
        self.centerX = CoordinateConverter.scrWidth / 2
        self.centerY = CoordinateConverter.scrHeight / 2

    def convertRectToScr(self, x, y, width, height):
        left = self.centerX + x * CoordinateConverter.scale
        width = width * CoordinateConverter.scale
        top = self.centerY - y * CoordinateConverter.scale
        height = height * CoordinateConverter.scale
        return QRect(left, top, width, height)

    def worldToScr(self, x, y):
        scrX = self.centerX + x * CoordinateConverter.scale
        scrY = self.centerY - y * CoordinateConverter.scale
        return QPoint(scrX, scrY)

    def scrToWorld(self, scrPoint):
        return [(scrPoint.x() - self.centerX) / CoordinateConverter.scale,
                (self.centerY - scrPoint.y()) / CoordinateConverter.scale]

    def objectToWorld(self, point, objTransformationMatrix):
        # TODO: Optimize as rotation matrix is orthogonality
        inv_obj_trans = np.linalg.inv(objTransformationMatrix)
        point.append(1)
        point_vector = np.array(point)[np.newaxis].T
        target_matrix = np.matmul(inv_obj_trans, point_vector)
        target_point = np.asarray(target_matrix[0:3, :]).flatten().tolist()
        return target_point

    def worldToObject(self, point, objTransformationMatrix):
        point.append(1)
        point_vector = np.array(point)[np.newaxis].T
        target_matrix = np.matmul(objTransformationMatrix, point_vector)
        target_point = np.asarray(target_matrix[0:3, :]).flatten().tolist()
        return target_point


# unit tests
if __name__ == '__main__':
    import MatrixOps
    import math

    conv = CoordinateConverter()
    rotation = MatrixOps.rotate_matrix(45, [0, 0, 1])
    transformation = MatrixOps.translate_matrix(1, 1, 0)
    objTransformationMatrix = np.matmul(transformation, rotation)
    origin_obj = [0, 0, 0]
    converted_world_origin = conv.worldToObject(origin_obj, objTransformationMatrix)
    print(converted_world_origin, " should be:", [1, 1, 0])

    test_point_obj = [1, 0, 0]
    converted_world_point = conv.worldToObject(test_point_obj, objTransformationMatrix)
    print(converted_world_point, " should be:", [math.sqrt(2) / 2 + 1, math.sqrt(2) / 2 + 1, 0])

    origin_world = [0, 0, 0]
    converted_obj_origin = conv.objectToWorld(origin_world, objTransformationMatrix)
    print(converted_obj_origin, " should be:", [-math.sqrt(2) / 2, 0, 0])

    origin_world_point = [1, 0, 0]
    converted_obj_point = conv.objectToWorld(origin_world_point, objTransformationMatrix)
    print(converted_obj_point, " should be:", [-math.sqrt(2) / 2, -math.sqrt(2) / 2, 0])

    # Robot leg 1
    leg_rotation = MatrixOps.rotate_matrix(45, [0, 0, 1])
    leg_transformation = MatrixOps.translate_matrix(0.1, 0.15, 0)
    leg_objTransformationMatrix = np.matmul(leg_transformation, leg_rotation)
    print(leg_objTransformationMatrix)
