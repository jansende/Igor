

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
    #get Status
    StatusList = []
    for Thread in JobList:
        Status = Thread.getStatus()
        if Status not in StatusList:
            StatusList.append(Status)
    for StatusSection in StatusList:
        for Thread in JobList:
            Status   = Thread.getStatus()
            Priority = Thread.getPriority()
            Worker   = ''
            Name     = Thread.Name()[:-5]
            if Configuration.filterByName() and Name.partition('.')[2]!='':
                    Worker = Name.partition('.')[0]
                    Name   = Name.partition('.')[2]
            if Status == StatusSection:
                out = '| {status:10} | {worker:10} | {name:30} | {priority:<8} |'.format(status=Status,worker=Worker,name=Name,priority=Priority)
                print(out)
        print('+------------+------------+--------------------------------+----------+')
if __name__== '__main__':
    Configuration = JobServerConfiguration('config.json')
    printJobList(Configuration)
