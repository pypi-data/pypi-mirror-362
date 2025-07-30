import numpy as np
from scipy.spatial.transform import Rotation as R


class Pose:
    x: float
    y: float
    z: float
    qx: float
    qy: float
    qz: float
    qw: float

    def __init__(self, translation, quat):
        self.x, self.y, self.z = translation
        self.qx, self.qy, self.qz, self.qw = quat

    def get_euler(self, seq="xyz", degrees=False):
        return R.from_quat([self.qx, self.qy, self.qz, self.qw]).as_euler(
            seq=seq, degrees=degrees
        )

    @property
    def rot_matrix(self):
        return R.from_quat([self.qx, self.qy, self.qz, self.qw]).as_matrix()

    @property
    def homogeneous_matrix(self):
        """返回齐次矩阵"""
        homogeneous_matrix = np.eye(4)
        homogeneous_matrix[:3, :3] = self.rot_matrix
        homogeneous_matrix[:3, 3] = [self.x, self.y, self.z]
        return homogeneous_matrix

    @property
    def translation(self):
        return np.array([self.x, self.y, self.z])

    @property
    def quaternion(self):
        return np.array([self.qx, self.qy, self.qz, self.qw])

    @staticmethod
    def from_homogeneous_matrix(matrix: np.ndarray) -> "Pose":
        """齐次矩阵构建Pose

        Args:
            matrix (np.ndarray): 齐次矩阵

        Returns:
            Pose: 位姿
        """
        translation = matrix[:3, 3]
        quat = R.from_matrix(matrix[:3, :3]).as_quat()

        return Pose(translation=translation, quat=quat)

    def __matmul__(self, other: "Pose") -> "Pose":
        """
        支持 Pose2 @ Pose2 左乘操作
        等价于: self.homogeneous_matrix @ other.homogeneous_matrix
        """
        if not isinstance(other, Pose):
            raise TypeError("只能将 Pose2 左乘另一个 Pose2")
        new_matrix = self.homogeneous_matrix @ other.homogeneous_matrix
        return Pose.from_homogeneous_matrix(new_matrix)
