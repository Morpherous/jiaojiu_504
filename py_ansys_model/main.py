import pyansys
import numpy as np
import pandas as pd
import matplotlib
import os

def set_shell():
    ansys.et(1, "SHELL281")
    ansys.keyopt(1, 1, 0)
    ansys.keyopt(1, 5, 0)
    ansys.keyopt(1, 8, 2)
    ansys.keyopt(1, 9, 0)
    ansys.keyopt(1, 10, 0)
    ansys.keyopt(1, 11, 0)
    print("set shell281 finished")


# 添加新材料
def add_new_material(mat_index, dens, exyz=[], gxyz=[], prxyz=[]):
    ansys.mptemp("", "", "", "", "", "", "")
    ansys.mptemp(1, 0)
    ansys.mpdata("EX", mat_index, "", exyz[0])
    ansys.mpdata("EY", mat_index, "", exyz[1])
    ansys.mpdata("EZ", mat_index, "", exyz[2])
    ansys.mpdata("GXY", mat_index, "", gxyz[0])
    ansys.mpdata("GYZ", mat_index, "", gxyz[1])
    ansys.mpdata("GXZ", mat_index, "", gxyz[2])
    ansys.mpdata("PRXY", mat_index, "", prxyz[0])
    ansys.mpdata("PRYZ", mat_index, "", prxyz[1])
    ansys.mpdata("PRXZ", mat_index, "", prxyz[2])
    ansys.mpdata("DENS", mat_index, "", dens)


# fc定义Tsai-Wu强度失效准则
def set_fc(mat_index, t_type, ten=[], cmp=[], xyz=[]):
    ansys.fc(mat_index, t_type, "xten", ten[0])
    ansys.fc(mat_index, t_type, "yten", ten[1])
    ansys.fc(mat_index, t_type, "zten", ten[2])
    ansys.fc(mat_index, t_type, "xcmp", cmp[0])
    ansys.fc(mat_index, t_type, "ycmp", cmp[1])
    ansys.fc(mat_index, t_type, "zcmp", cmp[2])
    ansys.fc(mat_index, t_type, "xy", xyz[0])
    ansys.fc(mat_index, t_type, "yz", xyz[1])
    ansys.fc(mat_index, t_type, "xz", xyz[2])


# TB定义最大应力准则
def set_tb(mat_index, ten=[]):
    ansys.tb("FAIL", 1)
    ansys.tbtemp("", "CRIT")
    ansys.tbtemp(mat_index, 0, 1, 0)  # 1指使用最大应力准则，0分别指不适用最大应变准则和Tasi-Wu失效准则
    ansys.tbtemp(0)
    ansys.tbdata(10, ten[0])  # 依次为x,y,z方向的抗拉强度，xy方向的剪切强度
    ansys.tbdata(12, ten[1])
    ansys.tbdata(13, ten[2])
    ansys.tbdata(14, ten[3])
    ansys.tbdata(16, ten[4])
    print("set tb finished")


def set_model_material():
    # 材料设置
    # 单轴向布UD
    add_new_material(1, 1.92e3, [3.95e10, 1.3234e10, 1.2044e10], [3.9e9, 3.17e9, 3.17e9], [0.234, 0.11, 0.11])
    set_fc(1, "s", [767, 20, 30], [-392, -70, -55], [41e6, 30e6, 41e6])
    set_fc(1, "epel", [0.05, 0.08, 0.04], [-0.045, -0.06, -0.045], [0.035, 0.042, 0.025])
    # set_tb(1,ten=[]):

    # 三轴向布
    add_new_material(2, 1.89e3, [2.8e10, 1.55e10, 1.0338e10], [6.2e9, 5.962e9, 5.96e9], [0.463, 0.398, 0.146])
    set_fc(2, "s", [767, 20, 30], [-392, -70, -55], [41e6, 30e6, 41e6])
    set_fc(2, "epel", [0.05, 0.08, 0.04], [-0.045, -0.06, -0.045], [0.035, 0.042, 0.025])

    # PVC
    add_new_material(3, 60, [3.5e7, 3.5e7, 3.5e7], [2.2e7, 1.5e7, 1.5e7], [0.3, 0.3, 0.3])
    set_fc(3, "s", [767, 20, 30], [-392, -70, -55], [41e6, 30e6, 41e6])
    set_fc(3, "epel", [0.05, 0.08, 0.04], [-0.045, -0.06, -0.045], [0.035, 0.042, 0.025])

    # 双轴向布
    add_new_material(4, 1.92e3, [1.25e10, 1.13e10, 1e10], [6e9, 6e9, 3.2e9], [0.626, 0.626, 0.14])
    set_fc(4, "s", [767, 20, 30], [-392, -70, -55], [41e6, 30e6, 41e6])
    set_fc(4, "epel", [0.05, 0.08, 0.04], [-0.045, -0.06, -0.045], [0.035, 0.042, 0.025])
    print("set model materials finished")


