import json
import multiprocessing
import os
import platform
import socket
import threading
from .helpers            import openJSON

class MachineInformation(object):
    def __init__(self, CurrentUser = 'unknown', Name = 'localhost', Domain = 'unknown', IpAddress = '127.0.0.1', NumberOfCores = 1, Platform = 'unknown', System = 'unknown', MachineType = 'unknown'):
        self.CurrentUser   = CurrentUser
        self.Name          = Name
        self.Domain        = Domain
        self.IpAddress     = IpAddress
        self.NumberOfCores = NumberOfCores
        self.Platform      = Platform
        self.System        = System
        self.MachineType   = MachineType
    def ThreadOffset(self):
        if   self.System == 'Windows':
            return 2
        elif self.System == 'linux':
            return 2
        else:
            return 2
    def NumberOfRunningJobs(self):
        #python + server are always running
        return threading.active_count() - self.ThreadOffset()
    def __repr__(self):
        return '<MachineInformation: ' + self.Name + '@' + self.IpAddress + ' (' + str(self.NumberOfCores) + ' Cores, ' + self.Platform + ')>'
    def __str__(self):
        return self.Name + '@' + self.IpAddress + ' (' + str(self.NumberOfCores) + ' Cores, ' + self.Platform + ')'
    class Encoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, MachineInformation):
                dic = {}
                dic['Machine'] = {}
                dic['Machine']['CurrentUser']   = obj.CurrentUser
                dic['Machine']['Name']          = obj.Name
                dic['Machine']['Domain']        = obj.Domain
                dic['Machine']['IpAddress']     = obj.IpAddress
                dic['Machine']['NumberOfCores'] = obj.NumberOfCores
                dic['Machine']['Platform']      = obj.Platform
                dic['Machine']['System']        = obj.System
                dic['Machine']['MachineType']   = obj.MachineType
                return dic
            else:
                raise TypeError
    class Decoder(json.JSONDecoder):
        def __init__(self):
            json.JSONDecoder.__init__(self, object_hook=self.default)
        def decode(self, s):
            obj = json.JSONDecoder.decode(self, s)
            if isinstance(obj, dict):
                raise RuntimeError('json represents a different object')
            return obj
        def default(self, dic):
            if 'Machine' not in dic:
                return dic
            else:
                obj = MachineInformation()
                try:
                    obj.CurrentUser = dic['Machine']['CurrentUser']
                except:
                    pass
                try:
                    obj.Name = dic['Machine']['Name']
                except:
                    pass
                try:
                    obj.Domain = dic['Machine']['Domain']
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
                try:
                    obj.MachineType = dic['Machine']['MachineType']
                except:
                    pass
                return obj
    class Loader(object):
        def __init__(self):
            pass
        def load(self):
            obj = MachineInformation()
            obj.CurrentUser = os.getlogin()
            try:
                obj.Name      = socket.gethostname()
                obj.Domain    = socket.getfqdn(obj.Name)
                obj.IpAddress = socket.gethostbyname(obj.Name)
            except:
                pass
            try:
                obj.NumberOfCores = multiprocessing.cpu_count()
            except:
                pass
            obj.Platform    = platform.platform(aliased=True, terse=True)
            obj.System      = platform.system()
            obj.MachineType = platform.machine()
            return obj

def getMachineList(Path, doCaseFold = True):
    MachineList = []
    for File in os.listdir(Path):
        if File.endswith('.json'):
            try:
                with openJSON(os.path.join(Path,File), MachineInformation) as Machine:
                    MachineList.append(Machine)
            except:
                continue
    MachineList.sort(key = lambda x: x.Domain)
    return MachineList

if __name__== '__main__':
    test = MachineInformation.Loader().load()
    print(test)
    data = json.dumps(test, cls=MachineInformation.Encoder)
    resu = json.loads(data, cls=MachineInformation.Decoder)
    print(resu)

    test_list = [MachineInformation.Loader().load(),MachineInformation.Loader().load(),MachineInformation.Loader().load()]
    print(test_list)
    data_list = json.dumps(test_list, cls=MachineInformation.Encoder)
    resu_list = json.loads(data_list, cls=MachineInformation.Decoder)
    print(resu_list)