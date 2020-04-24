from ansys_model import ANSYS_MODEL
from NSGA_2 import MyProblem, NSGA2_ANSYS
from Config import CONFIG
from util import getjiemian_linec
import pyansys
import time
import os
import geatpy as ea
#import ipdb

# 初始化配置文件
opt = CONFIG(project_path='F:/ansys_program/windblade/ansys_model/',
             csv_path='F:/ansys_program/windblade/useful_csv/',
             Encoding='BG', NIND=20,MAXGEN=300,
             Drawing=1, plot_use=False,
             start_time=time.time(), ansys_time=1, primary_index=1)

# ipdb.set_trace()

# ansys建模
ansys = pyansys.Mapdl(run_location=opt.project_path, override=True,
                      interactive_plotting=True, loglevel="ERROR")
model = ANSYS_MODEL(ansys=ansys, opt=opt)
model.model()

# 多目标优化
ansys_nsga2 = NSGA2_ANSYS(myproblem=MyProblem(model), Encoding=opt.Encoding,
                          NIND=opt.NIND, MAXGEN=opt.MAXGEN, Drawing=opt.Drawing)
ansys_nsga2.run_nsga()
# 关闭ansys后台
ansys.kill()
