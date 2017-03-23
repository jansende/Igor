args=`getopt -o j:b:lc:w:h --long jobdir:,basedir:,log,corenum:,help,worker: -q -- "$@"`
OPTERROR=$?
eval set -- "$args"
#Check for Argument Errors
if [ $# -eq 1 ] && [ $OPTERROR == 0 ]; then
    echo "You didn't supply any arguments.  Try --help for more information."
    exit 1
fi
if [ $OPTERROR != 0 ]; then
    echo "You entered at least one invalid argument.  Try --help for more information."
    exit 1
fi
#Parse Arguments
while true; do
    case "$1" in
        -j|--jobdir)   OPTJOBDIR="$2/";     shift 2;;
        -b|--basedir)  OPTBASE="$2";       shift 2;;
        -l|--log)      OPTLOG="true";      shift;;
        -c|--corenum)  OPTCORE="-p $2";    shift 2;;
        -h|--help)     OPTHELP="true";     shift;;
        -w|--worker)   OPTWORKER="$2";     shift 2;;
        --) shift; break;;
        *) echo "Internal error! Try --help for more information."; exit 1;;
    esac
done
#Display help
if [ -n "$OPTHELP" ]; then
    echo "create_ace_job.sh creates a JSON Job File for the Igor JobServer"
    echo "Usage: create_ace_jobs.sh [OPTION] file"
    echo "Arguments:"
    echo " -j, --jobdir DIRECTORY   Creates the Job File in DIRECTORY instead of ."
    echo " -b, --basedir DIRECTORY  Tells the jobserver to run ACE in DIRECTORY instead of ."
    echo " -l, --log                Writes the output of ACE into file.log"
    echo " -c, --corenum CORES      Run Ace on that many cores"
    echo " -w, --worker WORKER      Assign WORKER to the Job"
    echo " -h, --help               To display this information."
    exit 0
fi
#Get File
filename=${1##*/}
fileprefix=${filename%.*}
basedirectory=$(realpath $1)
#Set Parameter
if [ -n "$OPTLOG" ]; then
    OPTLOG="> $fileprefix.log"
fi
#Create Job File
script="./ace $OPTCORE $filename $OPTLOG"
jobfilename="${OPTJOBDIR}${fileprefix}_ace.json"
echo "{                                                   ">$jobfilename
echo "  \"Job\": {                                        ">>$jobfilename
echo "    \"Name\"     : \"$fileprefix (ACE)\",           ">>$jobfilename
if [ -n "$OPTWORKER" ]; then
echo "    \"Worker\"   : \"$OPTWORKER\",                  ">>$jobfilename
fi
echo "    \"Script\"   : \"$script\",                     ">>$jobfilename
echo "    \"Status\"   : \"ToDo\",                        ">>$jobfilename
if [ -n "$OPTBASE" ]; then
echo "    \"WorkingDirectory\" : \"$OPTBASE\",            ">>$jobfilename
fi
echo "    \"Priority\" : 5                                ">>$jobfilename
echo "  }                                                 ">>$jobfilename
echo "}                                                   ">>$jobfilename

