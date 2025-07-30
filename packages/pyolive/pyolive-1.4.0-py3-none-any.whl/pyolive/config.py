import os
import yaml


class Config:
    ATHENA_HOME = os.getenv('ATHENA_HOME')

    def __init__(self, file):
        filepath = os.path.join(Config.ATHENA_HOME, 'config', file)
        with open(filepath) as f:
            self.cf = yaml.load(f, Loader=yaml.FullLoader)

    def get_value(self, key):
        name = key.split('/')
        size = len(name)
        if size == 1:
            val = self.cf[name[0]]
        elif size == 2:
            val = self.cf[name[0]][name[1]]
        elif size == 3:
            val = self.cf[name[0]][name[1]][name[2]]
        elif size == 4:
            val = self.cf[name[0]][name[1]][name[2]][name[3]]
        else:
            print("Overflow key depth")
        return val
