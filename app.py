

import threading
import DoBotArm as Dbt
import DobotDllType as dType
import bezierCurve as bCurve
import catMullRomCurve as sCurve


# --Main Program--
def main():
    homeX, homeY, homeZ = 250, 0, 50
    # Create DoBot Class Object with home position x,y,z
    ctrlBot = Dbt.DoBotArm(homeX, homeY, homeZ)
    # important to clear the alarms and errors
    dType.ClearAllAlarmsState(ctrlBot.api)
    ctrlBot.moveHome()
    ctrlBot.moveArmXYZ(250, -200, 40)

    # # bezier curve
    # ctrlBot.performCurve(ctrlP=4, curve=0) # perfoms the trajectory in 3D space
    # ctrlBot.drawCurve(ctrlP=4, curve=0) # draws the curve on a 2D support

    # # catMullRom
    # ctrlBot.performCurve(ctrlP=10, curve=1)  # perfoms the trajectory in 3D space
    # ctrlBot.drawCurve(ctrlP=10, curve=1) # draws the curve on a 2D support


main()
