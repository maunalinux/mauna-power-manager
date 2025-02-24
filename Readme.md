# Mauna Power Manager
Simple power manager tools written python.

## Features
* performance & powersave profile switch
* automatic profile switch on ac/bat modes
* uses own service

## How to install from source
```shell
# install source
meson setup build --prefix=/usr
ninja -C build install
# enable systemd service (if available)
systemctl enable mpm
# reboot required
reboot
```
## Configuration
Configuration files store in **/etc/mauna/mpm.conf** file and **/etc/mauna/mpm.conf.d/** directory.

## Usage
You can use `mpm` command for changing profile or brightness
```
Usage: pmm [set/get] [mode/backlight] (value)
```
Also you can use indicator from system tray.
