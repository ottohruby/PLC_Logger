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
    ListOfNames = ['Index','ErrorEng','ErrorCz','Data4','Data5','Data6','Data7','Data8','Data9','Data10','Data11']
    try:
        df = pd.read_csv(path, names = ListOfNames)
        return df
    except Exception as e:
        raise ConfigError(f"ERROR in ErrorList({path}): Could not extract specified csv file")
#
def Get_Machine_From_Process(processNo):
    try:
        return structures.PROCESS_NO_DIC[int(processNo)]
    except KeyError as e:
        print(f"Get_Device_From_Process({processNo}): A machine with this processNo is not defined")
        return processNo

def Get_Err(data,process):
    err_df = ErrorList("Errors/error_p"+str(process)+".csv")
    try:
        rows = err_df.loc[err_df['Index'] == data]
        if len(rows) == 1:
            return rows['ErrorEng'].iloc[0]
        else:
            raise ConfigError()
    except Exception as e:
        raise ConfigError(f"Error in Get_Err({data}): Could not find an error with given code in csv file")
#
def FolderChk(path):
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
    # event = "E03"
    if not isinstance(error, str) or not isinstance(event, str):
        raise ConfigError(f"ERROR in CreateRow({error},{event}): Parameters must be strings")

    now = datetime.datetime.now()
    now = now.strftime("%Y/%m/%d/ %H:%M:%S")
    LineOfFile = now + "," + event + "," + error
    return LineOfFile
#
def WriteRow(data,processNo,model="533"):
    systemName = platform.system()
    if systemName == "Windows":
        DefaultPath = "C:/ShareData/Process{}/EasyProgram/Production inf/1AA-SA00337A [RSZL]/ProdLog".format(processNo)
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
# data = 55
# process = 999
# try:
#     print("nove: " + Get_Err(data,process))
# except Exception as e:
#     print(e)


# df = ErrorList("Errors/error_p999.csv")
# df1 = df[df.duplicated('Index', keep=False)].sort_values('ErrorEng')
# print(df1)
