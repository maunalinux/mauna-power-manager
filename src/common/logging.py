import os
import time
from config import *
import datetime

if os.getuid() == 0:
    logfile = open("/var/log/mpm.log","a")
else:
    logfile = open("{}/.cache/mpm.log".format(os.environ["HOME"]),"a")

start_time = time.time()

def log_begin():
    logfile.write("##### {} #####\n".format(datetime.datetime.now()))

def log(msg):
    ftime = time.time() - start_time
    ftime = float(int(10000*ftime))/10000
    logfile.write("[{}]: {}\n".format(ftime, msg))
    logfile.flush()

if get("debug",False):
    debug = log
else:
    def debug(msg):
        return
