import numpy as np
from Geometry import *

# returns the general Bezier cubic formula given 4 control points
def get_cubic(a, b, c, d):
    return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * t * b + 3 * (1 - t) * np.power(t, 2) * c + np.power(t, 3) * d

# evalute each cubic curve on the range [0, 1] sliced in n points
def evaluate_bezier(P0,P1,P2,P3,n):
    xCurve = get_cubic(P0.x,P1.x,P2.x,P3.x)
    yCurve = get_cubic(P0.y,P1.y,P2.y,P3.y)
    return [Point(xCurve(t),yCurve(t)) for t in np.linspace(0,1,n)]
