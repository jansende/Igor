try:
  import readline
except ImportError:
    print('You need to install readline.')
    print('Under Windows use: pip install pyreadline')
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
import copy

from classes.job                import JobInformation, getJobList
from classes.workerinformation  import WorkerInformation
from classes.machineinformation import MachineInformation, getMachineList
from classes.helpers            import openJSON

def cleanJobs(Directory, Worker = None):
    for File in os.listdir(Directory):
        if File.endswith('.json'):
            try:
                with openJSON(os.path.join(Directory,File), JobInformation) as Job:
                    if Job.Status == 'Finished':
                        os.remove(os.path.join(Directory,File))
            except:
                continue
def cleanMachines(Directory):
    for File in os.listdir(Directory):
        if File.endswith('.json'):
            try:
                with openJSON(os.path.join(Directory,File), MachineInformation) as Machine:
                    os.remove(os.path.join(Directory,File))
            except:
                continue
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
    with openJSON(File, MachineInformation) as Machine:
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
    with openJSON(File, JobInformation) as Job:
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
    raise FileNotFoundError('*** File error: file could not be read')

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
        with openJSON(self.config_file, WorkerInformation) as Worker:
            return Worker.JobDirectory
    def do_show(self, arg):
        '''
           Display an overview of all jobs
           Usage: show jobs [WORKER]
               WORKER      ... filters jobs to display only those handled by WORKER

           Display an overview of all workers
           Usage: show workers

           Display information for a file (regardless if worker or job)
           Usage: show JSON_FILE
               JSON_FILE   ... job or workers file
        '''
        arguments = arg.split()
        if len(arguments) == 0:
            raise IndexError('*** Unknown syntax: ' + self.lastcmd)
        if   arguments[0].endswith('.json'):
            printInformation(os.path.join(self._WorkingDirectory(),arguments[0]))
        elif arguments[0] == 'workers':
            printMachines(self._WorkingDirectory())
        elif arguments[0] == 'jobs':
            try:
                printJobs(self._WorkingDirectory(), arguments[1])
            except IndexError:
                printJobs(self._WorkingDirectory())
        else:
            raise NotImplementedError('*** Unknown syntax: ' + self.lastcmd)
    def complete_show(self, *args):
        files    = set(self._complete_file_names(*args, filter='*.json'))
        commands = set(self._complete_show_commands(*args))
        return list(commands | files)
    def do_clean(self, arg):
        '''
           Removes all completed jobs from the job folder
           Usage: clean jobs

           Removes all worker information from the worker information folder
           Usage: clean workers
        '''
        arguments = arg.split()
        if len(arguments) != 1:
            raise IndexError('*** Unknown syntax: ' + self.lastcmd)
        if arguments[0] == 'workers':
            cleanMachines(self._WorkingDirectory())
        elif arguments[0] == 'jobs':
            cleanJobs(self._WorkingDirectory())
        else:
            raise NotImplementedError('*** Unknown syntax: ' + self.lastcmd)
    def complete_clean(self, *args):
        #The commands are the same as for show
        commands = set(self._complete_show_commands(*args))
        return list(commands)
    def do_redo(self, arg):
        '''
           Restart a given job
           Usage: redo JSON_FILE
               JSON_FILE   ... job file
        '''
        arguments = arg.split()
        if len(arguments) == 0:
            raise IndexError('*** Unknown syntax: ' + self.lastcmd)
        if   arguments[0].endswith('.json'):
            with openJSON(os.path.join(self._WorkingDirectory(),arguments[0]), JobInformation, 'u') as New:
                New.Status = 'ToDo'
        else:
            raise NotImplementedError('*** Unknown syntax: ' + self.lastcmd)
    def complete_redo(self, *args):
        files    = set(self._complete_file_names(*args, filter='*.json'))
        return list(files)
    def do_reassign(self, arg):
        '''
           Reassigns a given job to a new worker
           Usage: reassign JSON_FILE WORKER
               JSON_FILE   ... job file
               WORKER      ... name of the worker the job is assigned to
        '''
        arguments = arg.split()
        if len(arguments) == 2:
            with openJSON(os.path.join(self._WorkingDirectory(),arguments[0]), JobInformation, 'u') as New:
                New.Worker = arguments[1]
        else:
            raise NotImplementedError('*** Unknown syntax: ' + self.lastcmd)
    def complete_reassign(self, *args):
        files    = set(self._complete_file_names(*args, filter='*.json'))
        return list(files)
    def do_delete(self, arg):
        '''
           Deletes a given job file
           Usage: delete JSON_FILE
               JSON_FILE   ... job file
        '''
        arguments = arg.split()
        if len(arguments) == 1:
            os.remove(os.path.join(self._WorkingDirectory(),arguments[0]))
        else:
            raise NotImplementedError('*** Unknown syntax: ' + self.lastcmd)
    def complete_delete(self, *args):
        files    = set(self._complete_file_names(*args, filter='*.json'))
        return list(files)
    def _complete_file_names(self, text, *ignored, filter):
        try:
            files = glob.glob(os.path.join(self._WorkingDirectory(),filter))
            return [os.path.basename(a) for a in files if os.path.basename(a).startswith(text)]
        except:
            return []
    def _complete_show_commands(self, text, *ignored):
        commands = ['jobs','workers']
        return [a for a in commands if a.startswith(text)]
    def do_exit(self, arg):
        '''Exit the JobViewer'''
        return True

if __name__ == '__main__':
    JobViewer().cmdloop()

