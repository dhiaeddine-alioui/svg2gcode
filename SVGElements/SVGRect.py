from Geometry import *
import re
from Transform import parseTransform
from Path import *
from subPath import *

class SVGRect :
    __ID=0
    def __init__(self,x,y,width,height,transform):
        SVGRect.__ID+=1
        self.ID=SVGRect.__ID
        self.transformString=transform
        self.transform=parseTransform(transform)
        self.x=x
        self.y=y
        self.width=width
        self.height=height

    def renderStroke(self,p):
        points=[]
        points.append(self.transform(Point(self.x,self.y)))
        points.append(self.transform(Point(self.x+self.width,self.y)))
        points.append(self.transform(Point(self.x+self.width,self.y+self.height)))
        points.append(self.transform(Point(self.x,self.y+self.height)))
        points.append(self.transform(Point(self.x,self.y)))
        for point in points :
            p.minX=min(point.x,p.minX)
            p.minY=min(point.y,p.minY)
            p.maxX=max(point.x,p.maxX)
            p.maxY=max(point.y,p.maxY)
        return Path(subpaths=[subPath(points=points)] )

    def toJSON(self):
        shapeJS={}
        shapeJS["type"]="rect"
        shapeJS["ID"]=self.ID
        shapeJS["x"]=self.x
        shapeJS["y"]=self.y
        shapeJS["width"]=self.width
        shapeJS["height"]=self.height
        shapeJS["transform"]=self.transformString
        return shapeJS
