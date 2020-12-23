import numpy as np
import math
from Geometry import *
import re
from Transform import parseTransform
from Path import *
from subPath import *

class SVGCircle :
    __ID=0
    def __init__(self,cx,cy,r,transform):
        SVGCircle.__ID+=1
        self.ID=SVGCircle.__ID
        self.transformString=transform
        self.cx=cx
        self.cy=cy
        self.r=r
        self.transform=parseTransform(transform)

    def renderStroke(self,p):
        points=[]
        for t in np.linspace(-math.pi,math.pi,360):
            x=self.r*math.cos(t)+self.cx
            y=self.r*math.sin(t)+self.cy
            point=self.transform(Point(x,y))
            p.minX=min(point.x,p.minX)
            p.minY=min(point.y,p.minY)
            p.maxX=max(point.x,p.maxX)
            p.maxY=max(point.y,p.maxY)
            points.append(point)
        return Path(subpaths=[subPath(points=points)] )

    def toJSON(self):
        shapeJS={}
        shapeJS["type"]="circle"
        shapeJS["ID"]=self.ID
        shapeJS["cx"]=self.cx
        shapeJS["cy"]=self.cy
        shapeJS["r"]=self.r
        shapeJS["transform"]=self.transformString
        return shapeJS
