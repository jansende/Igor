import multiprocessing
import os
import platform
import socket
import threading
import time
from .helpers            import openJSON

class MachineInformation(object):
    JSONName = 'Machine'
    def __init__(self, CurrentUser = 'unknown', Name = 'localhost', Domain = 'unknown', IpAddress = '127.0.0.1', NumberOfCores = 1, Platform = 'unknown', System = 'unknown', MachineType = 'unknown', TimeStamp = time.ctime()):
        self.CurrentUser   = CurrentUser
        self.Name          = Name
        self.Domain        = Domain
        self.IpAddress     = IpAddress
        self.NumberOfCores = NumberOfCores
        self.Platform      = Platform
        self.System        = System
        self.MachineType   = MachineType
        self.TimeStamp     = TimeStamp
    @property
    def ThreadOffset(self):
        if   self.System == 'Windows':
            return 2
        elif self.System == 'linux':
            return 2
        else:
            return 2
    @property
    def NumberOfRunningJobs(self):
        #python + server are always running
        return threading.active_count() - self.ThreadOffset
    def __repr__(self):
        return '<MachineInformation: ' + self.Name + '@' + self.IpAddress + ' (' + str(self.NumberOfCores) + ' Cores, ' + self.Platform + ')>'
    def __str__(self):
        return self.Name + '@' + self.IpAddress + ' (' + str(self.NumberOfCores) + ' Cores, ' + self.Platform + ')'
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
