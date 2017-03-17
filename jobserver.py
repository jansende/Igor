import threading
import time

from classes.machineinformation import MachineInformation
from classes.worker             import Worker

if __name__== '__main__':
    Worker = Worker('config.json')
    Worker.start()
    Machine = MachineInformation.Loader().load()
    while threading.active_count() > Machine.ThreadOffset-1:
        time.sleep(1)
