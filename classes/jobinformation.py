import json
import os

class JobInformation(object):
    def __init__(self, Name = 'unknown', Worker = '', Priority = 0, Status = 'ToDo', Script = '', TimeOut = None, WorkingDirectory = '.'):
        self.Name             = Name
        self.Worker           = Worker
        self.Priority         = Priority
        self.Status           = Status
        self.Script           = Script
        self.TimeOut          = TimeOut
        self.WorkingDirectory = WorkingDirectory
    def hasErrors(self):
        return self.Status == 'Error' or \
               self.Script == ''      or \
               not os.path.isdir(self.WorkingDirectory)
    def __repr__(self):
        return '<JobInformation: ' + self.Name + '>'
class JobInformationEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JobInformation):
            dic = {}
            dic['Job'] = {}
            dic['Job']['Name']             = obj.Name
            dic['Job']['Worker']           = obj.Worker
            dic['Job']['Priority']         = obj.Priority
            dic['Job']['Status']           = obj.Status
            dic['Job']['Script']           = obj.Script
            if obj.TimeOut is not None:
                dic['Job']['TimeOut']          = obj.TimeOut
            dic['Job']['WorkingDirectory'] = obj.WorkingDirectory
            return dic
        else:
            raise TypeError
class JobInformationDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.default)
    def decode(self, s):
        obj = json.JSONDecoder.decode(self, s)
        if isinstance(obj, dict):
            raise RuntimeError('json represents a different object')
        return obj
    def default(self, dic):
        if 'Job' not in dic:
            return dic
        else:
            obj = JobInformation()
            try:
                obj.Name = dic['Job']['Name']
            except:
                pass
            try:
                obj.Worker = dic['Job']['Worker']
            except:
                pass
            try:
                obj.Priority = dic['Job']['Priority']
            except:
                pass
            try:
                obj.Status = dic['Job']['Status']
            except:
                pass
            try:
                obj.Script = dic['Job']['Script']
            except:
                pass
            try:
                obj.TimeOut = float(dic['Job']['TimeOut'])
            except:
                pass
            try:
                obj.WorkingDirectory = dic['Job']['WorkingDirectory']
            except:
                pass
            return obj

if __name__== '__main__':
    test = JobInformation()
    print(test)
    data = json.dumps(test, cls=JobInformationEncoder)
    resu = json.loads(data, cls=JobInformationDecoder)
    print(resu)

    test_list = [JobInformation(),JobInformation(),JobInformation()]
    print(test_list)
    data_list = json.dumps(test_list, cls=JobInformationEncoder)
    resu_list = json.loads(data_list, cls=JobInformationDecoder)
    print(resu_list)