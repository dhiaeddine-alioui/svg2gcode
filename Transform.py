import re
from Geometry import *
import math

def translation_decorator(xTranslation,yTranslation):
    def translation(point):
        return Point(point.x+float(xTranslation),point.y+float(yTranslation))
    return translation

def rotate_decorator(cx,cy,rot):
    if rot ==None :
        return identity
    else :
        def rotate(point):
             angle = rot*math.pi/180
             xM=point.x-cx
             yM=point.y-cy
             x=xM*math.cos(angle)+yM*math.sin(angle)+cx
             y=-xM*math.sin(angle)+yM*math.cos(angle)+cy
             return Point(x,y)
        return rotate

def identity(point):
    return point


def parseTransform(transform):
    translation=identity
    rotation=identity
    skewX=identity
    scale=identity

    if "translate" in transform:
        parameters=re.findall(r"translate\(([-+]?[0-9]*\.?[0-9]*)?[ ]?([-+]?[0-9]*\.?[0-9]*)?\)",transform)
        if parameters[0][0]!='' and parameters[0][1]!='':
            _x=float(parameters[0][0])
            _y=float(parameters[0][1])
            translation=translation_decorator(_x,_y)

    if "rotate" in transform:
        parameters=re.findall(r"rotate\(([-+]?[0-9]*\.?[0-9]*)?[ ]?([-+]?[0-9]*\.?[0-9]*)?[ ]?([-+]?[0-9]*\.?[0-9]*)?\)",transform)
        cx=0
        cy=0
        rot=None

        if parameters[0][0]!='':
            rot=-float(parameters[0][0])
        if parameters[0][1]!='':
            cx=float(parameters[0][1])
        if parameters[0][2]!='':
            cy=float(parameters[0][2])

        rotation=rotate_decorator(cx,cy,rot)

    def finalTransformation(point):
        return translation(rotation(skewX(scale(point))))

    return finalTransformation
