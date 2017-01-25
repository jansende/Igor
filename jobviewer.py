

import socket
import json
import os
import os.path
import threading
import time
import subprocess

from jobserver import Job
from jobserver import JobServerConfiguration

def printJobList(Configuration):
    JobList = []
    for File in os.listdir(Configuration.JobDirectory()):
        if File.endswith('.json'):
            Thread = Job(os.path.join(Configuration.JobDirectory(),File))
            JobList.append(Thread)
    JobList.sort(key = lambda x: x.getStatus())
    print('+------------+------------+--------------------------------+----------+')
    print('|   Status   |   Worker   |              Name              | Priority |')
    print('+------------+------------+--------------------------------+----------+')
    for Thread in JobList:
        Status   = Thread.getStatus()
        Priority = Thread.getPriority()
        if Configuration.filterByName():
            if Thread.Name()[:-5].partition('.')[1]!='':
                Worker = Thread.Name()[:-5].partition('.')[0]
                Name   = Thread.Name()[:-5].partition('.')[2]
            else:
                Worker = ''
                Name   = Thread.Name()[:-5]
        else:
            Worker = ''
            Name   = Thread.Name()[:-5]
        out = '| {status:10} | {worker:10} | {name:30} | {priority:<8} |'.format(status=Status,worker=Worker,name=Name,priority=Priority)
        print(out)
    print('+------------+------------+--------------------------------+----------+')
if __name__== '__main__':
    Configuration = JobServerConfiguration('config.json')
    printJobList(Configuration)
