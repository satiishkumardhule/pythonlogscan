import os, sys, time
import logging

logger = logging.getLogger('logscan_application')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('logscan_application.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

inputDir=r"/home/satishkumardhule/logScan/logs"

def process_file(name):
    current = open(name, "r")
    curino = os.fstat(current.fileno()).st_ino
    while True:
        while True:
            line = current.readline()
            if not line:
                break
            print(f"file :{name} : {line}")
        try:
            
            if os.stat(name).st_ino != curino:
                new = open(name, "r")
                current.close()
                current = new
                curino = os.fstat(current.fileno()).st_ino
                logger.warning(f"{name} file has changed")
                continue
        except IOError:
            logger.fatal(f"{name} IO Exception")
            pass
        time.sleep(1)


from multiprocessing import Pool
from os import listdir 
p = Pool(100)
print()
logger.debug(listdir(inputDir))
# process_file(inputDir+r'/a')
p.map(process_file, [os.path.join(inputDir,i) for i in listdir(inputDir)])