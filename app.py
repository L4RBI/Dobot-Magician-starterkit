

import threading
import DoBotArm as Dbt
import DobotDllType as dType
import bezierCurve as bCurve
import catMullRomCurve as sCurve


# --Main Program--
def main():
    # homeX, homeY, homeZ = 250, 0, 50
    # # Create DoBot Class Object with home position x,y,z
    # ctrlBot = Dbt.DoBotArm(homeX, homeY, homeZ)
    # dType.ClearAllAlarmsState(ctrlBot.api)
    # ctrlBot.moveHome()
    # ctrlBot.moveArmXYZ(250, -200, 40)
    # ctrlBot.toggleSuction()
    # input("DDD")
    # ctrlBot.toggleSuction()

    # ctrlBot.drawCurve(1)

    # # catMullRom
    #x, y, z, X, Y, Z = bCurve.genCurve(nbPoints=5, random=True)
    # for i in range(len(X)):
    #     ctrlBot.moveArmXYZ(X[i], Y[i], Z[i])
    # ctrlBot.moveHome()

    # # catMullRom
    x, y, z, X, Y, Z = sCurve.genCurve(nbPoints=10)
    # for i in range(len(X)):
    #     ctrlBot.moveArmXYZ(X[i], Y[i], Z[i])


main()
