try:
  import readline
except ImportError:
    print('pip install pyreadline')
    raise
import cmd
import glob
import json
import os
import os.path
import socket
import subprocess
import threading
import time

from classes.job                import JobInformationDecoder, getJobList
from classes.workerinformation  import WorkerInformationDecoder
from classes.machineinformation import MachineInformationDecoder, getMachineList

def LoadJSONObject(File, Decoder):
    with open(File) as json_file:
        return json.load(json_file, cls=Decoder)
def printJobs(Directory, Worker = None):
    JobList = getJobList(Directory, filterByWorker=Worker)
    if len(JobList) == 0:
        raise RuntimeError('*** runtime error: no Jobs were found')

    WorkerList = set([ a.Information.Worker         for a in JobList ])
    StatusList = set([ a.Information.Status.lower() for a in JobList ])

    for Worker in WorkerList:
        print('========================================')
        print('{worker:^40}'.format(worker=Worker))
        print('========================================')
        for Status in StatusList:
            Jobs = getJobList(Directory, filterByWorker=Worker, filterByStatus=Status)
            if len(Jobs) > 0:
                print('--{status:-<38}'.format(status=Status.capitalize()))
                for Thread in Jobs:
                    print(os.path.basename(Thread.File))
    print('========================================')
def printMachines(Directory):
    MachineList = getMachineList(Directory)
    if len(MachineList) == 0:
        raise RuntimeError('*** runtime error: no Workers were found')
    print('========================================')
    print('{title:^40}'.format(title='WORKERS'))
    print('========================================')
    for Machine in MachineList:
        print(Machine)
    print('========================================')
def printMachineInformation(File):
    Machine = LoadJSONObject(File, MachineInformationDecoder)
    print('========================================')
    print('{domain:^40}'.format(domain=Machine.Domain))
    print('========================================')
    print('User:', Machine.CurrentUser)
    print('Name:', Machine.Name)
    print('IP:  ', Machine.IpAddress)
    print('----------------------------------------')
    print('CPU:  {numberofcores} Cores ({machinetype})'.format(machinetype=Machine.MachineType,numberofcores=Machine.NumberOfCores))
    print('OS:   {system} ({platform})'.format(system=Machine.System,platform=Machine.Platform))
    print('========================================')
def printJobInformation(File):
    Job = LoadJSONObject(File, JobInformationDecoder)
    print('========================================')
    print('{name:^40}'.format(name=Job.Name))
    print('========================================')
    print('Worker:   ', Job.Worker)
    print('Priority: ', Job.Priority)
    print('Status:   ', Job.Status)
    print('----------------------------------------')
    print('Script:   ', Job.Script)
    print('TimeOut:  ', Job.TimeOut)
    print('Directory:', Job.WorkingDirectory)
    print('========================================')
def printInformation(File):
    try:
        printMachineInformation(File)
        return
    except:
        pass
    try:
        printJobInformation(File)
        return
    except:
        pass
    raise FileNotFoundError('*** Ident error: file could not be read')

class JobViewer(cmd.Cmd):
    intro = 'Welcome to the Igor JobViewer. Type help or ? to list commands.'
    prompt = 'Igor>'
    config_file = 'config.json'
    def onecmd(self, line):
        #This ensures that we can use the do_* syntax and raise exceptions without breaking the program.
        #Furthermore, this means we can raise exceptions on deeper levels without implementing error handling in the do_* routines.
        try:
            return cmd.Cmd.onecmd(self, line)
        except Exception as Error:
            print(Error)
    def _WorkingDirectory(self):
        #Gets the JobDirectory from the configuration file.
        with open(self.config_file) as json_file:
            WorkerInformation = json.load(json_file, cls=WorkerInformationDecoder)
            return WorkerInformation.JobDirectory
    def do_show(self, arg):
        '''Shows detailed information about Jobs and Workers
        Usage: show [workers/jobs/NAME]
        workers         ... displays an overview of all workers
        jobs            ... displays an overview of all jobs
        jobs WORKERNAME ... the same as before, but only displays jobs from a certain worker
        '''
        arguments = arg.split()
        if   arguments[0].endswith('.json'):
            printInformation(arguments[0])
        elif arguments[0] == 'workers':
            printMachines(self._WorkingDirectory())
        elif arguments[0] == 'jobs':
            try:
                printJobs(self._WorkingDirectory(), arguments[1])
            except IndexError:
                printJobs(self._WorkingDirectory())
        else:
            raise NotImplementedError('*** Unknown syntax: ' + self.lastcmd)
    def _complete_show_commands(self, text, *ignored):
        commands = ['jobs','workers']
        return [a for a in commands if a.startswith(text)]
    def _complete_file_names(self, text, *ignored, filter):
        try:
            files = glob.glob(os.path.join(self._WorkingDirectory(),filter))
            return [os.path.basename(a) for a in files if os.path.basename(a).startswith(text)]
        except:
            return []
    def complete_show(self, *args):
        commands = set(self._complete_show_commands(*args))
        files    = set(self._complete_file_names(*args, filter='*.json'))
        return list(commands | files)
    def do_exit(self, arg):
        '''Exit the JobViewer'''
        return True

if __name__ == '__main__':
    JobViewer().cmdloop()

