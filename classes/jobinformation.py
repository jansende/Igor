import os.path

class JobInformation(object):
    JSONName = 'Job'
    def __init__(self, Name = 'unknown', Worker = '', Priority = 0, Status = 'ToDo', Script = '', TimeOut = None, WorkingDirectory = '.'):
        self.Name             = Name
        self.Worker           = Worker
        self.Priority         = Priority
        self.Status           = Status
        self.Script           = Script
        self.TimeOut          = TimeOut
        self.WorkingDirectory = WorkingDirectory
    @property
    def hasErrors(self):
        return self.Status == 'Error' or \
               self.Script == ''      or \
               not os.path.isdir(self.WorkingDirectory)
    def __repr__(self):
        return '<JobInformation: ' + self.Name + '>'