def create_model(path):
    # 画点
    cnt = 1
    for i in range(0, 94, 3):
        temppath = path + str(i) + ".csv"
        data = pd.read_csv(temppath)
        data.columns = ['Index', 'x', 'y', 'z']
        for j in range(0, data.shape[0], 50):
            x = data.iloc[j]['x']
            y = data.iloc[j]['y']
            z = data.iloc[j]['z']
            ansys.k(cnt, x, y, z)
            cnt += 1
    # 样条曲线连接
    for i in range(0, 32 * 20, 20):
        ansys.bsplin(i + 1, i + 2, i + 3, i + 4, i + 5, i + 6)
        ansys.bsplin(i + 6, i + 7)
        ansys.bsplin(i + 7, i + 8)
        ansys.bsplin(i + 8, i + 9, i + 10, i + 11)
        ansys.bsplin(i + 11, i + 12, i + 13, i + 14)
        ansys.bsplin(i + 14, i + 15)
        ansys.bsplin(i + 15, i + 16)
        ansys.bsplin(i + 16, i + 17, i + 18, i + 19, i + 20, i + 1)
    # 线连接成面，形成蒙皮
    ansys.allsel()
    ansys.get("LNUM", "LINE", 0, "NUM", "MAX")
    ansys.load_parameters()
    Lnum = int(ansys.parameters["LNUM"])
    for i in range(1, Lnum - 7, 8):
        for j in range(0, 8, 1):
            ansys.askin(i + j, i + j + 8)
    # 连接底面蒙皮
    # ansys.al(Lnum-7,Lnum-6,Lnum-5,Lnum-4,Lnum-3,Lnum-2,Lnum-1,Lnum)
    ansys.get("SK", "area", 0, "NUM", "MAX")
    ansys.load_parameters()
    wind_skin_area = int(ansys.parameters["SK"])
    print("wind_skin area is :", wind_skin_area)
    # 连接腹板
    for i in range(Lnum + 7 + 20, Lnum + 7 + 29 * 8, 8):
        ansys.askin(i, i + 4)
    print("create model finished")
    ansys.view(1,1,1,1)
    ansys.allsel()
    #ansys.aplot()
    return wind_skin_area


def set_mesh_model():
    ansys.allsel("all", "all")
    ansys.amesh("all")
    ansys.run("esel,s,,,all")
    ansys.run("ensym,,,,all")
    ansys.allsel()
    print("mesh model finished")


# 设置约束
def set_constraint():
    ansys.slashsolu()
    ansys.lsel("s", "loc", "z", 100)
    ansys.dl("all", "", "all")
    ansys.solve()
    print("set constraint finished")


# 获取模型质量
def get_model_weight():
    ansys.solu()
    ansys.antype(0)
    ansys.acel("", -9.8)
    ansys.allsel()
    ansys.run("solve")
    ansys.post1()
    ansys.fsum()
    ansys.get("weight", "fsum", 0, "item", "fy")
    ansys.load_parameters()
    weight = ansys.parameters['WEIGHT'] / 9.8
    ansys.finish()
    ansys.slashsolu()
    ansys.lsclear("INER")
    ansys.finish()
    return weight


def set_modal_analyse():
    ansys.slashsolu()
    ansys.antype(2)
    ansys.modopt("lanb", 10)
    ansys.mxpand(10, "", "", 0)
    ansys.allsel()
    ansys.solve()
    ansys.finish()
    # 获取模态分析图像和各阶频率
    ansys.post1()
    ansys.view(1, 1, 1, 1)
    freqs = []
    for modal_index in range(1, 11, 1):
        ansys.set(1, modal_index)
        ansys.pldisp(1)
        # 获取频率
        ansys.get("FREQ" + str(modal_index), "MODE", modal_index, "FREQ")
        ansys.load_parameters()
        freqs.append(ansys.parameters["FREQ" + str(modal_index)])
    ansys.finish()
    return freqs

