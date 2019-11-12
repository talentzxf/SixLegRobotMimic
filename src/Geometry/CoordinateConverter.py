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
        print(point_vector)
        target_matrix = np.matmul(objTransformationMatrix, point_vector)
        target_point = np.asarray(target_matrix[0:3, :]).flatten().tolist()
        return target_point


# unit tests
if __name__ == '__main__':
    import unittest
    import MatrixOps

    conv = CoordinateConverter()
    rotation = MatrixOps.rotate_matrix(45, [0, 0, 1])
    transformation = MatrixOps.translate_matrix(1, 1, 0)
    objTransformationMatrix = np.matmul(transformation, rotation)
    origin = [0, 0, 0]
    converted_origin = conv.worldToObject(origin, objTransformationMatrix)
    print(converted_origin)

