# PATH	'C:\Users\Administrator\Desktop\energies ¶þÉó·µÐÞ\Ò»ÉóÐÞ¶© 项目生成文件位置
# OUTSTR  10    计算开始时间
# ENDT	 100    计算结束时间
# US0Z0	 1.5    surface velocity
# MUCS	 2.967057   surface velocity degree流场角度，弧度
# TIDE	 0      相对海平面位置
# TP	 3.83   Peak spectral period波浪周期
# HS	 .33    wave height波高
# GAMMA	 3.33   Peakedness
# MUW	 2.722711   波浪角度，弧度
# IDUM	7   1-999的随机数字

import os
import random
from pprint import pprint
import pandas as pd
from Conf import CONF
import numpy
from tqdm import tqdm


class DLC_12():
    def __init__(self, opt, fa_num, fb_num, fa_prj, fb_prj):
        self.opt = opt
        self.fa_num = fa_num
        self.fb_num = fb_num
        self.fa_prj = fa_prj
        self.fb_prj = fb_prj
        self.compare_result_num = []
        self.compare_result_prj = []

    def compare_file(self):
        with open(self.fa_num, 'r') as fa:
            fa_lines = fa.readlines()
        with open(self.fb_num, 'r') as fb:
            fb_lines = fb.readlines()
        for i in range(len(fa_lines)):
            if fa_lines[i] != fb_lines[i]:
                self.compare_result_num.append(i)
        print('==========%s and %s compare=======' %
              (self.fa_num.split('/')[-1], self.fb_num.split('/')[-1]))
        for index in self.compare_result_num:
            print(fa_lines[index])
        print('===================end===================')

        with open(self.fa_prj, 'r') as ffa:
            ffa_lines = ffa.readlines()
        with open(self.fb_prj, 'r') as ffb:
            ffb_lines = ffb.readlines()
        for i in range(len(ffa_lines)):
            if ffa_lines[i] != ffb_lines[i]:
                self.compare_result_prj.append(i)
        # print('==========%s and %s compare=======' %
        #       (self.fa_prj.split('/')[-1], self.fb_prj.split('/')[-1]))
        # for index in self.compare_result_prj:
        #     print(ffa_lines[index])
        # print('===================end===================')

    def replace_file_by_parameters(self, file, compare_result_num, parameters):
        with open(file, 'r') as f:
            lines = f.readlines()
        for i in range(len(compare_result_num)):
            index = compare_result_num[i]
            temp_line = ''
            if 'PATH' in lines[index] and 'PATH' in parameters:
                temp_line = parameters['PATH']
            if 'OUTSTR' in lines[index] and 'OUTSTR' in parameters:
                temp_line = parameters['OUTSTR']
            if 'ENDT' in lines[index] and 'ENDT' in parameters:
                temp_line = parameters['ENDT']
            if 'US0Z0' in lines[index] and 'US0Z0' in parameters:
                temp_line = parameters['US0Z0']
            if 'MUCS' in lines[index] and 'MUCS' in parameters:
                temp_line = parameters['MUCS']
            if 'TIDE' in lines[index] and 'TIDE' in parameters:
                temp_line = parameters['TIDE']
            if 'TP' in lines[index] and 'TP' in parameters:
                temp_line = parameters['TP']
            if 'HS' in lines[index] and 'HS' in parameters:
                temp_line = parameters['HS']
            if 'GAMMA' in lines[index] and 'GAMMA' in parameters:
                temp_line = parameters['GAMMA']
            if 'MUW' in lines[index] and 'MUW' in parameters:
                temp_line = parameters['MUW']
            if 'IDUM' in lines[index] and 'IDUM' in parameters:
                temp_line = parameters['IDUM']
            lines[index] = temp_line
        return lines

    def generate_batch(self):
        batch_num = 1
        csv_file = pd.read_csv(self.opt['DLC']['DLC_12']['Csv_Path'])
        pbar = tqdm(range(csv_file.shape[0]))

        try:
            os.makedirs(os.path.join(self.opt['Root_path'], 'batch/dlc1.2/'))
        except:
            pass

        batch_lst = open(os.path.join(self.opt['Root_path'], 'batch/dlc1.2/', 'batch.lst'), 'w+')
        batch_lst.write('NUMBAT	%d\n' % csv_file.shape[0])
        for index in pbar:
            pbar.set_description('Generating Batch DLC1.2')
            # 写batch.x文件
            path = ('PATH\t%s\n' % os.path.join(self.opt['Root_path'], 'run/dlc1.2/',
                                                csv_file.iloc[index]['dlc_index'][3:])).replace('/', '\\')
            outstr = 'OUTSTR\t%d\n' % csv_file.iloc[index]['OUTSTR']
            endt = 'ENDT\t%d\n' % csv_file.iloc[index]['ENDT']
            us0z0 = 'US0Z0\t%.1f\n' % csv_file.iloc[index]['US0Z0']
            mucs = 'MUCS\t%f\n' % ((csv_file.iloc[index]['MUCS'] + 180) * 3.14159 / 180)
            tide = 'TIDE\t%d\n' % (csv_file.iloc[index]['TIDE'] - 30)
            tp = 'TP\t%.1f\n' % csv_file.iloc[index]['TP']
            hs = 'HS\t%.1f\n' % csv_file.iloc[index]['HS']
            gamma = 'GAMMA\t%f\n' % csv_file.iloc[index]['GAMMA']
            muw = 'MUW\t%f\n' % ((csv_file.iloc[index]['MUW'] + 180) * 3.14159 / 180)
            idum = 'IDUM\t%d\n' % random.randint(1, 999)
            param_num = {'PATH': path, 'OUTSTR': outstr, 'ENDT': endt, 'US0Z0': us0z0,
                         'MUCS': mucs, 'TIDE': tide, 'TP': tp, 'HS': hs,
                         'GAMMA': gamma, 'MUW': muw, 'IDUM': idum
                         }

            lines_num = self.replace_file_by_parameters(self.fa_num, self.compare_result_num, param_num)

            try:
                os.makedirs(os.path.join(self.opt['Root_path'], 'batch/dlc1.2/'))
            except:
                pass

            with open(os.path.join(self.opt['Root_path'], 'batch/dlc1.2/', 'Batch.' + str(batch_num)), 'w+') as f:
                for line in lines_num:
                    f.write(str(line))

            # 写batch.prj文件
            param_prj = {
                'OUTSTR': outstr, 'ENDT': endt, 'US0Z0': us0z0,
                'MUCS': mucs, 'TP': tp, 'HS': hs,
                'GAMMA': gamma, 'MUW': muw, 'IDUM': idum,
            }
            lines_prj = self.replace_file_by_parameters(self.fa_prj, self.compare_result_prj, param_prj)
            with open(os.path.join(self.opt['Root_path'], 'batch/dlc1.2/', 'BatchPrj.' + str(batch_num)), 'w+') as ff:
                for line in lines_prj:
                    ff.write(str(line))

            batch_lst.write(
                'IFILE	Batch.%d\nIPATH\t%s\nIEXTN\tpowprod\nIEXEC\t4:dtbladed\nICALC	10\nISTST\t-1;0;-1;-1;0\nIENAB\t-1\nDISCON\t-\n' % (
                    batch_num, (os.path.join(self.opt['Root_path'], 'run/dlc1.2/',
                                             csv_file.iloc[index]['dlc_index'][3:])).replace('/', '\\')
                ))
            batch_num += 1

    def run_dlc12(self):
        self.compare_file()
        self.generate_batch()


# 测试代码
opt = CONF().parse_json()
dlc11 = DLC_12(opt, '../DLC_12/compare_file/Batch.1', '../DLC_12/compare_file/Batch.2',
               '../DLC_12/compare_file/BatchPrj.1', '../DLC_12/compare_file/BatchPrj.2')
dlc11.run_dlc12()
