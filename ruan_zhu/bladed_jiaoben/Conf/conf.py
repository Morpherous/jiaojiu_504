import json
from pprint import pprint
import os

class CONF():
    def parse_json(self):
        info = json.load(open('./Conf/config.json', 'rb'))
        print("===============user config=======================")
        pprint(info)
        print('==================end============================')
        return info
