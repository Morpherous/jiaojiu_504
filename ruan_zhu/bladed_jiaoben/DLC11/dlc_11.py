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
# TI	 .09    湍流数值
# TI_V	 .045   湍流*0.8
# TI_W	 .02    湍流*0.5
# WINDF	f:\bladed_test\current\dlc_11\1.4\b.wnd     .wnd文件生成位置

import os
from pprint import pprint
import pandas as pd


class DLC_11():
    def __init__(self, opt, fa, fb):
        self.opt = opt
        self.fa = fa
        self.fb = fb
        self.compare_result = []

    def compare_file(self):
        with open(self.fa, 'r') as fa:
            fa_lines = fa.readlines()
        with open(self.fb, 'r') as fb:
            fb_lines = fb.readlines()
        for i in range(len(fa_lines)):
            if fa_lines[i] != fb_lines[i]:
                self.compare_result.append(i)
        print('==========%s and %s compare=======' % (self.fa.split('/')[-1], self.fb.split('/')[-1]))
        for index in self.compare_result:
            print(fa_lines[index])
        print('===================end===================')

    def replace_file_by_parameters(self, parameters):
        with open(self.fa, 'r') as f:
            lines = f.readlines()
        for i in range(len(self.compare_result)):
            index = self.compare_result[i]
            temp_line = ''
            if 'PATH' in lines[index]:
                temp_line = parameters['PATH']
            if 'OUTSTR' in lines[index]:
                temp_line = parameters['OUTSTR']
            if 'ENDT' in lines[index]:
                temp_line = parameters['ENDT']
            if 'US0Z0' in lines[index]:
                temp_line = parameters['US0Z0']
            if 'MUCS' in lines[index]:
                temp_line = parameters['MUCS']
            if 'TIDE' in lines[index]:
                temp_line = parameters['TIDE']
            if 'TP' in lines[index]:
                temp_line = parameters['TP']
            if 'HS' in lines[index]:
                temp_line = parameters['HS']
            if 'GAMMA' in lines[index]:
                temp_line = parameters['GAMMA']
            if 'MUW' in lines[index]:
                temp_line = parameters['MUW']
            if 'IDUM' in lines[index]:
                temp_line = parameters['IDUM']
            if 'TI' in lines[index]:
                temp_line = parameters['TI']
            if 'TI_V' in lines[index]:
                temp_line = parameters['TI_V']
            if 'TI_W' in lines[index]:
                temp_line = parameters['TI_W']
            if 'WINDF' in lines[index]:
                temp_line = parameters['WINDF']
            lines[index] = temp_line
        return lines

    def generate_batch(self):
        csv_fil = pd.read_csv(self.opt['DLC']['DLC_11']['Csv_Path'])
