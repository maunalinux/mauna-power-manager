import os
import sys
import json
from pathlib import Path
sys.path.insert(0, os.path.dirname( os.path.realpath(__file__) )+"/../common")
from common import *
def listen(main):
    if not os.path.exists("/run/mpm"):
        os.mkfifo("/run/mpm")
        os.chmod("/run/mpm", 0o222)
        os.chown("/run/mpm", 0, 0)
    while True:
        fifo = Path("/run/mpm")
        data = fifo.read_text().strip()
        print(data)
        if data != "":
            data = json.loads(data)
            if "pid" in data:
                main(data)
@cached
def list_acpi_osi():
    ret = []
    for name in strings("/sys/firmware/acpi/tables/DSDT"):
        if "_OSI\n" in name.strip():
            ret.append(name.split("\n")[-1])
    ret.sort()
    return ret

def send_client(data):
    print(data)
    data["pid"] = str(os.getpid())
    for dir in listdir("/run/user"):
        if os.path.exists("/run/user/{}/mpm/".format(dir)):
            for fifo in listdir("/run/user/{}/mpm/".format(dir)):
                debug("Send data to client: {} {}".format(dir, fifo))
                if not os.path.isdir("/proc/{}".format(fifo)):
                    os.unlink("/run/user/{}/mpm/{}".format(dir,fifo))
                else:
                    with open("/run/user/{}/mpm/{}".format(dir,fifo), "w") as f:
                        f.write(json.dumps(data))
                        f.flush()
