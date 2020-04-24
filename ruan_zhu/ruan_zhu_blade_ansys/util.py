import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Config import CONFIG
import time

'''
此函数用来确定主梁帽和腹板的位置，确定好关键点的序号后，在ANSYS_MODEL的create_model中修改连接点部分
默认为工字梁，主梁帽位置为0.15c到0.5c之间，腹板在主梁帽中间为0.325c处
'''


def getjiemian_linec(csv_path):
    df = pd.read_csv(csv_path)
    maxdis = 0
    index1, index2 = 0, 0
    for i in df.index:
        for j in df.index:
            if i == j:
                continue
            else:
                if (df.iloc[i].x - df.iloc[j].x) * (df.iloc[i].x - df.iloc[j].x) + (df.iloc[i].y - df.iloc[j].y) * (
                        df.iloc[i].y - df.iloc[j].y) > maxdis:
                    maxdis = (df.iloc[i].x - df.iloc[j].x) * (df.iloc[i].x - df.iloc[j].x) + (
                            df.iloc[i].y - df.iloc[j].y) * (df.iloc[i].y - df.iloc[j].y)
                    index1 = i
                    index2 = j
    print(index1, index2)

    def plot_linec(x1, y1, x2, y2, c, name):
        midx, midy = x1 - (x1 - x2) * c, y1 - (y1 - y2) * c
        tempk = (y1 - y2) * 1.0 / (x1 - x2)
        k = -1.0 / tempk
        print("k", k, tempk)
        b = midy - k * midx
        x = np.linspace(midx - 200, midx + 200)
        y = k * x + b
        plt.plot(x, y, label=name)
        plt.vlines(midx, -600, 500, label="v_" + name)

    fig, ax = plt.subplots()
    ax.scatter(df.x, df.y)
    for i, indexnum in enumerate(range(len(df.x))):
        ax.annotate(indexnum + 1, (df.x[i], df.y[i]))
    plt.plot([df.iloc[index1].x, df.iloc[index2].x], [df.iloc[index1].y, df.iloc[index2].y])
    plt.xlabel("X")
    plt.ylabel("Y")
    x1, y1 = df.iloc[index2].x, df.iloc[index2].y
    x2, y2 = df.iloc[index1].x, df.iloc[index1].y
    midx, midy = x1 - (x1 - x2) * 0.325, y1 - (y1 - y2) * 0.325
    frontx, fronty = x1 - (x1 - x2) * 0.15, y1 - (y1 - y2) * 0.15
    backx, backy = x1 - (x1 - x2) * 0.5, y1 - (y1 - y2) * 0.5

    plot_linec(x1, y1, x2, y2, 0.15, "0.15c")
    plot_linec(x1, y1, x2, y2, 0.3, "0.3c")
    plot_linec(x1, y1, x2, y2, 0.5, "0.5c")
    plt.legend(loc="lower right")
    plt.savefig(csv_path + "/front_mid_back.png")


# 初始化配置文件
opt = CONFIG(project_path='F:/ansys_program/windblade/ansys_model/',
             csv_path='F:/ansys_program/windblade/useful_csv/',
             Encoding='BG', NIND=20, MAXGEN=300,
             Drawing=1, plot_use=False,
             start_time=time.time(), ansys_time=1, primary_index=1)

getjiemian_linec(opt.csv_path)
