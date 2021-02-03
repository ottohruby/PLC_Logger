#usr/bin/python3
from pathlib import Path
import csv
import datetime
import pandas as pd
import csv
import platform
#
class ConfigError(Exception):
    pass

#
def GetDate(mode):
    if mode == "file":
        x = datetime.date.today()
        return (x.strftime("%y%m%d"))
    elif mode == "folder":
        x = datetime.date.today()
        return (x.strftime("%y%m"))
    else:
        raise ConfigError(f"ERROR in GetDate({mode}): Invalid mode selected")
#
def LoadConfig():
    pass
#
def ErrorList(path):
    try:
        return pd.read_csv(path,skiprows = 2,index_col = 1)
    except Exception as e:
        raise ConfigError(f"ERROR in ErrorList({path}): Could not extract specified csv file")
#
def Get_Err(data):
    err = ErrorList("error_p1.csv")
    try:
        return str(err.iloc[int(data), 2])
    except Exception as e:
        raise ConfigError(f"Error in Get_Err({data}): Could not find an error at this location in csv file")
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
def WriteRow(data):
    systemName = platform.system()
    if systemName == "Windows":
        DefaultPath = "C:/ShareData/Process1/533/ProdLog"
    elif systemName == "Darwin":  # Mac
        DefaultPath = "/Users/げんちゃん/Server"
    else:  # Linux
        raise ConfigError(f"This system ({systemName}) is not supported")

    file = FolderChk(DefaultPath)
    file.write("\n")
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

