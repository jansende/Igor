import socket
import json
import os
import os.path
import threading
import time
import subprocess

#CONFIG
min_thread_number = 2 #Linux
#min_thread_number = 3 #Windows

##TODO:
## - Keep somehow track, on what the Jobs are doing
class JobServer(threading.Thread):
    def __init__(self, Configuration):
        threading.Thread.__init__(self)
        self._Configuration = Configuration
    def run(self):
        print('JobServer started.')
        print('This is: ',self._Configuration.Name(),'@',self._Configuration.IpAddress(),sep='')
        while True:
            #Reread Configuration
            NumberOfRunningJobs = self._getNumberOfRunningJobs()
            MaximumJobNumber    = self._Configuration.MaximumJobNumber()
            RefreshTime         = self._Configuration.RefreshTime()
            ServerStatus        = self._Configuration.ServerStatus()
            #Do Stuff
            print('Checking Server Status...',end='')
            if ServerStatus == 'Shutdown':
                print()
                self.shutdown()
                break
            print('Done (Running in "',ServerStatus,'"-Mode.)',sep='')
            print('Currently ',NumberOfRunningJobs,' of ',MaximumJobNumber,' Slots are running Jobs.',sep='')
            if NumberOfRunningJobs < MaximumJobNumber:
                print('There is room for more!')
                print('Looking for new Jobs...',end='')
                JobList = self._getJobList()
                print('Done (',len(JobList),' found.)',sep='')
                if ServerStatus == 'Worker' and len(JobList) == 0:
                    print('No more new Jobs available. The Server will be shut down.')
                    self.shutdown()
                    print('All Jobs completed!')
                    break
                for i in range(0,MaximumJobNumber-NumberOfRunningJobs):
                    if len(JobList) == 0:
                        break
                    Thread = JobList.pop()
                    print('Running Job: ',Thread,' (Priority: ',Thread.getPriority(),')',sep='')
                    Thread.markJobFile()
                    Thread.start()
            print('Waiting for ',RefreshTime,'seconds...',sep='',end='')
            time.sleep(RefreshTime)
            print('Done')
    def shutdown(self):
        print('Server is scheduled for shutdown! Waiting for running Jobs to finish...',end='')
        self._waitForJobsToFinish()
        print('Done')
    def _waitForJobsToFinish(self):
        while threading.active_count() > min_thread_number:
            time.sleep(1)
    def _getJobList(self):
        JobList = []
        for File in os.listdir(self._Configuration.JobDirectory()):
            if File.endswith('.json'):
                Thread = Job(os.path.join(self._Configuration.JobDirectory(),File))
                if Thread.getStatus() == 'ToDo':
                    if self._Configuration.filterByName():
                        if File.startswith(self._Configuration.Name()+'.'):
                            JobList.append(Thread)
                    else:
                        JobList.append(Thread)
        JobList.sort(key = lambda x: x.getPriority())
        return JobList
    def _getNumberOfRunningJobs(self):
        #python + server are always running
        return threading.active_count() - min_thread_number
class Job(threading.Thread):
    def __init__(self, JobFile):
        threading.Thread.__init__(self)
        self._JobFile = JobFile
    def markJobFile(self,Mark='InProgress'):
        Data = None
        with open(self._JobFile) as json_data:
            Data = json.load(json_data)
            Data['Job']['Status'] = Mark
        if Data is not None:
            with open(self._JobFile,'w') as json_data:
                json_data.write(json.dumps(Data,sort_keys=True,indent=2))
    def run(self):
        Script           = self.getScript()
        WorkingDirectory = self.getWorkingDirectory()
        if Script is not None:
            try:
                if subprocess.Popen(Script,cwd=WorkingDirectory,shell=True) > 0:
                    raise
##                if subprocess.check(Script,shell=True) > 0:
##                    raise
                self.markJobFile('Finished')
            except:
                self.markJobFile('Error')
    def __repr__(self):
        return '<Job: file="' + self._JobFile + '", priority="' + str(self.getPriority()) + '">'
    def __str__(self):
        return self._JobFile
    def getScript(self):
        try:
            with open(self._JobFile) as json_data:
                Data = json.load(json_data)
                Script = Data['Job']['Script']
        except:
            Script = None
        return Script
    def getStatus(self):
        if self.getScript() is not None:
            try:
                with open(self._JobFile) as json_data:
                    Data = json.load(json_data)
                    Status = Data['Job']['Status']
            except:
                Status = 'ToDo'
        else:
            Status = 'Broken'
        return Status
    def getPriority(self):
        try:
            with open(self._JobFile) as json_data:
                Data = json.load(json_data)
                Priority = int(Data['Job']['Priority'])
        except:
            Priority = 0
        return Priority
    def getWorkingDirectory(self):
        try:
            with open(self._JobFile) as json_data:
                Data = json.load(json_data)
                WorkingDirectory = Data['Job']['WorkingDirectory']
        except:
            WorkingDirectory = os.path.dirname(self._JobFile)
        return WorkingDirectory
class JobServerConfiguration(object):
    def __init__(self, json_file):
        self._json_file   = json_file
    def Name(self):
        return socket.gethostname()
    def IpAddress(self):
        Address = socket.gethostbyname(self.Name())
        return Address
    def JobDirectory(self):
        try:
            with open(self._json_file) as json_data:
                Data = json.load(json_data)
                JobDirectory = Data['JobServer']['JobDirectory']
        except:
            JobDirectory = '.'
        return JobDirectory
    def filterByName(self):
        try:
            with open(self._json_file) as json_data:
                Data = json.load(json_data)
                filterByName = Data['JobServer']['filterByName']
        except:
            filterByName = False
        return filterByName
    def RefreshTime(self):
        try:
            with open(self._json_file) as json_data:
                Data = json.load(json_data)
                RefreshTime = float(Data['JobServer']['RefreshTime'])
        except:
            RefreshTime = 5.0
        return RefreshTime
    def MaximumJobNumber(self):
        try:
            with open(self._json_file) as json_data:
                Data = json.load(json_data)
                MaximumJobNumber = int(Data['JobServer']['MaximumJobNumber'])
        except:
            MaximumJobNumber = 4
        return MaximumJobNumber
    def ServerStatus(self):
        try:
            with open(self._json_file) as json_data:
                Data = json.load(json_data)
                ServerStatus = Data['JobServer']['ServerStatus']
        except:
            ServerStatus = "Server"
        return ServerStatus
if __name__== '__main__':
    Configuration = JobServerConfiguration('config.json')
    Server = JobServer(Configuration)
    Server.start()
    while threading.active_count() > min_thread_number-1:
        time.sleep(1)
