#!/usr/bin/env python3
from util import *
import sys
import subprocess

if len(sys.argv) < 2:
    sys.exit(0)

def write_settings(data):
    ctx = ""
    for section in data:
        if section == "osi":
            if "prefer" in data["osi"].keys() and data["osi"]["prefer"] != "":
                grub_cfg = "GRUB_CMDLINE_LINUX_DEFAULT=\"${GRUB_CMDLINE_LINUX_DEFAULT} acpi_osi=\\\""+data["osi"]["prefer"]+"\\\"\""
                writefile("/etc/default/grub.d/99-mpm.conf", grub_cfg)
            else:
                os.unlink("/etc/default/grub.d/99-mpm.conf")
            subprocess.run(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"])
            continue
        ctx += "[" + section + "]\n"
        for var in data[section]:
            ctx += str(var) + "=" + str(data[section][var]) +"\n"
        ctx += "\n"
    writefile("/etc/mauna/mpm.conf.d/99-mpm-settings.conf",ctx)


if sys.argv[1] == "save-config":
    write_settings(sys.argv[2])
