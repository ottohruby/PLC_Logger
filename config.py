#usr/bin/python3
from pathlib import Path
import csv
import datetime
import pandas as pd
import csv
#
def GetDate(mode):
    if mode == "file":
        x = datetime.date.today()
        return (x.strftime("%y%m%d"))
    if mode == "folder":
        x = datetime.date.today()
        return (x.strftime("%y%m"))
#
def LoadConfig():
    pass
#
def ErrorList(path):
    return pd.read_csv(path,skiprows = 2,index_col = 1)
#
def Get_Err(data):
    err = ErrorList("error_p1.csv")
    return str(err.iloc[int(data),2])
#
def FolderChk(path):
    path = path + "/" + GetDate("folder")
    new_dir = Path(path)
    if not new_dir.exists():
        new_dir.mkdir(parents=True)
    else:
        pass
    return FileChk(path)
#
def FileChk(path):
    filename = "ProdLog_" + GetDate("file") + ".csv"
    path = path +"/"+  filename
    if not Path(path).is_file():
        f = open(path, "w")
    else:
        f = open(path, "a")
    return f
#
def CreateRow(error,event="E03"):
    #event = "E03"
    now = datetime.datetime.now()
    now = now.strftime("%Y/%m/%d/ %H:%M:%S")
    LineOfFile = now + "," + event + "," + error
    return LineOfFile
#
def WriteRow(data):
    DefaultPath = "/Users/げんちゃん/Server"
    file = FolderChk(DefaultPath)
    file.write("¥n")
    file.write(data + "¥n")
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
