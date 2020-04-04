import os
import random
from Conf import CONF


class Turbulent():
    def __init__(self, root_path, opt, refht):
        self.root_path = root_path
        self.opt = opt
        self.Lambda = refht * 0.7 if refht < 60 else 42

    def generate_turbulent_path(self):

        try:
            os.mkdir(os.path.join(self.root_path, '/batch/Current_Turbulent/'))
        except:
            print("/batch/Current/ exist")

        for dlcname, _ in self.opt['DLC']:
            os.makedirs(os.path.join(self.root_path, '/batch/Current_Turbulent/' + dlcname))

    def generate_batch(self):
        for dlc in self.opt['DLC']:
            batch_num = 0
            for dlcname, dlc_dict in dlc.items():
                if len(dlc_dict['MeanTur']):
                    print("Generate %s turbulent" % (dlcname))
                    for velocity in dlc_dict['MeanSpeed']:
                        batch_num += 1
                        dlc_vel_path = os.path.join(self.root_path, 'batch/Current_Turbulent/', dlcname
                                                    , str(velocity))
                        try:
                            os.makedirs(dlc_vel_path)
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

                        batch_num_file.write('OUTFILE\t%s\n' % (os.path.join(dlc_vel_path, 'turb.wnd')))
                        batch_num_file.write("MEND\n")

                        # 写batchPrj.x文件


    def run_turbulent(self):
        self.generate_batch()
        self.generate_batch()


info = CONF()
opt = info.parse_json()
aaa = Turbulent("F:/blade_test/", opt, 55)
aaa.run_turbulent()
