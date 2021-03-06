import os
import time
import datetime
import subprocess as sp
try:
    from Notify import Main as NotifyMain
    Notify = NotifyMain()
    Notify.SetMode("C")
except(ImportError):
    print("Unable to import Notify, Aborting.")
    exit()

class Timer:
    def __init__(self, StartHour, EndHour, Name):
        self.StartHour = StartHour
        self.EndHour = EndHour
        self.Name = Name
        self.Active = False
        self.CurrentHour = 0

    def GetNewTime(self):
        self.CurrentHour = datetime.datetime.today().hour
        self.CurrentHour = int(self.CurrentHour)

    def CheckIfTimerActive(self):
        if self.CurrentHour >= self.StartHour:
            if self.CurrentHour < self.EndHour:
                self.Active = True
        else:
            self.Active = False

    def IsTimerActive(self):
        if self.Active == True:
            return True
        else:
            return False

    def TimerLoop(self):
        self.GetNewTime()
        self.CheckIfTimerActive()

EFSS = Timer(6, 23,"EFSS")
SGPS = Timer(6, 23, "SGPS")

MainDeviceList = [["EFSS","00:0C:76:4E:1A:D1","192.168.1.25","OFFLINE"],
                  ["SGPS","78:45:C4:04:9D:68","192.168.1.3","OFFLINE"]
                  ]

class Main:
    def __init__(self):
        self.CurrentHour = ""
        self.CurrentMinute = ""

    def GetNewTimeData(self):
        self.CurrentHour = datetime.datetime.today().hour
        if self.CurrentHour in [1,2,3,4,5,6,7,8,9,0]:
            self.CurrentHour = "0" + str(datetime.datetime.today().hour)
        else:
            self.CurrentHour = str(datetime.datetime.today().hour)
        self.CurrentMinute = datetime.datetime.today().minute
        if self.CurrentMinute in [1,2,3,4,5,6,7,8,9,0]:
            self.CurrentMinute = "0" + str(datetime.datetime.today().minute)
        else:
            self.CurrentMinute = str(datetime.datetime.today().minute)

    def StartAllDevices(self):
        for count in range(0, len(MainDeviceList)):
            os.system("etherwake " + MainDeviceList[count][1])
            print("Packet Sent to: {}".format(MainDeviceList[count][1]))
        input()
        self.MainMenu()

    def ScanDevices(self):
        Notify.Info("Scanning Devices...")
        for count in range(0, len(MainDeviceList)):
            status,result = sp.getstatusoutput("ping -c1 -w2 " + MainDeviceList[count][2])
            if status == 0:
                MainDeviceList[count].insert(3,"ONLINE")
            else:
                MainDeviceList[count].insert(3,"OFFLINE")
        #print(MainDeviceList)

    def PrintDeviceStatus(self):
        self.ScanDevices()
        for count in range(0, len(MainDeviceList)):
            print("Device: " + MainDeviceList[count][0])
            if MainDeviceList[count][3] == "ONLINE":
                Notify.Green()
                print("ONLINE")
                Notify.ClearColour()
            elif MainDeviceList[count][3] == "OFFLINE":
                Notify.Red()
                print("OFFLINE")
                Notify.ClearColour()
            print()
        input()

    def AutoMode(self):
        SGPSStatus = False
        EFSSStatus = False
        try:
            while True:
                EFSS.TimerLoop()
                SGPS.TimerLoop()
                if EFSS.IsTimerActive() == True:
                    if EFSSStatus == False:
                        os.system("etherwake " + MainDeviceList[0][1])
                        Notify.Info("Started: {}".format(MainDeviceList[0][0]))
                    else:
                        Notify.Info("EFSS Online.")
                    EFSSStatus = True
                else:
                    EFSSStatus = False

                if SGPS.IsTimerActive() == True:
                    if SGPSStatus == False:
                        os.system("etherwake " + MainDeviceList[1][1])
                        Notify.Info("Started: {}".format(MainDeviceList[1][0]))
                    else:
                        Notify.Info("SGPS Online.")
                    SGPSStatus = True
                else:
                    SGPSStatus = False
                time.sleep(5)
        except(KeyboardInterrupt):
            self.MainMenu()



    def MainMenu(self):
        os.system("clear")
        self.GetNewTimeData()
        self.ScanDevices()
        print("""
        |----------------------------------|
        | Current Time: {}:{}              |
        |----------------------------------|
        |[1] Start All Devices             |
        |[2] Print Device Status           |
        |[3] Automatic Mode                |
        |[4] Exit                          |
        |----------------------------------|
        """.format(self.CurrentHour, self.CurrentMinute))
        while True:
            try:
                menuchoice = int(input("> "))
                if menuchoice not in [1,2,3,4]:
                    menuchoice = int(input("> "))
                else:
                    break
            except(ValueError):
                menuchoice = int(input("> "))
        if menuchoice == 1:
            self.StartAllDevices()
        elif menuchoice == 2:
            self.PrintDeviceStatus()
        elif menuchoice == 3:
            self.AutoMode()
        elif menuchoice == 4:
            exit()
        self.MainMenu()

Core = Main()
Core.MainMenu()