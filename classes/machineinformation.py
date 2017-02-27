import json
import multiprocessing
import os
import platform
import socket
import threading

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
class MachineInformationEncoder(json.JSONEncoder):
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
class MachineInformationLoader(object):
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