from util import *
import backends.power as power
import backends.backlight as backlight
import backends.battery as battery

def main(data):
    if os.path.exists("/usr/share/mauna/power-manager/pause-service"):
        return
    debug("Reading /run/mpm fifo")

    events_blocked = False

    # battery events
    if acpi_battery == None:
        battery_init()
    print(acpi_battery)
        
    for b in acpi_battery:
        b.update()
        if "update" in data:
            reload_config()
            if data["update"] == "service":
                if b.status == "charging":
                    continue
                if float(b.level) <= float(get("powersave_threshold","25","modes")):
                    power.set_mode("powersave")
                    events_blocked = True
            elif data["update"] == "client":
                b.set_stop_threshold(get("charge_stop_enabled",False,"modes"))

    if not events_blocked:
        # mode switch
        if "new-mode" in data:
            if data["new-mode"] in ["powersave", "balanced", "performance"]:
                power.set_mode(data["new-mode"])
        if "new-backlight" in data:
            for dev in data["new-backlight"]:
                backlight.set_brightness(dev, data["new-backlight"][dev])

    if "new-config" in data:
        write_settings(json.loads(data["new-config"]))

    # client update
    udata = {}
    udata["mode"] = power.get_mode()
    udata["info"] = {}
    udata["info"]["acpi-supported"] = is_acpi_supported()
    udata["info"]["laptop"] = is_laptop()
    udata["info"]["virtual-machine"] = is_virtual_machine()
    udata["info"]["type"] = get_device_type()    
    udata["info"]["live"] = is_live()
    udata["info"]["oem"] = is_oem_available()
    udata["info"]["deep"] = is_support_deep()    
    if "show" in data:
        udata["show"] = data["show"]    
    udata["backlight"] = {}
    for dev in backlight.get_devices():
        udata["backlight"][dev] = {}
        udata["backlight"][dev]["current"] = backlight.get_brightness(dev)
        udata["backlight"][dev]["max"] = backlight.get_max_brightness(dev)
    udata["battery"] = {}
    for dev in acpi_battery:
        udata["battery"][dev.name] = {}
        udata["battery"][dev.name]["level"] = dev.level
        udata["battery"][dev.name]["real_name"] = dev.real_name
        udata["battery"][dev.name]["status"] = dev.status
        udata["battery"][dev.name]["usage"] = dev.usage        
        udata["battery"][dev.name]["health"] = dev.health
    send_client(udata)

acpi_battery = None
def battery_init():
    global acpi_battery
    acpi_battery = []
    for dev in get_acpi_power_devices():
        path="/sys/class/power_supply/{}/".format(dev)
        devtype = readfile("{}/type".format(path)).lower()
        if  devtype == "battery":
            b = battery.battery(dev)
            b.set_stop_threshold(get("charge_stop_enabled",False,"modes"))
            acpi_battery.append(b)


def write_settings(data):
    ctx = ""
    for section in data:
        ctx += "[" + section + "]\n"
        for var in data[section]:
            ctx += str(var) + "=" + str(data[section][var]) +"\n"
        ctx += "\n"
    writefile("/etc/mauna/mpm.conf.d/99-mpm-settings.conf",ctx)
