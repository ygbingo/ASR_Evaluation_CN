"""
用递归法计算利文斯顿距离
"""
class ViolentMinEditDistance_v2():
    # 在递归的过程中，每一次编辑，顺便基于当前路径的累计代价，计算到达这一步的代价。相比v1版本，这里避免了大量的重复计算
    def __init__(self, A, B):
        if len(B) < len(A):  # 为了后面计算简单，这里假设A比B要短
            self.ori_B = A
            self.ori_A = B
        else:
            self.ori_A = A
            self.ori_B = B
        self.len_ori_B = len(B)
        # ，用这个值做标记
        self.edit_path_list = []  # 用来收集所有可行的编辑方案。这里将每个编辑方案看做一个路径。这样有利于后面理解动态规划算法的”状态“

        self.min_edit_distance = -1  # -1表示还没有初始化
        self.best_path = None

    def fit(self):
        self.min_edit_distance_violent(self.ori_A, 0, [], 0)
        for path, score in self.edit_path_list:
            print(path, score)  # 展示每个编辑路径的内容和得分
            if score < self.min_edit_distance or self.min_edit_distance == -1:
                self.min_edit_distance = score
                self.best_path = path
        print("最小编辑距离是", self.min_edit_distance, self.best_path, "可选的路径数量是", len(self.edit_path_list))

    # 删除一个字符串的指定位置的字符
    def delete_char(self, a_str, index):
        return a_str[:index] + a_str[index + 1:]

        # 在字符串的指定位置添加一个字符

    def add_char(self, a_str, index, new_char):
        return a_str[:index] + new_char + a_str[index:]

        # 将字符串指定位置的一个字符，替换为另一个字符

    def repalce_char(self, a_str, index, new_char):
        return a_str[:index] + new_char + a_str[index + 1:]

        # 使用递归的方式生成所有的编辑序列，然后遍历、计算代价，求出最小代价作为最小编辑距离

    def min_edit_distance_violent(self, latest_A, edit_depth, this_path, this_path_score):
        if latest_A == self.ori_B:
            self.edit_path_list.append([this_path, this_path_score])
            return
        elif edit_depth >= self.len_ori_B:
            return
        else:
            if edit_depth >= len(latest_A):  # 如果当前编辑位置超出原始A，无法使用替换或者删除操作，只能添加B对应位置的字符。这是A短于B的情况
                self.min_edit_distance_violent(self.add_char(latest_A, edit_depth, self.ori_B[edit_depth]), \
                                               edit_depth + 1, this_path + ['add'], this_path_score + 1)
            elif edit_depth >= self.len_ori_B:  # 如果当前编辑位置超出原始A，无法使用替换或者删除操作，只能添加B对应位置的字符。这是A短于B的情况
                self.min_edit_distance_violent(self.delete_char(latest_A, edit_depth, self.ori_B[edit_depth]), \
                                               edit_depth + 1, this_path + ['del'], this_path_score + 1)
            else:
                # 删除
                self.min_edit_distance_violent(self.delete_char(latest_A, edit_depth), \
                                               edit_depth + 1, this_path + ['del'], this_path_score + 1)
                # 添加
                self.min_edit_distance_violent(self.add_char(latest_A, edit_depth, self.ori_B[edit_depth]), \
                                               edit_depth + 1, this_path + ['add'], this_path_score + 1)
                # 替换
                #                 print(edit_depth, len(latest_A))
                if latest_A[edit_depth] == self.ori_B[edit_depth]:  # 如果这个位置上，A和B的字符相同，就不用替换了
                    self.min_edit_distance_violent(latest_A, edit_depth + 1, this_path + ["keep"], this_path_score)
                else:  # 如果不同，还是需要替换
                    self.min_edit_distance_violent(self.repalce_char(latest_A, edit_depth, self.ori_B[edit_depth]), \
                                                   edit_depth + 1, this_path + ['rep'], this_path_score + 2)
            return


if __name__ == '__main__':
    s1 = "小猪饿了"
    s2 = "小懒猪饿了"
    vilent_v2 = ViolentMinEditDistance_v2(s1, s2)
    vilent_v2.fit()
