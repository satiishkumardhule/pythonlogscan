import os, sys, time
import logging
from multiprocessing import Pool
from os import listdir
from glob import glob

'''
scanlogs is devided into two parts
 1. core part is the process file function, which is multithreaded and can read upto 100 files in parallel
 2. we are calling process file fuction from outside, to start processing all the log files in configured directory 
'''
logger = logging.getLogger('logscan_application')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('logscan_application.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.FATAL)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logDir = r"C:\Users\satis\PycharmProjects\pythonlogscan\logs"


def process_file(logName):
    '''
This function processes the log files
    - reads all the logs files while bootstraping and generates the payload for ELK
    - when log file gets updated, only updated part is being read by the function
    - in case of log file rotation, new file gets processed from the begining
    - Error handling is added in case, log file goes missing or moved
    '''
    import re
    error_pat = re.compile(
        r"\[(?P<timestamp>.*)\] \[(?P<log_level>(\w+))\] \[(?P<thread>.*)\] This is an error event for client \[(?P<client_id>.*)\]")
    data_pat = re.compile(
        r"\[(?P<timestamp>.*)\] \[(?P<log_level>(\w+))\] \[(?P<thread>.*)\] This is a data event showing \[(?P<id>.*)\]")

    current = open(logName, "r")
    curino = os.fstat(current.fileno()).st_ino
    while True:
        while True:
            line = current.readline()
            if not line:
                break
            logger.debug(f"file :{logName} : {line}")
            match = data_pat.match(line)

            if match:
                logger.debug(f"In match for {line}")
                timestamp = match.group("timestamp")
                log_level = match.group("log_level")
                thread = match.group("thread")
                id = match.group("id")
                print(
                    f"POST on DATA index '{{timestamp':{timestamp}, 'log_level':{log_level}, 'thread': {thread}, 'id':{id}}}")
            else:
                match = error_pat.match(line)
                if match:
                    timestamp = match.group("timestamp")
                    log_level = match.group("log_level")
                    thread = match.group("thread")
                    client_id = match.group("client_id")
                    client_id = '-masked-client-id-'
                    print(
                        f"POST on ERROR index {{'timestamp':{timestamp}, 'log_level':{log_level}, 'thread': {thread}, 'client_id':{client_id}}}")
        try:

            if os.stat(logName).st_ino != curino:
                new = open(logName, "r")
                current.close()
                current = new
                curino = os.fstat(current.fileno()).st_ino
                logger.warning(f"{logName} log file has been rotated")
                continue
        except IOError:
            logger.fatal(f"{logName} IO Exception")
            pass
        time.sleep(1)


if __name__ == '__main__':
    p = Pool(20)
    logger.debug(listdir(logDir))
    # process_file(logDir+r'/a')
    p.map(process_file, glob(os.path.join(logDir, "*.log")))
