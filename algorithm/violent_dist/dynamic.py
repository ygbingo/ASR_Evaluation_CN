"""
使用动态规划计算
"""
import numpy as np

class DPMinEditDistance():

    def __init__(self, A, B):
        self.A = "#" + A  # 在A和B的头部添加“#”的目的，是占一个位置，用来表示一个“相同的开始”，
        # 即二者在最开始的位置是相等的，编辑代价是0，后面在这个基础上累计
        self.B = "#" + B
        self.A_len = len(self.A)
        self.B_len = len(self.B)
        # ，用这个值做标记
        self.edit_path_list = []  # 用来收集所有可行的编辑方案。这里将每个编辑方案看做一个路径。这样有利于后面理解动态规划算法的”状态“

        # 初始化编辑路径得分矩阵
        self.step_matrix = np.zeros((self.A_len, self.B_len))
        for i in range(self.A_len): self.step_matrix[i, 0] = i  # 这一列相当于将A的字符全部删除
        for i in range(self.B_len): self.step_matrix[0, i] = i  # 这一列相当于把B的字符串全部、依次添加到A的末尾

    def fit(self):
        for i in range(1, self.A_len):
            for j in range(1, self.B_len):
                self.step_matrix[i, j] = self.d_i_j(self.step_matrix, i, j)  # 使用状态更新公式计算到达每一个为指导的代价
        print(self.step_matrix)

        # 回溯得到最佳编辑方案
        index_A, index_B = self.A_len - 1, self.B_len - 1
        best_edit_path = []
        print("最小编辑距离是", self.step_matrix[index_A, index_B])
        while index_A > 0 and index_B > 0:
            best_cost = -1
            best_edit = None
            if index_A - 1 > -1:
                if self.step_matrix[index_A - 1, index_B] < best_cost or best_cost == -1:
                    best_cost = self.step_matrix[index_A - 1, index_B]
                    best_edit = 'add'
            if index_B - 1 > -1:
                if self.step_matrix[index_A, index_B - 1] < best_cost or best_cost == -1:
                    best_cost = self.step_matrix[index_A, index_B - 1]
                    best_edit = 'del'
            if index_A - 1 > -1 and index_B - 1 > -1:
                if self.step_matrix[index_A - 1, index_B - 1] < best_cost or best_cost == -1:
                    best_cost = self.step_matrix[index_A - 1, index_B]
                    best_edit = 'rep'

                if self.step_matrix[index_A - 1, index_B - 1] < self.step_matrix[index_A, index_B] \
                        or best_cost == -1:
                    best_cost = self.step_matrix[index_A - 1, index_B]
                    best_edit = 'keep'
            if best_edit in ["keep", 'rep']:
                index_A -= 1
                index_B -= 1
            if best_edit == "del":
                index_B -= 1
            if best_edit == "add":
                index_A -= 1
            best_edit_path = [best_edit] + best_edit_path
            print(index_A, index_B, best_edit)
        print("最佳编辑路径是", best_edit_path)

        # 计算到达当前状态的最佳路径，对应的总代价

    def d_i_j(self, step_matrix, i, j):
        c1 = step_matrix[i - 1, j] + 1
        c2 = step_matrix[i, j - 1] + 1
        c3 = step_matrix[i - 1, j - 1] + 1
        if self.A[i] == self.B[j]:
            c3 = step_matrix[i - 1, j - 1]
        min_c = min(c1, c2, c3)
        return min_c


if __name__ == '__main__':
    s1 = "小猪饿了"
    s2 = "小懒猪饿了"

    DP_version = DPMinEditDistance(s1, s2)
    DP_version.fit()
