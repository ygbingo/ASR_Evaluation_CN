"""
使用穷举的方式计算利文斯顿距离
"""


class ViolentMinEditDistance_v1():
    # 枚举所有可行的编辑方案，然后逐一计算代价，最后求最小代价
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

        self.edit_cost_map = {"del": 1, "add": 1, "rep": 2, "keep": 0}
        self.min_edit_distance = -1
        self.best_path = ""

    def cal_score(self, path):
        score = 0
        for edit in path:
            score += self.edit_cost_map[edit]
        return score

    def fit(self):
        self.min_edit_distance_violent(self.ori_A, 0, [])
        for path in self.edit_path_list:
            score = self.cal_score(path)
            print(path, score)  # 展示每个编辑路径的内容和得分
            if score < self.min_edit_distance or self.min_edit_distance == -1:
                self.min_edit_distance = score
                self.best_path = path
        print("最小编辑距离是", self.min_edit_distance, self.best_path)

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

    def min_edit_distance_violent(self, latest_A, edit_depth, this_path):
        if latest_A == self.ori_B:
            self.edit_path_list.append(this_path)
            return
        elif edit_depth >= self.len_ori_B:
            return
        else:
            if edit_depth >= len(latest_A):  # 如果当前编辑位置超出原始A，无法使用替换或者删除操作，只能添加B对应位置的字符。这是A短于B的情况
                self.min_edit_distance_violent(self.add_char(latest_A, edit_depth, self.ori_B[edit_depth]), edit_depth + 1, this_path + ['add'])
            elif edit_depth >= self.len_ori_B:  # 如果当前编辑位置超出原始A，无法使用替换或者删除操作，只能添加B对应位置的字符。这是A短于B的情况
                self.min_edit_distance_violent(self.delete_char(latest_A, edit_depth, self.ori_B[edit_depth]), edit_depth + 1, this_path + ['del'])
            else:
                # 删除
                self.min_edit_distance_violent(self.delete_char(latest_A, edit_depth), edit_depth + 1, this_path + ['del'])
                # 添加
                self.min_edit_distance_violent(self.add_char(latest_A, edit_depth, self.ori_B[edit_depth]), edit_depth + 1, this_path + ['add'])
                # 替换
                #                 print(edit_depth, len(latest_A))
                if latest_A[edit_depth] == self.ori_B[edit_depth]:  # 如果这个位置上，A和B的字符相同，就不用替换了
                    self.min_edit_distance_violent(latest_A, edit_depth + 1, this_path + ["keep"])
                else:  # 如果不同，还是需要替换
                    self.min_edit_distance_violent(self.repalce_char(latest_A, edit_depth, self.ori_B[edit_depth]), edit_depth + 1, this_path + ['rep'])
            return


if __name__ == '__main__':
    s1 = "小猪饿了"
    s2 = "小懒猪饿了"
    vilent_v1 = ViolentMinEditDistance_v1(s1, s2)
    vilent_v1.fit()
