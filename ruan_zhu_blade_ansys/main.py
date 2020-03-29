from ansys_model import ANSYS_MODEL
from NAGA_2 import MyProblem, NSGA2_ANSYS
from config import CONFIG
import pyansys

# 初始化配置文件
opt = CONFIG(root_path='/root/', Encoding='BG', NIND=20,
             MAXGEN=300, Drawing=1, plot_use=False)

# ansys建模
ansys = pyansys.Mapdl(run_location=opt.root_path, override=True,
                      interactive_plotting=True, loglevel="ERROR")
model = ANSYS_MODEL(ansys=ansys, opt=opt)
model.model()

# 多目标优化
ansys_nsga2 = NSGA2_ANSYS(MyProblem(ansys), opt.Encoding, opt.NIND,
                          opt.MAXGEN, opt.Drawing)
ansys_nsga2.run_nsga()
