#!/usr/bin/env python

import DobotDllType as dType
import sys
import bezierCurve as bCurve
import catMullRomCurve as sCurve
import matplotlib.pyplot as plt
sys.path.insert(1, './DLL')  # retireve the DLLs


"""-------The DoBot Control Class-------
Variables:
suction = Suction is currently on/off
picking: shows if the dobot is currently picking or dropping an item
api = variable for accessing the dobot .dll functions
home% = home position for %
                                  """

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
}

# Main control class for the DoBot Magician.


class DoBotArm:
    def __init__(self, homeX, homeY, homeZ):
        self.suction = False
        self.picking = False
        self.api = dType.load()
        self.homeX = homeX
        self.homeY = homeY
        self.homeZ = homeZ
        self.connected = False
        self.dobotConnect()

    def __del__(self):
        self.dobotDisconnect()

    # Attempts to connect to the dobot
    def dobotConnect(self):
        if(self.connected):
            print("You're already connected")
        else:
            state = dType.ConnectDobot(self.api, "", 115200)[0]
            # if everything connected proprely set up the configuration
            if(state == dType.DobotConnect.DobotConnect_NoError):
                print("Connect status:", CON_STR[state])
                dType.SetQueuedCmdClear(self.api)

                dType.SetHOMEParams(self.api, self.homeX,
                                    self.homeY, self.homeZ, 0, isQueued=1)
                dType.SetPTPJointParams(
                    self.api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued=1)
                dType.SetPTPCommonParams(self.api, 100, 100, isQueued=1)

                dType.SetHOMECmd(self.api, temp=0, isQueued=1)
                self.connected = True
                return self.connected
            else:
                print("Unable to connect")
                print("Connect status:", CON_STR[state])
                return self.connected

    # Returns to home location and then disconnects
    def dobotDisconnect(self):
        self.moveHome()
        dType.DisconnectDobot(self.api)

    # Delays commands
    def commandDelay(self, lastIndex):
        dType.SetQueuedCmdStartExec(self.api)
        while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
            dType.dSleep(200)
        dType.SetQueuedCmdStopExec(self.api)

    # Toggles suction peripheral on/off
    def toggleSuction(self):
        lastIndex = 0
        if(self.suction):
            lastIndex = dType.SetEndEffectorSuctionCup(
                self.api, True, False, isQueued=0)[0]
            self.suction = False
        else:
            lastIndex = dType.SetEndEffectorSuctionCup(
                self.api, True, True, isQueued=0)[0]
            self.suction = True
        self.commandDelay(lastIndex)

    # Moves arm to X/Y/Z Location
    def moveArmXYZ(self, x, y, z):
        lastIndex = dType.SetPTPCmd(
            self.api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, 0)[0]
        self.commandDelay(lastIndex)

    # draws a curve, if 0 draws bezier else draws catmull
    def drawCurve(self, ctrlP=5, curve=0):
        print('Move the arm to the z position of the paper, when you are done enter OK in the console:')
        _ = input()
        zLevel = dType.GetPose(self.api)[2]
        self.moveHome()
        if curve == 0:  # bezier curve
            x, y, z, X, Y, Z = bCurve.genCurve(ctrlP, True, 100, True, zLevel)
        else:
            x, y, z, X, Y, Z = sCurve.genCurve(ctrlP, 200, True, zLevel)
        for i in range(len(X)):
            self.moveArmXYZ(X[i], Y[i],  Z[i])

    # performs a curve, if 0 draws bezier else draws catmull
    def performCurve(self, ctrlP=5, curve=0):
        if curve == 0:  # bezier curve
            x, y, z, X, Y, Z = bCurve.genCurve(ctrlP, True, 100)
        else:
            x, y, z, X, Y, Z = sCurve.genCurve(ctrlP, 10, 200)
        for i in range(len(X)):
            self.moveArmXYZ(X[i], Y[i],  Z[i])

    # Returns to home location
    def moveHome(self):
        lastIndex = dType.SetPTPCmd(
            self.api, dType.PTPMode.PTPMOVLXYZMode, self.homeX, self.homeY, self.homeZ, 0)[0]
        self.commandDelay(lastIndex)

    # Toggles between hover and item level
    def pickToggle(self, itemHeight):
        lastIndex = 0
        positions = dType.GetPose(self.api)
        if(self.picking):
            lastIndex = dType.SetPTPCmd(
                self.api, dType.PTPMode.PTPMOVLXYZMode, positions[0], positions[1], self.homeZ, 0)[0]
            self.picking = False
        else:
            lastIndex = dType.SetPTPCmd(
                self.api, dType.PTPMode.PTPMOVLXYZMode, positions[0], positions[1], itemHeight, 0)[0]
            self.picking = True
        self.commandDelay(lastIndex)
