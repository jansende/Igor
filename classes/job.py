import json
import threading
from classes.jobinformation import JobInformation, JobInformationEncoder, JobInformationDecoder

class Job(threading.Thread):
    def __init__(self, File):
        threading.Thread.__init__(self)
        self.File        = File
        self.Information = JobInformation()
        self.loadInformationFromFile()
    def loadInformationFromFile(self):
        with open(self.File) as json_file:
            self.Information = json.load(json_file, cls=JobInformationDecoder)
        if self.Information.hasErrors():
            self.markFile('Error')
    def saveInformationToFile(self):
        with open(self.File,'w') as json_file:
            json_file.write(json.dumps(self.Information, sort_keys=True, indent=2, cls=JobInformationEncoder))
    def markFile(self, Status):
        self.Information.Status = Status
        self.saveInformationToFile()
    def run(self):
        try:
            Process = subprocess.Popen(self.Information.Script, cwd=self.Information.WorkingDirectory, shell=True)
            while Process.poll() is None:
                time.sleep(1)
            if Process.returncode > 0:
                raise
            self.markFile('Finished')
        except:
            self.markFile('Error')
    def __repr__(self):
        return '<Job: file="' + self.File + '", priority="' + str(self.Information.Priority) + '">'
    def __str__(self):
        return self.File