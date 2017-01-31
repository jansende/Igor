import json
import socket
import multiprocessing
import platform
import threading

class MachineInformation(object):
    def __init__(self, Name = 'localhost', IpAddress = '127.0.0.1', NumberOfCores = 1, Platform = 'unknown', System = 'unknown'):
        self.Name          = Name
        self.IpAddress     = IpAddress
        self.NumberOfCores = NumberOfCores
        self.Platform      = Platform
        self.System        = System
    def ThreadOffset(self):
        if self.System == 'Windows':
            return 2
        elif self.System == 'linux':
            return 2
        else:
            return 2
    def NumberOfRunningJobs(self):
        #python + server are always running
        return threading.active_count() - self.ThreadOffset()
    def __repr__(self):
        return '<MachineInformation: ' + self.Name + '@' + self.IpAddress + ' (' + str(self.NumberOfCores) + ' Cores, ' + self.System + ')>'
class MachineInformationEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MachineInformation):
            dic = {}
            dic['Machine'] = {}
            dic['Machine']['Name']          = obj.Name
            dic['Machine']['IpAddress']     = obj.IpAddress
            dic['Machine']['NumberOfCores'] = obj.NumberOfCores
            dic['Machine']['Platform']      = obj.Platform
            dic['Machine']['System']        = obj.System
            return dic
        else:
            raise TypeError
class MachineInformationDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.default)
    def decode(self, s):
        obj = json.JSONDecoder.decode(self, s)
        if isinstance(obj, dict):
            raise RuntimeError
        return obj
    def default(self, dic):
        if 'Machine' not in dic:
            return dic
        else:
            obj = MachineInformation()
            try:
                obj.Name = dic['Machine']['Name']
            except:
                pass
            try:
                obj.IpAddress = dic['Machine']['IpAddress']
            except:
                pass
            try:
                obj.NumberOfCores = dic['Machine']['NumberOfCores']
            except:
                pass
            try:
                obj.Platform = dic['Machine']['Platform']
            except:
                pass
            try:
                obj.System = dic['Machine']['System']
            except:
                pass
            return obj
class MachineInformationLoader(object):
    def __init__(self):
        pass
    def load(self):
        obj = MachineInformation()
        try:
            obj.Name      = socket.gethostname()
            obj.IpAddress = socket.gethostbyname(obj.Name)
        except:
            pass
        try:
            obj.NumberOfCores = multiprocessing.cpu_count()
        except:
            pass
        obj.Platform = platform.platform()
        obj.System   = platform.system()
        return obj

if __name__== '__main__':
    test = MachineInformationLoader().load()
    print(test)
    data = json.dumps(test, cls=MachineInformationEncoder)
    resu = json.loads(data, cls=MachineInformationDecoder)
    print(resu)

    test_list = [MachineInformationLoader().load(),MachineInformationLoader().load(),MachineInformationLoader().load()]
    print(test_list)
    data_list = json.dumps(test_list, cls=MachineInformationEncoder)
    resu_list = json.loads(data_list, cls=MachineInformationDecoder)
    print(resu_list)