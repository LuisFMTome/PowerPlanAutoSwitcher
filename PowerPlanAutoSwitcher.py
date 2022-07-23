######################################################
import os
import time
import pystray
import subprocess

from PIL import Image as img
from pystray import Icon, Menu, MenuItem
from threading import Thread
######################################################

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= (
    subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW
)
startupinfo.wShowWindow = subprocess.SW_HIDE

previousPlan = ""
platforms = {"steam" : 0, "EpicGamesLauncher" : 0}
u = "powercfg /setactive "
b = "powercfg /setactive "
gP = "Get-Process"
cmdMSI = "& 'C:\Program Files (x86)\MSI Afterburner\MSIAfterburner.exe' "
iconName = "Power Plan Switch"
iconImage = img.open("iconv2.png")

######################################################
r = os.popen('powercfg /list')

for line in r:
    if "Ultimate" in line:
        u += line.split(" ")[3]
        previousPlan = "UM"
    elif "Balanced" in line:
        b += line.split(" ")[3]
        previousPlan = "BM"

r.close()
######################################################
icon = pystray.Icon(iconName, iconImage, iconName)

def iconStart():
    icon.run()

def subprocessRun(cmd):
     subprocess.run(["powershell", "-Command", cmd], 
                capture_output=False, startupinfo=startupinfo)

thread = Thread(target = iconStart)
thread.start()

while True:

    index = 0
    processList = subprocess.run(["powershell", "-Command", gP], 
        capture_output=True, text=True, 
        startupinfo=startupinfo)

    for key in platforms.keys():
        if key in processList.stdout:
            platforms[key] = 1

    if sum(platforms.values()) > 0:
        if previousPlan == "BM":
            subprocessRun(u)
            subprocessRun(cmdMSI+"-Profile1")
            previousPlan = "UM"
    else:
        if previousPlan == "UM":
            subprocessRun(b)
            subprocessRun(cmdMSI+"-Profile2")
            previousPlan = "BM"
    
    platforms = {"steam" : 0, "EpicGamesLauncher" : 0}
    time.sleep(0.5)

######################################################
