#usr/bin/python3
from pathlib import Path
import datetime
import pandas as pd
import platform
import numpy as np
import structures
#
class ConfigError(Exception):
    pass

def GetDate(mode):
    """
    Return date based on selected mode

    :param mode: Selected mode (file or folder)
    :return: Current date
    """

    if mode == "file":
        x = datetime.date.today()
        return (x.strftime("%y%m%d"))
    elif mode == "folder":
        x = datetime.date.today()
        return (x.strftime("%y%m"))
    else:
        raise ConfigError(f"ERROR in GetDate({mode}): Invalid mode selected")

def LoadConfig():
    pass

def ErrorList(path):
    """
    Return data frame based on given path

    :param path: Path to csv file
    :return: Data frame
    """

    ListOfNames = ['Index','ErrorEng','ErrorCz','Data4','Data5','Data6','Data7','Data8','Data9','Data10','Data11']
    try:
        df = pd.read_csv(path, names = ListOfNames)
        return df
    except Exception as e:
        raise ConfigError(f"ERROR in ErrorList({path}): Could not extract specified csv file")
#
def Get_Machine_From_Process(processNo):
    """
    Return the machine name based on given number of process

    :param processNo: Number of process
    :return: Machine name
    """

    try:
        return structures.PROCESS_NO_DIC[int(processNo)]
    except KeyError as e:
        print(f"Get_Device_Fromm_Process({processNo}): A machine with this processNo is not defined")
        return processNo

def Get_Err(data,process):
    """
    Return error description based on given error number

    :param data: Error number
    :param process: Number of process
    :return: Error description
    """

    err = ErrorList("Errors/error_p"+str(process)+".csv")
    try:
        return err.iat[int(data-1),1]    #Decrement value to compansate counting from 0 
    except Exception as e:
        raise ConfigError(f"Error in Get_Err({data}): Could not find an error at this location in csv file")
#
def FolderChk(path):
    """
    Return the file from given path
    If the parent folders does not exists they will be created

    :param path: Default path
    :return: Path to file
    """

    path = path + "/" + GetDate("folder")
    new_dir = Path(path)
    try:
        if not new_dir.exists():
            new_dir.mkdir(parents=True)
        else:
            pass
    except Exception as e:
        raise ConfigError(f"Error in FolderChk({path}): The path of file is not correct")
    return FileChk(path)


#
def FileChk(path):
    """
    Return file object from given path

    :param path: Path to file
    :return: File
    """

    filename = "ProdLog_" + GetDate("file") + ".csv"
    path = path +"/"+  filename
    try:
        if not Path(path).is_file():
            f = open(path, "w")
        else:
            f = open(path, "a")
    except Exception as e:
        raise ConfigError(f"ERROR in FileChk({path}): Could not open the file")
    return f


#
def CreateRow(error,event="E03"):
    """
    Create a new row from input information

    :param error: Error description
    :param event: Event description
    :return: Line of file which is going to be logged
    """

    if not isinstance(error, str) or not isinstance(event, str):
        raise ConfigError(f"ERROR in CreateRow({error},{event}): Parameters must be strings")

    now = datetime.datetime.now()
    now = now.strftime("%y/%m/%d %H:%M:%S")
    LineOfFile = now + "," + event + ",Increment arbitrary counter," + error
    return LineOfFile
#
def WriteRow(data,processNo,model="533"):
    """
    Write data to file

    :param data: Line which will be logged
    :param processNo: Process number
    :param model: Model number
    """

    systemName = platform.system()
    if systemName == "Windows":
        DefaultPath = "C:/ShareData/Process{}/EasyProgram/Production inf/1AA-SA0533A/ProdLog".format(processNo)
    elif systemName == "Darwin":  # Mac
        DefaultPath = "/Users/げんちゃん/Server"
    else:  # Linux
        raise ConfigError(f"This system ({systemName}) is not supported")

    file = FolderChk(DefaultPath)
    #file.write("\n")
    file.write(data + "\n")
    file.close()

#print("ProdLog_" + GetDate("folder") + ".csv")
#fields = "Test" + GetDate("folder")
#cesta = FolderChk("/Users/げんちゃん/Server")
#print (WriteRow(Get_Err(2)))
#data = CreateRow(Get_Err(3))
#WriteRow(data)
#print (type(cesta))
#print (type(Path("/Users/げんちゃん/Server")))
#print (GetDate(""))
#print (ErrorList("error_p1.csv"))
#new_line = csv.writer(y,)
#if __name__ == "__main__":
#    import sys
#    FolderChk(sys.arg[1])
# s = "C:\ShareData\Process{PROCESS NO}\533\ProdLog\{FOLDER DATE}"

#config = Config()
try:
    test = 1
    #config.write_row((1,2,3))
    #output = Get_Err(22,1)
    #print (output)
except Exception as e:
    print(e)
