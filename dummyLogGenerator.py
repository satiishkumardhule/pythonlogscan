import os, sys, time
import logging
from multiprocessing import Pool
from os import listdir
from glob import glob
import datetime
import random
import os
logDir=r"C:\Users\satis\PycharmProjects\pythonlogscan\logs"
import shutil
#do something
import time

def process_file(logfile):
    while 1:
        if os.stat(logfile).st_size > 10000:
            try:
                shutil.move(logfile,logfile+"."+time.strftime("%Y%m%d%H%M%S"))
            except Exception:
                pass
        with open(logfile,'a') as fp:
            timestamp= datetime.datetime.now()
            client = 'Client-' + str(random.randint(1, 10000))
            thread = 'Thread-'+str(random.randint(1, 1000))
            id = random.randint(1, 1000)
            lines=[f"[{timestamp}] [INFO] [{thread}] This is a data event showing [{id}]\n",
             f"[{timestamp}] [ERROR] [{thread}] This is an error event for client [{client}]\n"]
            random.shuffle(lines)
            fp.write((lines[0]))
            time.sleep(0.01)

if __name__ == '__main__':
    p = Pool(20)
    p.map(process_file, glob(os.path.join(logDir,"*.log")))