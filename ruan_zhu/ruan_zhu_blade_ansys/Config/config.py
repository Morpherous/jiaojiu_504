import time

'''
CONFIG类中包含了所有需要配置的参数

Args:
    project_path:ansys模型存放的项目路径，程序自动生成的图片也将存放在此目录
    csv_path:叶片截面数据，格式为.csv
    Encoding:遗传算法编码方式，详见Geatpy说明
    NIND:种群个体数目
    MAXGEN:算法最大运行次数（遗传次数）
    Drawing:Geatpy中绘图方式选择，详见Geatpy
    plot_use:是否保存程序运行时所有截图，默认为False不保存
    start_time=time.time(), ansys_time=1:为计时参数，不用设置，采用默认即可
    primary_index=1:截面序号设定，不用设置，采用默认即可
'''

class CONFIG():
    def __init__(self, project_path, csv_path, Encoding, NIND, MAXGEN,
                 Drawing, plot_use=False, start_time=time.time(), ansys_time=1, primary_index=1):
        self.project_path = project_path
        self.csv_path = csv_path
        self.Encoding = Encoding
        self.NIND = NIND
        self.MAXGEN = MAXGEN
        self.Drawing = Drawing
        self.plot_use = plot_use
        self.ansys_time = ansys_time
        self.start_time = start_time
        self.primary_index = primary_index
        print('==========user config============')
        for k, v in self.__dict__.items():
            print(k, ":", v)
        print('============end==================')
    def _parse(self,**kwargs):
        state_dict=self._state_dict()
        for k,v in kwargs.items():
            if k not in state_dict:
                raise ValueError("Key is Error: %s"%k)
            setattr(self.k,v)

    def _state_dict(self):
        return {k:getattr(self,k) for k,_ in CONFIG.__dict__.items()
                if  not k.startswith('_')}