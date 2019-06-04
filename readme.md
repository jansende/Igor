Igor is a simple, file-based job manager written in python. If you want to run server jobs without installing a proper job management system, this is the right solution. All you need are several servers accessing the same (network) folder. You can then create and (remotely) run jobs using Igor from one pc. Linux, MacOs, and Windows are supported.

# Getting started
## Get the code
```bash
git clone https://github.com/jansende/Igor.git
cd Igor/
```
If you clone Igor into a network folder shared between clients and servers, you are done. If the folders are different, you need to repeat the cloning process for each machine.

## Start a server
The recommended way to use Igor, is to login to your remote machines, and start the server using `screen`.
```bash
ssh awesome.server
screen
python jobserver.py
#[Ctrl+A], [D] to leave the screen without killing it
exit
```

## View Jobs
Igor provides a custom command line viewer for your jobs. It is accessed by:
```bash
python jobviewer.py
```

## Creating Jobs
Currently Igor does not provide any facilities for creating jobs. However, it is easy to write your own job generator, as the information is written using json:

```json
{
    "Job": {
        "Name": "My Job Title",
        "Priority": 0,
        "Script": "echo 'Hello World'",
        "Status": "ToDo",
        "Worker": "awesome.server",
        "WorkingDirectory": "."
    }
}
```

- The `Name` field is only used for display purposes.
- The `Priority` field can be used to control the order in which things are run. Higher numbers will be run first.
- The `Script` field is what command/job you are running.
- The `Status` field describes the current status of the job. Use `ToDo` to make it run when the next server has time to do it. (And not job with higher priority.)
- The `Worker` field specifies on which server to run your job.
- The `WorkingDirectory` field sets the working directory for your command.

## Server Customization
You can specify the behaviour of your servers with the `config.json` file:

```json
{
    "Worker": {
        "JobDirectory"     : ".",
        "filterByName"     : false,
        "RefreshTime"      : 5.0,
        "MaximumJobNumber" : 4
  }
}
```

- The `JobDirectory` field specifies where the server searches for new jobs to run.
- The `filterByName` field specifies if the server should only run jobs with its server name. (`false` means it will run any job regardless of the `Worker` field of the job.)
- The `RefreshTime` field specifies how long the server waits until checking for jobs again. (In this case it is checking every 5 seconds.)
- The `MaximumJobNumber` field is used to specify how many jobs can be run in parallel by the server.

