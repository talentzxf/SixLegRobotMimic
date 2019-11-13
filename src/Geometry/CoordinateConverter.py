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

    def worldToObject(self, point, objTransformationMatrix):
        # TODO: Optimize as rotation matrix is orthogonality
        inv_obj_trans = np.linalg.inv(objTransformationMatrix)
        point.append(1)
        point_vector = np.array(point)[np.newaxis].T
        target_matrix = np.matmul(inv_obj_trans, point_vector)
        target_point = np.asarray(target_matrix[0:3, :]).flatten().tolist()
        return target_point

    def objectToWorld(self, point, objTransformationMatrix):
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
    converted_world_origin = conv.objectToWorld(origin_obj, objTransformationMatrix)
    print(converted_world_origin, " should be:", [1, 1, 0])

    test_point_obj = [1, 0, 0]
    converted_world_point = conv.objectToWorld(test_point_obj, objTransformationMatrix)
    print(converted_world_point, " should be:", [math.sqrt(2) / 2 + 1, math.sqrt(2) / 2 + 1, 0])

    origin_world = [0, 0, 0]
    converted_obj_origin = conv.worldToObject(origin_world, objTransformationMatrix)
    print(converted_obj_origin, " should be:", [-math.sqrt(2), 0, 0])

    origin_world_point = [1, 0, 0]
    converted_obj_point = conv.worldToObject(origin_world_point, objTransformationMatrix)
    print(converted_obj_point, " should be:", [-math.sqrt(2) / 2, -math.sqrt(2) / 2, 0])

    # Rotate 90 around y, z will be x, x will be -z.
    # rotation = MatrixOps.rotate_matrix(90, [0, 1, 0])
    # objTransformationMatrix = rotation
    # obj_x = [1, 0, 0]
    # converted_obj_x = conv.objectToWorld(obj_x, objTransformationMatrix)
    # obj_z = [0, 0, 1]
    # converted_obj_z = conv.objectToWorld(obj_z, objTransformationMatrix)
    # print(converted_obj_x , "should be: [0,0,-1]")
    # print(converted_obj_z, " should be: [1,0,0]")

    # # Rotate 90 around x, y will be z, z will be -y.
    # rotation = MatrixOps.rotate_matrix(90, [1, 0, 0])
    # objTransformationMatrix = rotation
    # obj_y = [0, 1, 0]
    # converted_obj_y = conv.objectToWorld(obj_y, objTransformationMatrix)
    # obj_z = [0, 0, 1]
    # converted_obj_z = conv.objectToWorld(obj_z, objTransformationMatrix)
    # print(converted_obj_y, " should be: [0, 0, 1]")
    # print(converted_obj_z, " should be: [0,-1,0]")
    #
    # translate = MatrixOps.translate_matrix(12, 6, 0)
    # rotation = MatrixOps.rotate_matrix(30, [0, 0, 1])
    # obj_trans = np.matmul(translate, rotation)
    # p = [3, 7, 0]
    # print(obj_trans)
    # print(conv.objectToWorld(p, obj_trans))
