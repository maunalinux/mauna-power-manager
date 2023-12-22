import os
import configparser
cmdargs = {}
config = []
def reload_config():
    global cmdargs
    global config
    try:
        cfgs = ["/etc/mauna/mpm.conf"]
        if os.path.isdir("/etc/mauna/mpm.conf.d"):
            for cdir in os.listdir("/etc/mauna/mpm.conf.d/"):
                cfgs.append("/etc/mauna/mpm.conf.d/"+cdir)

        config = configparser.RawConfigParser()
        config.read(cfgs)
    except Exception as e:
        print(str(e))
        config = []

    cmdargs = {}
    with open("/proc/cmdline") as f:
        for word in f.read().split(" "):
            if word.startswith("mpm.") and "=" in word:
                v = word.split(".")
                if len(v) >= 3:
                    sec = v[1]
                    variable = v[2]
                    var = variable.split("=")[0]
                    value = variable.split("=")[1]
                    if sec not in cmdargs:
                        cmdargs[sec] = {}
                    cmdargs[sec][var] = value

    print(cmdargs)

reload_config()

def get(variable, default=None, section="mauna"):
    ret = default
    if section in cmdargs:
        if variable in cmdargs[section]:
            ret = cmdargs[section][variable]
    else:
        if section not in config:
            return default
        if variable not in config[section]:
            return default
        ret = config[section][variable]
    if default == True or default == False:
        if str(ret).lower() == "true":
            return True
        else:
            return False
    return str(ret)
