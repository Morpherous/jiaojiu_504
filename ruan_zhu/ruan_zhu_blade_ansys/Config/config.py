import time


class CONFIG():
    def __init__(self, project_path, csv_path, Encoding, NIND, MAXGEN,
                 Drawing, plot_use=True, start_time=time.time(), ansys_time=1, primary_index=1):
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
    # def _parse(self,**kwargs):
    #     for k,v in kwargs.items():
    #         if k not in self.__dict__():
    #             raise('Config Error: this key not in default key: %s'%k)
    #         setattr(self,k,v)
