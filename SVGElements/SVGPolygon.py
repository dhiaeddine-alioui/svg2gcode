from Geometry import *
import re
from Transform import parseTransform
from Path import *
from subPath import *

class SVGPolygon :
    __ID=0
    def __init__(self,points,transform):
        SVGPolygon.__ID+=1
        self.ID=SVGPolygon.__ID
        self.transformString=transform
        self.transform=parseTransform(transform)
        self.points=points

    def renderStroke(self,p):
        points=[]
        xyList=re.findall(r"[-+]?\d*\.\d+|\d+",self.points)
        if len(xyList)%2!=0:
            print("Error in parsing polygon !!")
            exit()
        else :
            for index in range(0,int(len(xyList)/2)) :
                point=self.transform(Point(float(xyList[index*2]),
                                                   float(xyList[index*2+1]) ))
                p.minX=min(point.x,p.minX)
                p.minY=min(point.y,p.minY)
                p.maxX=max(point.x,p.maxX)
                p.maxY=max(point.y,p.maxY)
                points.append(point)
        return Path(subpaths=[subPath(points=points)] )

    def toJSON(self):
        shapeJS={}
        shapeJS["type"]="polygon"
        shapeJS["ID"]=self.ID
        shapeJS["points"]=self.points
        shapeJS["transform"]=self.transformString
        return shapeJS
