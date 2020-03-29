import geatpy as ea
import numpy as np


class MyProblem(ea.Problem):
    def __init__(self, ansys):
        self.ansys = ansys
        name = "BNH"
        M = 3  # 目标维数，重量，应力，应变
        maxormins = [1] * M  # 1最小化，-1最大化
        Dim = 26  # 决策变量 总计12+12+1+1
        varTypes = [1] * Dim  # 0连续变量，1离散变量
        lb = [1, 1,
              3, 3, 8, 10, 12, 14, 15, 14, 13, 9, 7, 2,
              28, 27, 22, 17, 14, 13, 10, 10, 7, 5, 2, 2]  # 决策变量下界
        ub = [3, 3,  # 蒙皮、腹板
              5, 6, 15, 20, 25, 28, 30, 28, 25, 18, 15, 5,  # 主梁帽
              57, 55, 45, 35, 28, 25, 20, 20, 15, 10, 5, 4  # 加强层
              ]  # 决策变量上界
        lbin = [1] * Dim
        ubin = [1] * Dim
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb,
                            ub, lbin, ubin)

        def aimFunc(self, pop):
            Vars = pop.Phen
            temp_weight = []
            temp_max_eqv = []
            temp_max_u = []
            for i in range(Vars.shape[0]):
                wei, eqv, u, freqs = self.change_layer(Vars[i][:])
                temp_weight.append(wei)
                temp_max_eqv.append(eqv)
                temp_max_u.append(u)
            weight = np.array(temp_weight)
            weight = weight.reshape((-1, 1))

            max_eqv = np.array(temp_max_eqv)
            max_eqv = max_eqv.reshape((-1, 1))

            max_u = np.array(temp_max_u)
            max_u = max_u.reshape((-1, 1))
            # 优化目标
            pop.ObjV = np.hstack([weight, max_eqv, max_u])
            # 限制条件
            x = []
            for i in range(1, 27):
                x.append(Vars[:, [i]])
            tempvalue = 12
            pop.CV = np.hstack([
                # x16 - x15, x17 - x16, x18 - x17, x19 - x18, x20 - x19, x21 - x20,
                # x22 - x21, x23 - x22, x24 - x23, x25 - x24, x26 - x25,  # 加强层限制
                # x3 - x4, x4 - x5, x5 - x6, x6 - x7, x7 - x8, x8 - x9,
                # x10 - x9, x11 - x10, x12 - x11, x13 - x12, x14 - x13,  # 腹板限制
                # np.abs(x4 + x16 - (x3 + x15)) - tempvalue,
                # np.abs(x5 + x17 - (x4 + x16)) - tempvalue,
                # np.abs(x6 + x18 - (x5 + x17)) - tempvalue,
                # np.abs(x7 + x19 - (x6 + x18)) - tempvalue,
                # np.abs(x8 + x20 - (x7 + x19)) - tempvalue,
                # np.abs(x9 + x21 - (x8 + x20)) - tempvalue,
                # np.abs(x10 + x22 - (x9 + x21)) - tempvalue,
                # np.abs(x11 + x23 - (x10 + x22)) - tempvalue,
                # np.abs(x12 + x24 - (x11 + x23)) - tempvalue,
                # np.abs(x13 + x24 - (x12 + x24)) - tempvalue,
                # np.abs(x14 + x25 - (x13 + x24)) - tempvalue,
                # np.abs(x25 - x26) - tempvalue,  # 总层数梯度约束
                # weight - 2200,  # 最大重量约束
                # 900 - weight,  # 最小重量约束
                # x3 - x4, x7 - x8, x12 - x11,  # 主梁帽限制
            ])


class NSGA2_ANSYS():
    def __init__(self, myproblem, Encoding, NIND, MAXGEN, Drawing):
        self.Encoding = Encoding
        self.NIND = NIND
        self.MAXGEN = MAXGEN
        self.Drawing = Drawing
        self.myproblem = myproblem

    def run_nsga(self):
        Field = ea.crtfld(self.Encoding, self.myproblem.varTypes,
                          self.myproblem.ranges, self.myproblem.borders)
        population = ea.Population(self.Encoding, Field, self.NIND)
        myAlgorithm = ea.moea_NSGA2_templet(self.myproblem, population)
        myAlgorithm.MAXGEN = self.MAXGEN  # 最大遗传代数
        myAlgorithm.drawing = self.Drawing  # 设置绘图方式

        NDSet = myAlgorithm.run()
        NDSet.save()
        print('用时：%f 秒' % (myAlgorithm.passTime))
        print('评价次数：%d 次' % (myAlgorithm.evalsNum))
        print('非支配个体数：%d 个' % (NDSet.sizes))
        # 算法模板里面采用了“遗忘策略”，对于约束优化会让实际进化代数比设定值更多，
        # 从而让评价次数比预期的高。如果要与预期一样，
        # 需要删去Algorithm.py文件中的105-118行中的条件语句，即取消“遗忘策略”。
