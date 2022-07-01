######################################################

import os
import time
import subprocess

######################################################

previousPlan = ""
previousPlatform =""
pdic = {"steam.exe" : 0, "EpicGamesLauncher.exe" : 0}
r = os.popen('powercfg /list')
u = "powercfg /setactive "
b = "powercfg /setactive "

######################################################

#subprocess.run(["powershell", "-Command", "clear"], capture_output=False)

######################################################

for line in r:
    if "Ultimate" in line:
        u += line.split(" ")[3]
        previousPlan = "UM"
    elif "Balanced" in line:
        b += line.split(" ")[3]
        previousPlan = "BM"

######################################################

r.close()

######################################################

while True:

    index = 0

    subprocess.call([r'GetProcess\getProcess.bat'])
    pList = open("GetProcess\processList.txt")

    for line in pList:
        for key in pdic.keys():
            if key in line:
                pdic[key] = 1
                #if previousPlatform == "":
                    #previousPlatform = key
                #else:

    
    pList.close()

    if sum(pdic.values()) > 0:
        if previousPlan == "BM":
            subprocess.run(["powershell", "-Command", u], capture_output=False)
            subprocess.call([r'MSI\MSIp1.bat'])
            print()
            print("Power plan: Ultimate mode")
            previousPlan = "UM"
    else:
        if previousPlan == "UM":
            subprocess.run(["powershell", "-Command", b], capture_output=False)
            subprocess.call([r'MSI\MSIp2.bat'])
            print()
            print("Power plan: Balanced mode")
            previousPlan = "BM"

    pdic = {"steam.exe" : 0, "EpicGamesLauncher.exe" : 0}
    time.sleep(1)

######################################################