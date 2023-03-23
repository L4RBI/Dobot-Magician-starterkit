import numpy as np
import matplotlib.pyplot as plt


def genCurve(nbPoints=3, random=False, smoothness=100, draw=False, zLevel=None):
    if draw and zLevel != None:  # in case the curve needs to be drawn on a peper/support
        # init the x coordinates of the control points randomly
        x = np.random.uniform(low=180, high=250, size=(nbPoints,))
        # init the y coordinates of the control points randomly
        y = np.random.uniform(low=-200, high=200, size=(nbPoints,))
        # init the z coordinates of the control points to the level of the paper/support
        z = np.full((nbPoints,), zLevel)
    else:
        if(random):  # in the case where the movement will be done in 3Dspace/ üerformed by the robotic arm
            # init the x coordinates of the control points randomly
            x = np.random.uniform(low=180, high=250, size=(nbPoints,))
            # init the y coordinates of the control points randomly
            y = np.random.uniform(low=-200, high=200, size=(nbPoints,))
            # init the z coordinates of the control points randomly
            z = np.random.uniform(low=0, high=60, size=(nbPoints,))
        else:  # a manually set example of a quadratic bezier curve
            x = np.array([90, 280, 60])
            y = np.array([260, 0, -280])
            z = np.array([0, 100, 40])

    CELLS = smoothness  # the number of segments used to draw the curve

    nCP = nbPoints  # number of control points
    n = nCP - 1  # the order of the polynomes
    i = 0
    t = np.linspace(0, 1, CELLS)  # the iterations of t through time
    b = []
    xBezier = np.zeros((1, CELLS))  # init the x coordinates of the curve
    yBezier = np.zeros((1, CELLS))  # init the y coordinates of the curve
    zBezier = np.zeros((1, CELLS))  # init the z coordinates of the curve
    for j in range(0, nCP):  # performing the calculation and the populating of the curve
        b.append(Bernstien(n, i, t))
        xBezier = Bernstien(n, i, t) * x[j] + xBezier
        yBezier = Bernstien(n, i, t) * y[j] + yBezier
        zBezier = Bernstien(n, i, t) * z[j] + zBezier
        i = i + 1
    xBezier = xBezier.flatten()
    yBezier = yBezier.flatten()
    zBezier = zBezier.flatten()

    for line in b:  # plot the bernstein polynomials
        plt.plot(t, line)
    plt.show()

    # plots the curve in 3D space
    fig1 = plt.figure(figsize=(4, 4))
    ax1 = fig1.add_subplot(111, projection="3d")
    ax1.scatter(x, y, z, c="black")
    ax1.plot(xBezier, yBezier, zBezier, c="blue")
    plt.show()
    fig1.savefig('BezierCurve.png')
    return x, y, z, xBezier, yBezier, zBezier


def Ni(n, i):
    return np.math.factorial(n) / (np.math.factorial(i)*np.math.factorial(n - i))


def Bernstien(n, i, t):
    return np.array(Ni(n, i)*(t**i)*(1-t) ** (n-i))
