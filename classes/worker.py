import json
import threading
import time
import os.path

from .machineinformation import MachineInformation
from .workerinformation  import WorkerInformation
from .job                import getJobList
from .helpers            import openJSON

class Worker(threading.Thread):
    def __init__(self, File):
        threading.Thread.__init__(self)
        self.File        = File
        self.Machine     = MachineInformation()
        self.Information = WorkerInformation()
        self.loadMachine()
        self.loadInformationFromFile()
    def loadInformationFromFile(self):
        with openJSON(self.File, WorkerInformation) as Information:
            self.Information.__dict__.update(Information.__dict__)
    def saveInformationToFile(self):
        with openJSON(self.File, WorkerInformation, 'u') as Information:
            Information.__dict__.update(self.Information.__dict__)
    def loadMachine(self):
        self.Machine = MachineInformation.Loader().load()
    def saveMachine(self):
        with openJSON(os.path.join(self.Information.JobDirectory, self.Machine.Name + '.json'),MachineInformation,'w') as Hardware:
            Hardware.__dict__.update(self.Machine.__dict__)
    def run(self):
        print('Worker started.')
        print('This is: ',self.Machine,sep='')
        while True:
            print('Checking Server Status...',end='')
            self.loadMachine()
            self.saveMachine()
            self.loadInformationFromFile()
            if self.Information.Mode == 'Shutdown':
                print()
                self.shutdown()
                break
            print('Done (Running in "',self.Information.Mode,'"-Mode.)',sep='')
            print('Currently ',self.Machine.NumberOfRunningJobs,' of ',self.Information.MaximumJobNumber,' Slots are running Jobs.',sep='')
            if self.Machine.NumberOfRunningJobs < self.Information.MaximumJobNumber:
                print('There is room for more!')
                print('Searching for Jobs in:', self.Information.JobDirectory)
                JobList = self._getJobList()
                if self.Information.Mode == 'Worker' and len(JobList) == 0:
                    print('No more new Jobs available. The Server will be shut down.')
                    self.shutdown()
                    print('All Jobs completed!')
                    break
                for i in range(0,self.Information.MaximumJobNumber-self.Machine.NumberOfRunningJobs):
                    if len(JobList) == 0:
                        break
                    Thread = JobList.pop()
                    print('Running Job: ',Thread,' (Priority: ',Thread.Information.Priority,')',sep='')
                    Thread.start()
            self.sleep(self.Information.RefreshTime)
    def sleep(self, RefreshTime):
        print('Waiting for ',RefreshTime,'s ...',sep='',end='')
        time.sleep(RefreshTime)
        print('Done')
    def shutdown(self):
        print('Server is scheduled for shutdown! Waiting for running Jobs to finish...',end='')
        self._waitForJobsToFinish()
        print('Done')
    def _waitForJobsToFinish(self):
        while threading.active_count() > self.Machine.ThreadOffset:
            time.sleep(1)
    def _getJobList(self):
        print('Looking for new Jobs...',end='')
        if self.Information.filterByName:
            JobList = getJobList(self.Information.JobDirectory, filterByStatus = 'ToDo', filterByWorker = self.Machine.Name, doCaseFold = True)
        else:
            JobList = getJobList(self.Information.JobDirectory, filterByStatus = 'ToDo', doCaseFold = True)
        print('Done (',len(JobList),' found.)',sep='')
        return JobList