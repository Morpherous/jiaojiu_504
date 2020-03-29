import pyansys
import numpy as np
import pandas as pd
import time
from pprint import pprint


class ANSYS_MODEL(object):
    def __init__(self, ansys, opt):
        self.ansys = ansys
        self.opt = opt

        self.pri_name = []
        self.skin_name = []
        self.all_weight = []
        self.all_eqv = []
        self.all_u = []

    def set_background(self):
        self.ansys.run("/rgb,index,100,100,100,0")
        self.ansys.run("/rgb,index,80,80,80,13")
        self.ansys.run("/rgb,index,60,60,60,14")
        self.ansys.run("/rgb,index,0,0,0,15")

    # 设置shell
    def set_shell(self):
        self.ansys.prep7()
        self.ansys.et(1, "SHELL181")
        self.ansys.keyopt(1, 1, 0)
        self.ansys.keyopt(1, 3, 0)
        self.ansys.keyopt(1, 5, 0)
        self.ansys.keyopt(1, 8, 2)
        self.ansys.keyopt(1, 9, 0)
        self.ansys.keyopt(1, 10, 0)
        self.ansys.keyopt(1, 11, 0)
        print("set shell181 finished")

    # 添加新材料
    def add_new_material(self, mat_index, dens, exyz, gxyz, prxyz):
        self.ansys.mptemp("", "", "", "", "", "", "")
        self.ansys.mptemp(1, 0)
        self.ansys.mpdata("EX", mat_index, "", exyz[0])
        self.ansys.mpdata("EY", mat_index, "", exyz[1])
        self.ansys.mpdata("EZ", mat_index, "", exyz[2])
        self.ansys.mpdata("GXY", mat_index, "", gxyz[0])
        self.ansys.mpdata("GYZ", mat_index, "", gxyz[1])
        self.ansys.mpdata("GXZ", mat_index, "", gxyz[2])
        self.ansys.mpdata("PRXY", mat_index, "", prxyz[0])
        self.ansys.mpdata("PRYZ", mat_index, "", prxyz[1])
        self.ansys.mpdata("PRXZ", mat_index, "", prxyz[2])
        self.ansys.mpdata("DENS", mat_index, "", dens * (1e-12))

    # fc定义Tsai-Wu强度失效准则
    def set_fc(self, mat_index, t_type, ten, cmp, xyz):
        self.ansys.fc(mat_index, t_type, "xten", ten[0])
        self.ansys.fc(mat_index, t_type, "yten", ten[1])
        self.ansys.fc(mat_index, t_type, "zten", ten[2])
        self.ansys.fc(mat_index, t_type, "xcmp", cmp[0])
        self.ansys.fc(mat_index, t_type, "ycmp", cmp[1])
        self.ansys.fc(mat_index, t_type, "zcmp", cmp[2])
        self.ansys.fc(mat_index, t_type, "xy", xyz[0])
        self.ansys.fc(mat_index, t_type, "yz", xyz[1])
        self.ansys.fc(mat_index, t_type, "xz", xyz[2])
        self.ansys.fc(mat_index, t_type, "xycp", -1)
        self.ansys.fc(mat_index, t_type, "yzcp", -1)
        self.ansys.fc(mat_index, t_type, "xzcp", -1)

    # TB定义最大应力准则
    def set_tb(self, mat_index, ten):
        self.ansys.tb("FAIL", 1)
        self.ansys.tbtemp("", "CRIT")
        self.ansys.tbtemp(mat_index, 0, 1, 0)  # 1指使用最大应力准则，0分别指不适用最大应变准则和Tasi-Wu失效准则
        self.ansys.tbtemp(0)
        self.ansys.tbdata(10, ten[0])  # 依次为x,y,z方向的抗拉强度，xy方向的剪切强度
        self.ansys.tbdata(12, ten[1])
        self.ansys.tbdata(13, ten[2])
        self.ansys.tbdata(14, ten[3])
        self.ansys.tbdata(16, ten[4])
        print("set tb finished")

    # 材料参数设置
    def set_model_material(self):
        # 单轴向布UD
        self.add_new_material(
            1, 1.92e3, [
                3.95e4, 1.3234e4, 1.2044e4], [
                3.9e4, 3.17e4, 3.17e4], [
                0.234, 0.11, 0.11])
        # 三轴向布
        self.add_new_material(
            2, 1.89e3, [
                2.8e4, 1.55e4, 1.0338e4], [
                6.2e4, 5.962e4, 5.96e4], [
                0.463, 0.398, 0.146])
        # PVC
        self.add_new_material(
            3, 60, [
                35, 35, 35], [
                22, 15, 15], [
                0.3, 0.3, 0.3])
        # 双轴向布
        self.add_new_material(
            4, 1.92e3, [
                1.25e4, 1.13e4, 1e4], [
                6e3, 6e3, 3.2e3], [
                0.626, 0.626, 0.14])

    print("set model materials finished")

    def create_model(self, path):
        # 画点
        cnt = 1
        for i in range(1, 47, 1):
            temppath = path + str(i) + ".csv"
            data = pd.read_csv(temppath)
            data.columns = ['Index', 'x', 'y', 'z']
            for j in range(0, data.shape[0], 50):
                x = data.iloc[j]['x']
                y = data.iloc[j]['y']
                z = data.iloc[j]['z']
                self.ansys.k(cnt, x, y, z)
                cnt += 1
        self.ansys.view(1, 1, 1, 1)
        self.ansys.allsel()
        if self.opt.plot_use:
            self.ansys.kplot()
        # 样条曲线连接
        for i in range(0, 46 * 20, 20):
            self.ansys.bsplin(i + 1, i + 2, i + 3, i + 4, i + 5, )
            self.ansys.bsplin(i + 5, i + 6, i + 7)
            self.ansys.bsplin(i + 7, i + 8)
            self.ansys.bsplin(i + 8, i + 9, i + 10, i + 11)
            self.ansys.bsplin(i + 11, i + 12, i + 13, i + 14)
            self.ansys.bsplin(i + 14, i + 15)
            self.ansys.bsplin(i + 15, i + 16, i + 17)
            self.ansys.bsplin(i + 17, i + 18, i + 19, i + 20, i + 1)
        if self.opt.plot_use:
            self.ansys.lplot()
        # 线连接成面，形成蒙皮
        self.ansys.allsel()
        self.ansys.get("LNUM", "LINE", 0, "NUM", "MAX")
        self.ansys.load_parameters()
        Lnum = int(self.ansys.parameters["LNUM"])
        for i in range(1, Lnum - 7, 8):
            for j in range(0, 8, 1):
                self.ansys.askin(i + j, i + j + 8)
        if self.opt.plot_use:
            self.ansys.aplot()
        self.ansys.get("SK", "area", 0, "NUM", "MAX")
        self.ansys.load_parameters()
        wind_skin_area = int(self.ansys.parameters["SK"])
        print("wind_skin area is :", wind_skin_area)
        # 连接腹板 44是最后一个腹板
        for i in range(Lnum + 11, Lnum + 7 + 31 * 8, 8):
            self.ansys.askin(i, i + 4)
        print("Create model finished")
        # 转换角度
        self.ansys.view(1, 1, 1, 1)
        self.ansys.allsel()
        if self.opt.plot_use:
            self.ansys.aplot()
        return wind_skin_area

    # 划分网格并反向
    def mesh_all(self):
        self.ansys.prep7()
        self.ansys.allsel()
        self.ansys.amesh("all")
        self.ansys.esel("s", "", "", "all")
        self.ansys.ensym("", "", "", "all")
        print("Mesh model finished")

    # 设置约束
    def set_constraint(self):
        self.ansys.slashsolu()
        self.ansys.lsel("s", "loc", "z", 0)
        self.ansys.dl("all", "", "all")
        self.ansys.solve()
        print("Set constraint finished")

    # 获取模型质量
    def get_model_weight(self):
        self.ansys.slashsolu()
        self.ansys.antype(0)
        self.ansys.acel("", -9800)
        self.ansys.allsel()
        self.ansys.solve()
        self.ansys.post1()
        self.ansys.fsum()
        self.ansys.get("weight", "fsum", 0, "item", "fy")
        self.ansys.load_parameters()
        weight = self.ansys.parameters['WEIGHT'] / 9800
        self.ansys.finish()
        self.ansys.slashsolu()
        self.ansys.lsclear("INER")
        self.ansys.finish()
        print("Calculate weight finished")
        return weight

    # 模态分析
    def set_modal_analyse(self):
        self.ansys.slashsolu()
        self.ansys.antype(2)
        self.ansys.modopt("lanb", 10)
        self.ansys.mxpand(10, "", "", 0)
        self.ansys.allsel()
        self.ansys.solve()
        self.ansys.finish()
        # 获取模态分析图像和各阶频率
        self.ansys.post1()
        self.ansys.view(1, 1, 1, 1)
        freqs = []
        for modal_index in range(1, 11, 1):
            self.ansys.set(1, modal_index)
            if self.opt.plot_use:
                self.ansys.pldisp(1)
            # 获取频率
            self.ansys.get("FREQ" + str(modal_index), "MODE", modal_index, "FREQ")
            self.ansys.load_parameters()
            freqs.append(self.ansys.parameters["FREQ" + str(modal_index)])
        self.ansys.finish()
        print("Modal analyse finished")
        return freqs

    # 静力分析
    def set_static_analyse(self):
        self.ansys.slashsolu()
        self.ansys.antype("static")
        self.ansys.ksel("s", "loc", "z", -7200)
        self.ansys.fk("ALL", "FY", -8342.361)  # 1203.1e3/7.2/20=8342.361N
        self.ansys.allsel()
        self.ansys.solve()
        # 等效应变（位移）云图
        self.ansys.view(1, 1, 1, 1)
        self.ansys.post1()
        self.ansys.plnsol("u", "sum")
        # 等效应力云图
        self.ansys.view(1, 1)
        self.ansys.layer(0)
        self.ansys.plnsol("s", "eqv")
        # 返回最大应力和最大应变
        # 最大应力节点编号,imax/imin 输出最大/最小应力节点号，max/min输出最大/最小应力值
        self.ansys.post1()
        self.ansys.allsel()
        self.ansys.nsort("s", "eqv", 0, 0, "all")
        self.ansys.get("MAX_EQV_INDEX", "sort", 0, "imax")
        self.ansys.get("MAX_EQV_VALUE", "sort", 0, "max")
        self.ansys.get("MIN_EQV_VALUE", "sort", 0, "min")
        self.ansys.load_parameters()
        print("MAX_EQV_INDEX is :", self.ansys.parameters["MAX_EQV_INDEX"])
        print("MAX_EQV_VALUE is :", self.ansys.parameters["MAX_EQV_VALUE"])
        print("MIN_EQV_VALUE is :", self.ansys.parameters["MIN_EQV_VALUE"])
        # 最大位移节点编号，imax/imin 输出最大/最小位移节点号，max/min输出最大/最小位移值
        self.ansys.nsort("u", "sum", 0, 0, "all")
        self.ansys.get("MAX_U_INDEX", "sort", 0, "imax")
        self.ansys.get("MAX_U_VALUE", "sort", 0, "max")
        self.ansys.get("MIN_U_VALUE", "sort", 0, "min")
        self.ansys.load_parameters()
        print("MAX_U_INDEX is :", self.ansys.parameters["MAX_U_INDEX"])
        print("MAX_U_VALUE is :", self.ansys.parameters["MAX_U_VALUE"])
        print("MIN_U_VALUE is :", self.ansys.parameters["MIN_U_VALUE"])
        self.ansys.finish()
        print("Static analyse finished")
        return self.ansys.parameters["MAX_EQV_VALUE"], self.ansys.parameters["MAX_U_VALUE"]

    # 叶片分块命名
    def add_part_appearance(self, part_name, area_part):
        self.ansys.asel("s", "area", "", area_part[0])
        for i in range(1, len(area_part)):
            self.ansys.asel("a", "area", "", area_part[i])
        self.ansys.cm(part_name, "area")
        self.ansys.cmsel("s", part_name)
        if self.opt.plot_use:
            self.ansys.aplot()

    def split_appearance(self):
        self.opt.primary_index = 1
        # 主梁分块定义
        self.add_part_appearance("pri_" + str(self.opt.primary_index), [10, 11, 14, 15])
        self.pri_name.append("pri_" + str(self.opt.primary_index))
        self.opt.primary_index += 1

        self.add_part_appearance("pri_" + str(self.opt.primary_index), [18, 19, 22, 23])
        self.pri_name.append("pri_" + str(self.opt.primary_index))
        self.opt.primary_index += 1

        self.add_part_appearance("pri_" + str(self.opt.primary_index),
                                 [26, 27, 34, 35, 30, 31, 38, 39])
        self.pri_name.append("pri_" + str(self.opt.primary_index))
        self.opt.primary_index += 1

        self.add_part_appearance("pri_" + str(self.opt.primary_index),
                                 [42, 43, 46, 47, 50, 51, 54, 55])
        self.pri_name.append("pri_" + str(self.opt.primary_index))
        self.opt.primary_index += 1

        self.add_part_appearance("pri_" + str(self.opt.primary_index),
                                 [58, 59, 62, 63, 66, 67, 70, 71])
        self.pri_name.append("pri_" + str(self.opt.primary_index))
        self.opt.primary_index += 1

        self.add_part_appearance("pri_" + str(self.opt.primary_index),
                                 [74, 75, 78, 79, 82, 83, 86, 87])
        self.pri_name.append("pri_" + str(self.opt.primary_index))
        self.opt.primary_index += 1

        self.add_part_appearance("pri_" + str(self.opt.primary_index),
                                 [90, 91, 94, 95, 98, 99, 102, 103])
        self.pri_name.append("pri_" + str(self.opt.primary_index))
        self.opt.primary_index += 1

        p = []
        for i in range(106, 227, 8):
            p.append(i)
            p.append(i + 1)
            p.append(i + 4)
            p.append(i + 5)
        self.add_part_appearance("pri_" + str(self.opt.primary_index), p)
        self.pri_name.append("pri_" + str(self.opt.primary_index))
        self.opt.primary_index += 1

        self.add_part_appearance("pri_" + str(self.opt.primary_index), [234, 235, 238, 239])
        self.pri_name.append("pri_" + str(self.opt.primary_index))
        self.opt.primary_index += 1

        self.add_part_appearance("pri_" + str(self.opt.primary_index), [242, 243, 246, 247])
        self.pri_name.append("pri_" + str(self.opt.primary_index))
        self.opt.primary_index += 1

        self.add_part_appearance("pri_" + str(self.opt.primary_index), [250, 251, 254, 255])
        self.pri_name.append("pri_" + str(self.opt.primary_index))
        self.opt.primary_index += 1

        self.add_part_appearance("pri_" + str(self.opt.primary_index),
                                 [258, 259, 262, 263, 266, 267, 270, 271])
        self.pri_name.append("pri_" + str(self.opt.primary_index))
        self.opt.primary_index += 1

        self.add_part_appearance("pri_" + str(self.opt.primary_index),
                                 [274, 275, 278, 279, 282, 283, 286, 287])
        self.pri_name.append("pri_" + str(self.opt.primary_index))
        self.opt.primary_index += 1

        self.add_part_appearance("pri_" + str(self.opt.primary_index),
                                 [290, 291, 294, 295, 298, 299, 302, 303])
        self.pri_name.append("pri_" + str(self.opt.primary_index))
        self.opt.primary_index += 1

        self.add_part_appearance("pri_" + str(self.opt.primary_index),
                                 [306, 307, 310, 311, 314, 315, 318, 319])
        self.pri_name.append("pri_" + str(self.opt.primary_index))

        # 叶片除主梁之外的分割块
        skin_index = 1
        self.add_part_appearance("skin_" + str(skin_index), [i for i in range(1, 9, 1)])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index), [9, 12, 13, 16])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index), [17, 20, 21, 24])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index),
                                 [25, 28, 29, 32, 33, 36, 37, 40])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index),
                                 [41, 44, 45, 48, 49, 52, 53, 56])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index),
                                 [57, 60, 61, 64, 65, 68, 69, 72])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index),
                                 [73, 76, 77, 80, 81, 84, 85, 88])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index),
                                 [89, 92, 93, 96, 97, 100, 101, 104])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        sk = []
        for i in range(105, 226, 8):
            sk.append(i)
            sk.append(i + 3)
            sk.append(i + 4)
            sk.append(i + 7)
        self.add_part_appearance("skin_" + str(skin_index), sk)
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index), [233, 236, 237, 240])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index), [241, 244, 245, 248])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index), [249, 252, 253, 256])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index),
                                 [257, 260, 261, 264, 265, 268, 269, 272])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index),
                                 [273, 276, 277, 280, 281, 284, 285, 288])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index),
                                 [289, 292, 293, 296, 297, 300, 301, 304])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index),
                                 [305, 308, 309, 312, 313, 316, 317, 320])
        self.skin_name.append("skin_" + str(skin_index))
        skin_index += 1

        self.add_part_appearance("skin_" + str(skin_index),
                                 [i for i in range(321, 361, 1)])
        self.skin_name.append("skin_" + str(skin_index))

        # 分离rib腹板面
        self.ansys.allsel()
        self.ansys.get("ALLA", "area", 0, "NUM", "MAX")
        self.ansys.load_parameters()
        all_area = int(self.ansys.parameters["ALLA"])
        self.add_part_appearance("rib", [i for i in range(361, all_area + 1)])
        print("wind_skin_area + wind_rib_area = ", all_area)
        print("Split appearance to rib/skin/primary finished")
        return self.pri_name, self.skin_name

    # 铺多层材料
    def pave_layer(self, thickness, mat_index, angle, layers):
        if layers > 0:
            for i in range(layers):
                self.ansys.secdata(thickness, mat_index, angle, 3)

    # 单个截面铺层顺序：外蒙皮、加强层、主梁帽、内蒙皮
    def pave_sect(self, sec_index, sec_name, skin, pri, meng):
        self.ansys.sectype(sec_index, "shell", "", sec_name)
        # 内蒙皮
        self.pave_layer(0.8, 2, 45, meng)
        # 主梁帽
        self.pave_layer(0.53, 1, 0, pri)
        # 加强层
        self.pave_layer(0.8, 2, 45, skin)
        # 外蒙皮
        self.pave_layer(0.8, 2, 45, meng)
        self.ansys.secoffset("TOP")
        # print(sec_name)
        # self.ansys.secplot(sec_index)
        self.ansys.cmsel("s", sec_name)
        if self.opt.plot_use:
            self.ansys.aplot()
        self.ansys.aatt(1, "", 1, 0, sec_index)
        return sec_index + 1

    # 叶片分截面铺层
    def set_section(self, meng, rib, primary_layer, skin_layer):
        self.ansys.prep7()
        sec_index = 1
        # skin 主梁帽之外的部分
        sec_index = self.pave_sect(sec_index, "skin_1", skin_layer[0], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_2", skin_layer[0], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_3", skin_layer[0], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_4", skin_layer[1], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_5", skin_layer[2], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_6", skin_layer[3], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_7", skin_layer[4], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_8", skin_layer[5], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_9", skin_layer[6], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_10", skin_layer[7], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_11", skin_layer[8], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_12", skin_layer[8], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_13", skin_layer[9], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_14", skin_layer[9], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_15", skin_layer[10], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_16", skin_layer[10], 0, meng[0])
        sec_index = self.pave_sect(sec_index, "skin_17", skin_layer[11], 0, meng[0])
        # 主梁帽部分
        sec_index = self.pave_sect(
            sec_index,
            "pri_1",
            skin_layer[0],
            primary_layer[0],
            meng[0])
        sec_index = self.pave_sect(
            sec_index,
            "pri_2",
            skin_layer[0],
            primary_layer[0],
            meng[0])
        sec_index = self.pave_sect(
            sec_index,
            "pri_3",
            skin_layer[1],
            primary_layer[1],
            meng[0])
        sec_index = self.pave_sect(
            sec_index,
            "pri_4",
            skin_layer[2],
            primary_layer[2],
            meng[0])
        sec_index = self.pave_sect(
            sec_index,
            "pri_5",
            skin_layer[3],
            primary_layer[3],
            meng[0])
        sec_index = self.pave_sect(
            sec_index,
            "pri_6",
            skin_layer[4],
            primary_layer[4],
            meng[0])
        sec_index = self.pave_sect(
            sec_index,
            "pri_7",
            skin_layer[5],
            primary_layer[5],
            meng[0])
        sec_index = self.pave_sect(
            sec_index,
            "pri_8",
            skin_layer[6],
            primary_layer[6],
            meng[0])
        sec_index = self.pave_sect(
            sec_index,
            "pri_9",
            skin_layer[7],
            primary_layer[7],
            meng[0])
        sec_index = self.pave_sect(
            sec_index,
            "pri_10",
            skin_layer[8],
            primary_layer[8],
            meng[0])
        sec_index = self.pave_sect(
            sec_index,
            "pri_11",
            skin_layer[8],
            primary_layer[8],
            meng[0])
        sec_index = self.pave_sect(
            sec_index,
            "pri_12",
            skin_layer[9],
            primary_layer[9],
            meng[0])
        sec_index = self.pave_sect(
            sec_index,
            "pri_13",
            skin_layer[9],
            primary_layer[10],
            meng[0])
        sec_index = self.pave_sect(
            sec_index,
            "pri_14",
            skin_layer[10],
            primary_layer[11],
            meng[0])
        sec_index = self.pave_sect(
            sec_index,
            "pri_15",
            skin_layer[10],
            primary_layer[11],
            meng[0])
        # 腹板
        self.ansys.sectype(sec_index, "shell", "", "rib")
        self.pave_layer(0.61, 4, 45, rib[0])
        self.ansys.secdata(40, 3, 0, 3)  # PVC是各向同性材料，角度随便设置即可
        self.pave_layer(0.61, 4, 45, rib[0])
        self.ansys.secoffset("MID")
        print("Pave blade finished")

    # 清除铺层数据和所有载荷数据
    def clear_mesh_load(self):
        self.ansys.prep7()
        self.ansys.aclear("all")
        self.ansys.lsclear("all")
        print("Clear mesh and load")

    # 修改铺层层数
    def change_layer(self, variables):
        variables = [int(i) for i in variables]
        self.clear_mesh_load()
        self.set_section(variables[:1], variables[1:2], variables[2:14], variables[14:])
        self.mesh_all()
        self.ansys.finish()
        self.set_constraint()
        weight = self.get_model_weight()
        print("Model weight: %.5f kg" % (weight * 1000))
        freqs = self.set_modal_analyse()
        print("Ten modal freqs: ", freqs)
        max_eqv, max_u = self.set_static_analyse()
        print("Max_eqv is %f,Max_u is %f" % (max_eqv, max_u))
        print("------------------------------------------------------------")
        print("Change layer finished,self.ansys has run %d times" % (self.opt.ansys_time))
        runtime = time.time() - self.opt.start_time
        print(
            "Run time is %d h %d m %d s" %
            (runtime /
             3600,
             runtime %
             3600 /
             60,
             runtime %
             60))
        if self.opt.ansys_time % self.opt.NIND == 0:
            print("*****************************************************")
            print("NSGA has runned for %d times" % (self.opt.ansys_time / self.opt.NIND))
            print("*****************************************************")
        print("------------------------------------------------------------")
        self.opt.ansys_time += 1
        self.all_weight.append(weight)
        self.all_eqv.append(max_eqv)
        self.all_u.append(max_u)
        return weight, max_eqv, max_u, freqs

    def model(self):
        self.set_background()
        self.set_shell()
        self.set_model_material()
        _ = self.create_model(self.opt.root_path + '/useful_csv')
        _, _ = self.split_appearance()
