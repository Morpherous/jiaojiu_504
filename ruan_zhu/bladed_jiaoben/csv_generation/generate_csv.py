import pandas as pd
import os
from Conf import CONF
from tqdm import tqdm


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

class Generate_Csv():
    def __init__(self, opt):
        self.opt = opt

    def generate_dlc11(self):
        df = pd.DataFrame()
        stra = 'a'
        pbar = tqdm(range(len(self.opt['DLC']['DLC_11']['MeanSpeed'])))
        for index in pbar:
            pbar.set_description('Processing DLC_11')
            strb = 'a'
            for MUCS in self.opt['DLC']['DLC_11']['MUCS']:
                strindex = 1
                for MUW in self.opt['DLC']['DLC_11']['MUW']:
                    dlc_index = '1.1' + stra + strb + str(strindex)
                    US0Z0 = self.opt['DLC']['DLC_11']['MeanSpeed'][index]
                    TI = self.opt['DLC']['DLC_11']['MeanTur'][index]
                    hs = self.opt['DLC']['DLC_11']['HS']
                    tp = self.opt['DLC']['DLC_11']['TP']
                    gamma = self.opt['DLC']['DLC_11']['GAMMA']
                    tide = self.opt['DLC']['DLC_11']['TIDE'][0]
                    outstr = self.opt['DLC']['DLC_11']['OUTSTR']
                    endt = self.opt['DLC']['DLC_11']['ENDT']
                    add_data = pd.Series(
                        {'dlc_index': dlc_index, 'US0Z0': US0Z0, 'TI': TI, 'MUCS': MUCS,
                         'HS': hs, 'TP': tp, 'MUW': MUW, 'GAMMA': gamma, 'TIDE': tide,
                         'OUTSTR': outstr, 'ENDT': endt})
                    df = df.append(add_data, ignore_index=True)
                    strindex += 1
                strb = chr(ord(strb) + 1)
            stra = chr(ord(stra) + 1)
        # df.reindex(columns=['dlc_index', 'US0Z0', 'TI', 'MUCS', 'HS', 'TP', 'MUW', 'GAMMA', 'TIDE', 'OUTSTR', 'ENDT'])
        df.to_csv(self.opt['DLC']['DLC_11']['Csv_Path'], index=False)

    def generate_dlc12(self):
        df = pd.DataFrame()
        stra = 'a'
        pbar = tqdm(range(len(self.opt['DLC']['DLC_12']['MeanSpeed'])))
        for index in pbar:
            pbar.set_description('Processing DLC_12')
            for tide_index in range(len(self.opt['DLC']['DLC_12']['TIDE'])):
                for MUCS_index in range(len(self.opt['DLC']['DLC_11']['MUCS'])):
                    dlc_index = '1.2' + stra + '_' + str(tide_index + 1) + '_' + str(MUCS_index + 1)
                    US0Z0 = self.opt['DLC']['DLC_12']['MeanSpeed'][index]
                    MUCS = self.opt['DLC']['DLC_12']['MUCS'][MUCS_index]
                    hs = self.opt['DLC']['DLC_12']['HS']
                    tp = self.opt['DLC']['DLC_12']['TP']
                    MUW = self.opt['DLC']['DLC_12']['MUW'][0]
                    gamma = self.opt['DLC']['DLC_12']['GAMMA']
                    tide = self.opt['DLC']['DLC_12']['TIDE'][tide_index]
                    outstr = self.opt['DLC']['DLC_12']['OUTSTR']
                    endt = self.opt['DLC']['DLC_12']['ENDT']
                    add_data = pd.Series(
                        {'dlc_index': dlc_index, 'US0Z0': US0Z0, 'MUCS': MUCS,
                         'HS': hs, 'TP': tp, 'MUW': MUW, 'TIDE': tide, 'GAMMA': gamma,
                         'OUTSTR': outstr, 'ENDT': endt})
                    df = df.append(add_data, ignore_index=True)
            stra = chr(ord(stra) + 1)
        df.to_csv(self.opt['DLC']['DLC_12']['Csv_Path'], index=False)

    # 此处对于风流速和方向以及流剪切没有设置，因为为定值
    def generate_dlc13(self):
        df = pd.DataFrame()
        pbar = tqdm(range(len(self.opt['DLC']['DLC_13']['MeanSpeed'])))
        stra = 'a'
        for index in pbar:
            pbar.set_description('Processing DLC_13')
            for tide_index in range(len(self.opt['DLC']['DLC_13']['TIDE'])):
                dlc_index = '1.3' + stra + '_' + str(tide_index + 1)
                US0Z0 = self.opt['DLC']['DLC_13']['MeanSpeed'][index]
                MUCS = self.opt['DLC']['DLC_13']['MUCS'][0]
                hs = self.opt['DLC']['DLC_13']['HS']
                tp = self.opt['DLC']['DLC_13']['TP']
                MUW = self.opt['DLC']['DLC_13']['MUW'][0]
                # gamma = self.opt['DLC']['DLC_13']['GAMMA']
                tide = self.opt['DLC']['DLC_13']['TIDE'][tide_index]
                outstr = self.opt['DLC']['DLC_13']['OUTSTR']
                endt = self.opt['DLC']['DLC_13']['ENDT']
                add_data = pd.Series(
                    {'dlc_index': dlc_index, 'US0Z0': US0Z0, 'MUCS': MUCS,
                     'HS': hs, 'TP': tp, 'MUW': MUW, 'TIDE': tide,
                     'OUTSTR': outstr, 'ENDT': endt})
                df = df.append(add_data, ignore_index=True)
            stra = chr(ord(stra) + 1)
        df.to_csv(self.opt['DLC']['DLC_13']['Csv_Path'], index=False)

    # 2.1工况只有四个，直接手动设置即可
    # def generate_dlc21(self):

    def generate_dlc22(self):
        df = pd.DataFrame()
        pbar = tqdm(range(len(self.opt['DLC']['DLC_22']['MeanSpeed'])))
        stra = 'a'
        for index in pbar:
            pbar.set_description('Processing DLC_22')
            for pitch_index in range(len(self.opt['DLC']['DLC_22']['BREAKDOWN_PITCH'])):
                dlc_index = '2.2' + stra + str(pitch_index + 1)
                US0Z0 = self.opt['DLC']['DLC_22']['MeanSpeed'][index]
                MUCS = self.opt['DLC']['DLC_22']['MUCS'][0]
                hs = self.opt['DLC']['DLC_22']['HS']
                tp = self.opt['DLC']['DLC_22']['TP']
                MUW = self.opt['DLC']['DLC_22']['MUW'][0]
                # gamma = self.opt['DLC']['DLC_22']['GAMMA']
                tide = self.opt['DLC']['DLC_22']['TIDE'][0]
                outstr = self.opt['DLC']['DLC_22']['OUTSTR']
                endt = self.opt['DLC']['DLC_22']['ENDT']
                pitch = self.opt['DLC']['DLC_22']['BREAKDOWN_PITCH'][pitch_index]
                add_data = pd.Series(
                    {'dlc_index': dlc_index, 'US0Z0': US0Z0, 'MUCS': MUCS,
                     'HS': hs, 'TP': tp, 'MUW': MUW, 'TIDE': tide,
                     'OUTSTR': outstr, 'ENDT': endt, 'PITCH': pitch})
                df = df.append(add_data, ignore_index=True)
            stra = chr(ord(stra) + 1)
        df.to_csv(self.opt['DLC']['DLC_22']['Csv_Path'], index=False)

    # dlc2.3 dlc4.1工况很少，可以直接手动操作
    def generate_dlc42(self):
        df = pd.DataFrame()
        pbar = tqdm(range(len(self.opt['DLC']['DLC_42']['MeanSpeed'])))
        stra = 'a'
        for index in pbar:
            pbar.set_description('Processing DLC_42')
            for tide_index in range(len(self.opt['DLC']['DLC_42']['TIDE'])):
                for MUCS_index in range(len(self.opt['DLC']['DLC_11']['MUCS'])):
                    dlc_index = '4.2' + stra + '_' + str(tide_index + 1) + '_' + str(MUCS_index + 1)
                    US0Z0 = self.opt['DLC']['DLC_42']['MeanSpeed'][index]
                    MUCS = self.opt['DLC']['DLC_42']['MUCS'][MUCS_index]
                    hs = self.opt['DLC']['DLC_42']['HS']
                    tp = self.opt['DLC']['DLC_42']['TP']
                    MUW = self.opt['DLC']['DLC_42']['MUW'][0]
                    gamma = self.opt['DLC']['DLC_42']['GAMMA']
                    tide = self.opt['DLC']['DLC_42']['TIDE'][tide_index]
                    outstr = self.opt['DLC']['DLC_42']['OUTSTR']
                    endt = self.opt['DLC']['DLC_42']['ENDT']
                    add_data = pd.Series(
                        {'dlc_index': dlc_index, 'US0Z0': US0Z0, 'MUCS': MUCS,
                         'HS': hs, 'TP': tp, 'MUW': MUW, 'TIDE': tide, "GAMMA": gamma,
                         'OUTSTR': outstr, 'ENDT': endt})
                    df = df.append(add_data, ignore_index=True)
            stra = chr(ord(stra) + 1)
        df.to_csv(self.opt['DLC']['DLC_42']['Csv_Path'], index=False)

    def generate_dlc51(self):
        df = pd.DataFrame()
        stra = 'a'
        pbar = tqdm(range(len(self.opt['DLC']['DLC_51']['MeanSpeed'])))
        for index in pbar:
            pbar.set_description('Processing DLC_51')
            strb = 'a'
            for MUCS in self.opt['DLC']['DLC_51']['MUCS']:
                strindex = 1
                for MUW in self.opt['DLC']['DLC_51']['MUW']:
                    dlc_index = '5.1' + stra + strb + str(strindex)
                    US0Z0 = self.opt['DLC']['DLC_51']['MeanSpeed'][index]
                    TI = self.opt['DLC']['DLC_51']['MeanTur'][index]
                    hs = self.opt['DLC']['DLC_51']['HS']
                    tp = self.opt['DLC']['DLC_51']['TP']
                    gamma = self.opt['DLC']['DLC_51']['GAMMA']
                    tide = self.opt['DLC']['DLC_51']['TIDE'][0]
                    outstr = self.opt['DLC']['DLC_51']['OUTSTR']
                    endt = self.opt['DLC']['DLC_51']['ENDT']
                    add_data = pd.Series(
                        {'dlc_index': dlc_index, 'US0Z0': US0Z0, 'TI': TI, 'MUCS': MUCS,
                         'HS': hs, 'TP': tp, 'MUW': MUW, 'GAMMA': gamma, 'TIDE': tide,
                         'OUTSTR': outstr, 'ENDT': endt})
                    df = df.append(add_data, ignore_index=True)
                    strindex += 1
                strb = chr(ord(strb) + 1)
            stra = chr(ord(stra) + 1)
        df.to_csv(self.opt['DLC']['DLC_51']['Csv_Path'], index=False)

    # 此处对于风流速和方向以及流剪切没有设置，因为为定值
    def generate_dlc52(self):
        df = pd.DataFrame()
        pbar = tqdm(range(len(self.opt['DLC']['DLC_52']['MeanSpeed'])))
        stra = 'a'
        for index in pbar:
            pbar.set_description('Processing DLC_52')
            for tide_index in range(len(self.opt['DLC']['DLC_52']['TIDE'])):
                dlc_index = '1.3' + stra + '_' + str(tide_index + 1)
                US0Z0 = self.opt['DLC']['DLC_52']['MeanSpeed'][index]
                MUCS = self.opt['DLC']['DLC_52']['MUCS'][0]
                hs = self.opt['DLC']['DLC_52']['HS']
                tp = self.opt['DLC']['DLC_52']['TP']
                MUW = self.opt['DLC']['DLC_52']['MUW'][0]
                # gamma = self.opt['DLC']['DLC_52']['GAMMA']
                tide = self.opt['DLC']['DLC_52']['TIDE'][tide_index]
                outstr = self.opt['DLC']['DLC_52']['OUTSTR']
                endt = self.opt['DLC']['DLC_52']['ENDT']
                add_data = pd.Series(
                    {'dlc_index': dlc_index, 'US0Z0': US0Z0, 'MUCS': MUCS,
                     'HS': hs, 'TP': tp, 'MUW': MUW, 'TIDE': tide,
                     'OUTSTR': outstr, 'ENDT': endt})
                df = df.append(add_data, ignore_index=True)
            stra = chr(ord(stra) + 1)
        df.to_csv(self.opt['DLC']['DLC_52']['Csv_Path'], index=False)

    # dlc61工况很少，自行设置即可
    def generate_dlc62(self):
        df = pd.DataFrame()
        pbar = tqdm(range(2))
        stra = 'a'
        for index in pbar:
            pbar.set_description('Processing DLC_62')
            for muw_index in range(len(self.opt['DLC']['DLC_62']['MUW'])):
                for tide_index in range(len(self.opt['DLC']['DLC_62']['TIDE'])):
                    dlc_index = '6.2' + stra + '_' + str(muw_index + 1) + '_' + str(tide_index + 1)
                    US0Z0 = self.opt['DLC']['DLC_62']['MeanSpeed'][0]
                    hs = self.opt['DLC']['DLC_62']['HS']
                    tp = self.opt['DLC']['DLC_62']['TP']
                    MUCS = self.opt['DLC']['DLC_62']['MUCS'][index]
                    MUW = self.opt['DLC']['DLC_62']['MUW'][muw_index]
                    # gamma = self.opt['DLC']['DLC_62']['GAMMA']
                    tide = self.opt['DLC']['DLC_62']['TIDE'][tide_index]
                    outstr = self.opt['DLC']['DLC_62']['OUTSTR']
                    endt = self.opt['DLC']['DLC_62']['ENDT']
                    add_data = pd.Series(
                        {'dlc_index': dlc_index, 'US0Z0': US0Z0, 'MUCS': MUCS,
                         'HS': hs, 'TP': tp, 'MUW': MUW, 'TIDE': tide,
                         'OUTSTR': outstr, 'ENDT': endt})
                    df = df.append(add_data, ignore_index=True)
            stra = chr(ord(stra) + 1)
        df.to_csv(self.opt['DLC']['DLC_62']['Csv_Path'], index=False)

    def generate_all_csv(self):
        self.generate_dlc11()
        self.generate_dlc12()
        self.generate_dlc13()
        self.generate_dlc22()
        self.generate_dlc42()
        self.generate_dlc51()
        self.generate_dlc52()
        self.generate_dlc62()

# 测试代码
# opt = CONF().parse_json()
# all_csv = Generate_Csv(opt)
# all_csv.generate_all_csv()