def set_static_analyse():
    ansys.slashsolu()
    ansys.antype("static")
    ansys.ksel("s", "loc", "z", -8350)
    ansys.fk("ALL", "FY", -1000)
    ansys.allsel()
    ansys.solve()
    # 等效应变（位移）云图
    ansys.view(1, 1, 1, 1)
    ansys.post1()
    ansys.plnsol("u", "sum")
    # 等效应力云图
    ansys.view(1, 1)
    ansys.layer(0)
    ansys.plnsol("s", "eqv")
    # 返回最大应力和最大应变
    # 最大应力节点编号,imax/imin 输出最大/最小应力节点号，max/min输出最大/最小应力值
    ansys.post1()
    ansys.allsel()
    ansys.nsort("s", "eqv", 0, 0, "all")
    ansys.get("MAX_EQV_INDEX", "sort", 0, "imax")
    ansys.get("MAX_EQV_VALUE", "sort", 0, "max")
    ansys.get("MIN_EQV_VALUE", "sort", 0, "min")
    ansys.load_parameters()
    #print("MAX_EQV_INDEX is :", ansys.parameters["MAX_EQV_INDEX"])
    #print("MAX_EQV_VALUE is :", ansys.parameters["MAX_EQV_VALUE"])
    #print("MIN_EQV_VALUE is :", ansys.parameters["MIN_EQV_VALUE"])
    # 最大位移节点编号，imax/imin 输出最大/最小位移节点号，max/min输出最大/最小位移值
    #ansys.post1()
    ansys.nsort("u", "sum", 0, 0, "all")
    ansys.get("MAX_U_INDEX", "sort", 0, "imax")
    ansys.get("MAX_U_VALUE", "sort", 0, "max")
    ansys.get("MIN_U_VALUE", "sort", 0, "min")
    ansys.load_parameters()
    #print("MAX_U_INDEX is :", ansys.parameters["MAX_U_INDEX"])
    #print("MAX_U_VALUE is :", ansys.parameters["MAX_U_VALUE"])
    #print("MIN_U_VALUE is :", ansys.parameters["MIN_U_VALUE"])
    ansys.finish()
    return ansys.parameters["MAX_EQV_VALUE"],ansys.parameters["MAX_U_VALUE"]

def name_area(part_name, begin_num, end_num):
    ansys.asel("s", "area", "", begin_num, end_num)
    ansys.cm(part_name, "area")


def split_appearance(wind_skin_area):
    # 获取wind_skin和wind_rib面数目
    ansys.allsel()
    ansys.get("ALLA", "area", 0, "NUM", "MAX")
    ansys.load_parameters()
    all_area = int(ansys.parameters["ALLA"])
    name_area("wind_skin", 1, wind_skin_area)
    name_area("wind_rib", wind_skin_area + 1, all_area)



def set_sect():
    # 设定不同铺层截面
    ansys.sectype(1, "shell", "", "wind_skin")
    ansys.secdata(0.5, 1, 0.0, 3)
    ansys.secdata(0.5, 2, -30, 3)
    ansys.secdata(2, 2, 30, 3)
    ansys.secdata(2, 3, 45, 3)
    ansys.secdata(2, 3, -45, 3)
    ansys.secdata(2, 4, 0, 3)
    # ansys.secplot(1)

    ansys.sectype(2, "shell", "", "wind_rib")
    ansys.secdata(2, 1, 0.0, 3)
    ansys.secdata(2, 2, -30, 3)
    ansys.secdata(2, 2, 30, 3)
    ansys.secdata(2, 3, -45, 3)
    ansys.secdata(2, 3, 45, 3)
    # ansys.secplot(2)


path = "F:/ansys_program/windblade/ansys_model/"

ansys = pyansys.Mapdl(run_location=path, override=True,
                      interactive_plotting=True, loglevel="ERROR")

ansys.prep7()

set_shell()
set_model_material()
wind_skin_area = create_model("F:/ansys_program/windblade/origin_key_csv/")
split_appearance(wind_skin_area)
set_sect()
set_mesh_model()

ansys.finish()

set_constraint()
weight = get_model_weight()
print("weight: ",weight)
freqs = set_modal_analyse()
print("freqs: ",freqs)
max_eqv,max_u = set_static_analyse()
print("max_eqv: ",max_eqv)
print("max_u: ",max_u)
ansys.kill()
