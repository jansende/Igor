class WorkerInformation(object):
    JSONName = 'Worker'
    def __init__(self, JobDirectory = '.', filterByName = True, RefreshTime = 5.0, MaximumJobNumber = 1, Mode = 'Server'):
        self.JobDirectory     = JobDirectory
        self.filterByName     = filterByName
        self.RefreshTime      = RefreshTime
        self.MaximumJobNumber = MaximumJobNumber
        self.Mode             = Mode
    def __repr__(self):
        return '<WorkerInformation>'
