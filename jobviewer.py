import json
import os
import os.path
import socket
import subprocess
import threading
import time

from classes.job               import getJobList
from classes.workerinformation import WorkerInformationDecoder

def printJobList(File):
    with open(File) as json_file:
        WorkerInformation = json.load(json_file, cls=WorkerInformationDecoder)
    JobList = getJobList(WorkerInformation.JobDirectory)
    JobList.sort(key = lambda x: x.Information.Status)
    print('+-----------------+------------+--------------------------------+----------+')
    print('|     Status      |   Worker   |              Name              | Priority |')
    print('+-----------------+------------+--------------------------------+----------+')
    StatusList = []
    for Thread in JobList:
        Status = Thread.Information.Status
        if Status not in StatusList:
            StatusList.append(Status)
    for StatusSection in StatusList:
        for Thread in JobList:
            Status   = Thread.Information.Status
            Priority = Thread.Information.Priority
            Worker   = Thread.Information.Worker
            Name     = Thread.Information.Name
            if Status == StatusSection:
                out = '| {status:15} | {worker:10} | {name:30} | {priority:<8} |'.format(status=Status,worker=Worker,name=Name,priority=Priority)
                print(out)
        print('+-----------------+------------+--------------------------------+----------+')
if __name__== '__main__':
    printJobList('config.json')
