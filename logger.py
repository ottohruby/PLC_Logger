# usr/bin/python3
import platform
import sys
import logging
from pathlib import Path
import structures
import pandas as pd
import os
from utils import *

DEFAULT_MODEL = "1AA-SA00533A"
ENCODING = 'utf-16'

# Check the platform
# Only windows and macOS are supported
system = platform.system()
if system == "Windows":
    DEFAULT_PATH = "C:/ShareData"
elif system == "Darwin":  # Mac
    DEFAULT_PATH = "/Users/げんちゃん/Server"
else:
    print(f"This system ({system}) is not supported")
    input("Press Enter to exit")
    sys.exit(-1)


class LoggerError(Exception):
    def __init__(self, msg=''):
        self.msg = msg
        print(msg)
        logging.error(msg, exc_info=True)


class Info(object):
    def __init__(self, received):
        """
        Contains basic information which are extracted from given data.
        Public methods:
            text() - Returns String which depends on event_code
        Public members:
            time - String with actual time
            data -
            process -
            process_text - String from PROCESS_TEXT_DIC
            event -
            event_text - String from EVENT_TEXT_DIC
            event_code - String from EVENT_CODE_DIC
            model -
            model_text - TODO

        :param received: Received bytes
        """

        self.time = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
        self._received = received

        self.data = self._received[0] # TODO to int only in specific
        try:
            self.process = int(self._received[1])
            self.event = int(self._received[2])
            self.model = int(self._received[3])
        except ValueError as e:
            raise LoggerError(f"{e}")

        self.process_text = self._process_text()

        self.event_text = self._event_text()
        self.event_code = self._event_code()

        self.model_text = DEFAULT_MODEL  # TODO

    def _process_text(self):
        """
        Looks for process text in dictionary
        If nothing was found then the default value is returned

        :return: String
        """
        try:
            return structures.PROCESS_TEXT_DIC[self.process]
        except KeyError:
            print(f"Machine with process number ({self.process}) is not defined")
            return f"Process {self.process}"

    def _event_text(self):
        """
        Looks for even text in dictionary
        If nothing was found the exception is raised and data are not logged

        :return: String
        """
        try:
            return structures.EVENT_TEXT_DIC[self.event]
        except KeyError:
            raise LoggerError(f"Event info with number ({self.event}) is not defined")

    def _event_code(self):
        """
        Looks for event code in dictionary
        If nothing was found the exception is raised and data are not logged

        :return: String
        """
        try:
            return structures.EVENT_CODE_DIC[self.event]
        except KeyError:
            raise LoggerError(f"Event code with number ({self.event}) is not defined")

    def _error_description(self):
        """
        Looks for error description based on given error number (data)
        If nothing was found the exception is raised and data are not logged

        :return: String
        """
        script_dir = os.path.dirname(os.path.realpath(__file__))
        path = f"{script_dir}/Errors/error_p{self.process}.csv"

        header = ['Index', 'ErrorEng', 'ErrorCz', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8', 'Data9', 'Data10',
                  'Data11']
        try:
            err_df = pd.read_csv(path, names=header)
        except Exception:
            raise LoggerError(f"Could not extract specified csv file: {path}")

        try:
            error_no = int(self.data)
        except ValueError as e:
            raise LoggerError(f"{e}")
        
        rows = err_df.loc[err_df['Index'] == error_no]['ErrorEng']
        if len(rows) == 1:
            return rows.fillna(f"Error {self.data}").iat[0]
        if len(rows) == 0:
            raise LoggerError(f"There is no error with code ({self.data}) in csv file: {path}")
        else:
            raise LoggerError(f"There are more errors with code ({self.data}) in csv file: {script_dir}")

    def text(self):
        """
        Specific function to create string from received data.

        :return: String which will be saved with Logger
        """
        text = f"{self.time},{self.event_code},{self.event_text}"

        if self.event_code == "E03":
            error = self._error_description()
            text += "," + error + "," + "1"
            print(f"{self.process_text} had error: {error}")

        if self.event_code == "D16":
            text += "," + self.data
            print(f"{self.process_text} log message: {self.data}")

        logging.info(f"{self.process_text} had event: {self.event_text}")
        return text


class Logger(object):
    def __init__(self, info):
        """
        Used to log received data.
        This class has no public methods and no public members.

        :param info: Info object
        """
        self._info = info
        self._folder_path = self._build_folder_path()
        self._file_path = f"{self._folder_path}/ProdLog_{get_date('file')}.csv"
        self._file = self._open_file()
        self._write()

    def _build_folder_path(self):
        """
        Builds path where logging file should be located.

        :return: Path
        """
        specific = f"Process{self._info.process}/EasyProgram/Production inf/{self._info.model_text}/ProdLog"
        return f"{DEFAULT_PATH}/{specific}/{get_date('folder')}"

    def _check_folder_path(self):
        """
        Check if folder path exists. If not, then it is created here.

        :return: None
        """
        try:
            Path(self._folder_path).mkdir(parents=True, exist_ok=True)
        except Exception:
            raise LoggerError(f"Could not create logging folder: {self._file_path}")

    def _open_file(self):
        """
        Opens the logging file.
        If the logging file does not exists then it will be created.

        :return: File
        """
        self._check_folder_path()
        try:
            f = open(self._file_path, "a", encoding=ENCODING)
        except Exception:
            raise LoggerError(f"ERROR in FileChk({self._file_path}): Could not open the file")
        return f

    def _write(self):
        """
        Writes text extracted from Info object to file.

        :return: None
        """
        if not self._file:
            self._open_file()

        log_data = self._info.text()
        f = self._open_file()
        f.write(log_data + "\n")
        f.close()
