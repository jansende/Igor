import json
import os
import os.path
from classes.job import Job

class WorkerInformation(object):
    def __init__(self, JobDirectory = '.', filterByName = True, RefreshTime = 5.0, MaximumJobNumber = 1, Mode = 'Server'):
        self.JobDirectory     = JobDirectory
        self.filterByName     = filterByName
        self.RefreshTime      = RefreshTime
        self.MaximumJobNumber = MaximumJobNumber
        self.Mode             = Mode
    def JobList(self):
        List = []
        for File in os.listdir(self.JobDirectory):
            if File.endswith('.json'):
                try:
                    Thread = Job(os.path.join(self.JobDirectory,File))
                    List.append(Thread)
                except:
                    continue
        return List
    def __repr__(self):
        return '<WorkerInformation>'
class WorkerInformationEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, WorkerInformation):
            dic = {}
            dic['Worker'] = {}
            dic['Worker']['JobDirectory']     = obj.JobDirectory
            dic['Worker']['filterByName']     = obj.filterByName
            dic['Worker']['RefreshTime']      = obj.RefreshTime
            dic['Worker']['MaximumJobNumber'] = obj.MaximumJobNumber
            dic['Worker']['Mode']             = obj.Mode
            return dic
        else:
            raise TypeError
class WorkerInformationDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.default)
    def decode(self, s):
        obj = json.JSONDecoder.decode(self, s)
        if isinstance(obj, dict):
            raise RuntimeError
        return obj
    def default(self, dic):
        if 'Worker' not in dic:
            return dic
        else:
            obj = WorkerInformation()
            try:
                obj.JobDirectory = dic['Worker']['JobDirectory']
            except:
                pass
            try:
                obj.filterByName = dic['Worker']['filterByName']
            except:
                pass
            try:
                obj.RefreshTime = dic['Worker']['RefreshTime']
            except:
                pass
            try:
                obj.MaximumJobNumber = dic['Worker']['MaximumJobNumber']
            except:
                pass
            try:
                obj.Mode = dic['Worker']['Mode']
            except:
                pass
            return obj

if __name__== '__main__':
    test = WorkerInformation()
    print(test)
    data = json.dumps(test, cls=WorkerInformationEncoder)
    resu = json.loads(data, cls=WorkerInformationDecoder)
    print(resu)

    test_list = [WorkerInformation(),WorkerInformation(),WorkerInformation()]
    print(test_list)
    data_list = json.dumps(test_list, cls=WorkerInformationEncoder)
    resu_list = json.loads(data_list, cls=WorkerInformationDecoder)
    print(resu_list)