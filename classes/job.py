import json
import os
import os.path
import subprocess
import threading

from .jobinformation import JobInformation, JobInformationEncoder, JobInformationDecoder

class Job(threading.Thread):
    def __init__(self, File):
        threading.Thread.__init__(self)
        self.File        = File
        self.Information = JobInformation()
        self._loadInformationFromFile()
    def _loadInformationFromFile(self):
        if not os.path.isfile(self.File):
            raise
        with open(self.File) as json_file:
            self.Information = json.load(json_file, cls=JobInformationDecoder)
        if self.Information.hasErrors() and self.Status != 'FileError':
            self._markFile('FileError')
            raise
    def _saveInformationToFile(self):
        with open(self.File,'w') as json_file:
            json_file.write(json.dumps(self.Information, sort_keys=True, indent=2, cls=JobInformationEncoder))
    def _markFile(self, Status):
        self.Information.Status = Status
        self._saveInformationToFile()
    def run(self):
        try:
            self._markFile('InProgress')
            Process = subprocess.Popen(self.Information.Script, cwd=self.Information.WorkingDirectory, shell=True)
            Process.wait(self.Information.TimeOut)
            if Process.returncode != 0:
                raise RuntimeError
        except subprocess.TimeoutExpired:
            self._markFile('TimeOutError')
        except RuntimeError:
            self._markFile('RuntimeError')
        else:
            self._markFile('Finished')
        finally:
            Process.kill()
    def __repr__(self):
        return '<Job: file="' + self.File + '", priority="' + str(self.Information.Priority) + '">'
    def __str__(self):
        return self.File
def getJobList(Path, filterByStatus = None, filterByWorker = None, doCaseFold = True):
    JobList = []
    for File in os.listdir(Path):
        if File.endswith('.json'):
            try:
                Thread = Job(os.path.join(Path,File))
                JobList.append(Thread)
            except:
                continue
    if doCaseFold:
        if filterByStatus is not None:
            JobList = [x for x in JobList if x.Information.Status.casefold() == filterByStatus.casefold()]
        if filterByWorker is not None:
            JobList = [x for x in JobList if x.Information.Worker.casefold() == filterByWorker.casefold()]
    else:
        if filterByStatus is not None:
            JobList = [x for x in JobList if x.Information.Status == filterByStatus]
        if filterByWorker is not None:
            JobList = [x for x in JobList if x.Information.Worker == filterByWorker]
    JobList.sort(key = lambda x: x.Information.Priority)
    return JobList