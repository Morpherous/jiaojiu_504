import os
import random
from Conf import CONF


class Turbulent():
    def __init__(self, opt, refht):
        self.root_path = opt['Root_path']
        self.opt = opt
        self.Lambda = refht * 0.7 if refht < 60 else 42

    def generate_batch(self):
        for dlc in self.opt['DLC']:
            batch_num = 0
            for dlcname, dlc_dict in dlc.items():
                if len(dlc_dict['MeanTur']):
                    print("Generate %s `s turbulent" % (dlcname))

                    try:
                        os.makedirs(os.path.join(self.root_path, 'batch/Current_Turbulent/',
                                                 dlcname + '/'))
                    except:
                        pass
                    # 写batch.lst文件，batch_lst要记录所有流速，要先声明一下
                    batch_lst = open(os.path.join(self.root_path, 'batch/Current_Turbulent/',
                                                  dlcname + '/', 'batch.lst'), 'w+')
                    batch_lst.write('NUMBAT	%d\n' % (len(dlc_dict['MeanTur'])))
                    ######################
                    for velocity in dlc_dict['MeanSpeed']:
                        batch_num += 1
                        dlc_vel_path = os.path.join(self.root_path, 'batch/Current_Turbulent/' + dlcname)
                        dlc_vel_store_path = os.path.join(self.root_path, 'Current', dlcname, str(velocity))

                        try:
                            os.makedirs(dlc_vel_path)
                        except:
                            pass
                        try:
                            os.makedirs(dlc_vel_store_path)
                        except:
                            pass

                        # 写batch.x文件
                        batch_num_file = open(os.path.join(dlc_vel_path, 'batch.' + str(batch_num)), 'w+')

                        batch_num_file.write('RUNNAME	turb\nCALCN	3\nMSTART WINDND\nSPMODEL	7\n')

                        batch_num_file.write('NLAT	%d\nNVER	%d\nLATDIM	%d\nVERDIM	%d\n' % (
                            self.opt['CurNTMConst'][0], self.opt['CurNTMConst'][1],
                            self.opt['CurNTMConst'][2], self.opt['CurNTMConst'][3]
                        ))

                        batch_num_file.write('XLU	%f\nXLV	%f\nXLW	%f\n' % (
                            self.Lambda * 8.1, self.Lambda * 2.7, self.Lambda * 0.66))

                        batch_num_file.write(
                            'CohScale	%f\nCOHDEC	 12\nLENGTH	%f\n\nSTEP	%f\nUBAR	%f\nSEED	%d\n' % (
                                self.Lambda * 8.1, self.opt['CurNTMTime'][0] * velocity,
                                self.opt['CurNTMTime'][0] * velocity / 8192,
                                velocity, random.randint(1, 999)
                            ))

                        batch_num_file.write('OUTFILE\t%s\n' % (os.path.join(dlc_vel_store_path, 'turb.wnd')))
                        batch_num_file.write("MEND\n")

                        # 写batchPrj.x文件
                        batch_prj_file = open(os.path.join(dlc_vel_path, 'batchprj.' + str(batch_num)), 'w+')
                        batch_prj_file.write(
                            'VERSION	3.82\nTIDAL	-1\nCALCULATION	3\nOPTIONS	0\nPROJNAME\nDATE\nENGINEER\nNOTES	""\nPASSWORD\nMSTART WINDND\nSPMODEL	7\n')
                        batch_prj_file.write('NLAT	%d\nNVER	%d\nLATDIM	%d\nVERDIM	%d\n' % (
                            self.opt['CurNTMConst'][0], self.opt['CurNTMConst'][1],
                            self.opt['CurNTMConst'][2], self.opt['CurNTMConst'][3]
                        ))
                        batch_prj_file.write(
                            'LONGLS	 340.2\nLATLS	 0\nVERTLS	 0\nXLV	 113.4\nYLV	 0\nZLV	 0\nXLW	 27.72\nYLW	 0\nZLW	 0\nLAMBDA1	 0\nCohScale	 340.2\nCOHDEC	 12\nSCALE	 33.6\nGAMMA	 3.9\nYDIML	 0\nN2	32\nYDIMS	 0\nK1MIN	 3\n')
                        batch_prj_file.write(
                            'LENGTH	%f\nSTEP	%f\nUBAR	%f\nSEED	%d\n' % (
                                self.opt['CurNTMTime'][0] * velocity,
                                self.opt['CurNTMTime'][0] * velocity / 8192,
                                velocity, random.randint(1, 999)
                            )
                        )
                        batch_prj_file.write('OUTFILE\t%s\n' % (os.path.join(dlc_vel_store_path, 'turb.wnd')))
                        batch_prj_file.write(
                            'DIAM	 0\n\nHUBHT	 0\nTURBHTTYPE	 0\nTURBBOTTOM	 0\nGUSTAVT	 0\nGUSTSPEED	 0\nTOLERANCE	 0\nDLONGMIN	 0\nDLONGMAX	 0\nZ0MIN	 0\nZ0MAX	 0\nMAXITER	 14\nMAXSEED	 100\nNFILES	 1\nUseWindShear	 0\nWVMODEL	0\nMATCHFILE	''\nSPACING	 0\nSAMPLEFREQ	 0\nMEANSPEED	 0\nILAT	 0\nIVERT	 0\nGUSTMETHOD	 0\nDLONG	 0\nILAT	 0')
                        batch_prj_file.write(
                            'IVERT	 0\nLONGGUST	 0\nLATGUST	 0\nVERTGUST	 0\niLONGGUST	 0\niLATGUST	 0\niVERTGUST	 0\nPEAKINESS	 0\nMAXFRAN	 0\nMEND\n\n0WINDND\n')

                        # 写batch.lst文件
                        batch_lst.write(
                            'IFILE	Batch.%d\nIPATH	"%s"\nIEXTN	turb\nIEXEC	3:windnd\nICALC	3\nISTST	-1;0;0;0;0\nIENAB	-1\nDISCON	-\n' % (
                                batch_num, dlc_vel_store_path))

# 测试代码
# info = CONF()
# opt = info.parse_json()
# aaa = Turbulent(opt, 55)
# aaa.generate_batch()
