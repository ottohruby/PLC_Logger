#usr/bin/python3
from pathlib import Path
import datetime
import pandas as pd
import platform
import numpy as np
#
class ConfigError(Exception):
    pass

#

##class Config():
##    def __init__(self):
##        self.ErrorCsv = "error_p1.csv"
##        self.FileName = "ProdLog_{}.csv"
##        systemName = platform.system()
##        if systemName == "Windows":
##            self.FolderName = "C:/ShareData/Process{}/533/ProdLog/{}"
##        else:
##            self.FolderName = ""
##            raise ConfigError(f"This system ({systemName}) is not supported")
##
##    def get_file_date(self):
##        x = datetime.date.today()
##        return (x.strftime("%y%m%d"))
##
##    def get_folder_date(self):
##        x = datetime.date.today()
##        return (x.strftime("%y%m"))
##
##    def folder_check(self, path):
##        print(path)
##        new_dir = Path(path)
##        try:
##            if not new_dir.exists():
##                new_dir.mkdir(parents=True)
##            else:
##                pass
##        except Exception as e:
##            raise ConfigError(f"Error in FolderChk({path}): The path of file is not correct")
##
##    def file_write(self, path, row):
##        print(path)
##        try:
##            if not Path(path).is_file():
##                f = open(path, "w")
##            else:
##                f = open(path, "a")
##        except Exception as e:
##            raise ConfigError(f"ERROR in FileChk({path}): Could not open the file")
##
##        f.write("\n")
##        f.write(row + "\n")
##        f.close()
##
##    def get_error_list(self):
##        try:
##            return pd.read_csv(self.ErrorCsv, skiprows=4)
##        except Exception as e:
##            raise ConfigError(f"ERROR in ErrorList({self.ErrorCsv}): Could not extract specified csv file")
##
##    def get_error(self, err):
##        list = self.get_error_list()
##        try:
##            return str(list.iloc[int(err), 2])
##        except Exception as e:
##            raise ConfigError(f"Error in Get_Err({err}): Could not find an error at this location in csv file")
##
##    def create_row(self, error, event = "E03"):
##        if not isinstance(error, str) or not isinstance(event, str):
##            raise ConfigError(f"ERROR in CreateRow({error},{event}): Parameters must be strings")
##
##        now = datetime.datetime.now()
##        now = now.strftime("%Y/%m/%d/ %H:%M:%S")
##        LineOfFile = now + "," + event + "," + str(error)
##        return LineOfFile
##
##
##
##    def write_row(self, data):
##        error = self.get_error(data[0])
##        row = self.create_row(error)
##
##        fileName = self.FileName.format(self.get_file_date())
##        fileFolder = self.FolderName.format(data[1], self.get_folder_date())
##        filePath = fileFolder +"/"+  fileName
##        self.file_write(filePath, row)

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
def Get_Err(data,process):
    err = ErrorList("Errors/error_p"+str(process)+".csv")
    try:
        return err.iat[int(data-1),1]    #Decrement value to compansate counting from 0 
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
def WriteRow(data,processNo,model="533"):
    systemName = platform.system()
    if systemName == "Windows":
        DefaultPath = "C:/ShareData/Process{}/ProdLog".format(processNo)
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
