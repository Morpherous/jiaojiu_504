from Conf import CONF
from csv_generation import Generate_Csv
from Turbulent import Turbulent
from DLC_11 import DLC_11
from DLC_12 import DLC_12
from DLC_13 import DLC_13
from DLC_21 import DLC_21
from DLC_22 import DLC_22
from DLC_23 import DLC_23
from DLC_41 import DLC_41
from DLC_42 import DLC_42
from DLC_51 import DLC_51
from DLC_52 import DLC_52
from DLC_61 import DLC_61
from DLC_62 import DLC_62

# 加载配置文件（流剪切，风流速、流向 不设置）
opt = CONF().parse_json()

# 生成工况csv文件
all_csv = Generate_Csv(opt)
all_csv.generate_all_csv()

# 生成湍流文件
turbulent = Turbulent(opt)
turbulent.generate_batch()

# 开始生成工况文件
dlc11 = DLC_11(opt, './DLC_11/compare_file/Batch.1', './DLC_11/compare_file/Batch.2',
               './DLC_11/compare_file/BatchPrj.1', './DLC_11/compare_file/BatchPrj.2')
dlc11.run_dlc11()

dlc12 = DLC_12(opt, './DLC_12/compare_file/Batch.1', './DLC_12/compare_file/Batch.2',
               './DLC_12/compare_file/BatchPrj.1', './DLC_12/compare_file/BatchPrj.2')
dlc12.run_dlc12()

dlc13 = DLC_13(opt, './DLC_13/compare_file/Batch.1', './DLC_13/compare_file/Batch.2',
               './DLC_13/compare_file/BatchPrj.1', './DLC_13/compare_file/BatchPrj.2')
dlc13.run_dlc13()

dlc21 = DLC_21(opt, './DLC_21/compare_file/Batch.1', './DLC_21/compare_file/Batch.2',
               './DLC_21/compare_file/BatchPrj.1', './DLC_21/compare_file/BatchPrj.2')
dlc21.run_dlc21()

dlc22 = DLC_22(opt, './DLC_22/compare_file/Batch.1', './DLC_22/compare_file/Batch.2',
               './DLC_22/compare_file/BatchPrj.1', './DLC_22/compare_file/BatchPrj.2')
dlc22.run_dlc22()

dlc23 = DLC_23(opt, './DLC_23/compare_file/Batch.1', './DLC_23/compare_file/Batch.2',
               './DLC_23/compare_file/BatchPrj.1', './DLC_23/compare_file/BatchPrj.2')
dlc23.run_dlc23()

dlc41 = DLC_41(opt, './DLC_41/compare_file/Batch.1', './DLC_41/compare_file/Batch.2',
               './DLC_41/compare_file/BatchPrj.1', './DLC_41/compare_file/BatchPrj.2')
dlc41.run_dlc41()

dlc42 = DLC_42(opt, './DLC_42/compare_file/Batch.1', './DLC_42/compare_file/Batch.2',
               './DLC_42/compare_file/BatchPrj.1', './DLC_42/compare_file/BatchPrj.2')
dlc42.run_dlc42()

dlc51 = DLC_51(opt, './DLC_51/compare_file/Batch.1', './DLC_51/compare_file/Batch.2',
               './DLC_51/compare_file/BatchPrj.1', './DLC_51/compare_file/BatchPrj.2')
dlc51.run_dlc51()

dlc52 = DLC_52(opt, './DLC_52/compare_file/Batch.1', './DLC_52/compare_file/Batch.2',
               './DLC_52/compare_file/BatchPrj.1', './DLC_52/compare_file/BatchPrj.2')
dlc52.run_dlc52()

dlc61 = DLC_61(opt, './DLC_61/compare_file/Batch.1', './DLC_61/compare_file/Batch.2',
               './DLC_61/compare_file/BatchPrj.1', './DLC_61/compare_file/BatchPrj.2')
dlc61.run_dlc61()

dlc62 = DLC_62(opt, './DLC_62/compare_file/Batch.1', './DLC_62/compare_file/Batch.2',
               './DLC_62/compare_file/BatchPrj.1', './DLC_62/compare_file/BatchPrj.2')
dlc62.run_dlc62()
























