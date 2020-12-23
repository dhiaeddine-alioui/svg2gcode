from Geometry import *
from utils import distance

class subPath :
    _counter = 0
    def __init__(self,points=None):
        self.points=[]
        if points!=None:
            self.points=points
        subPath._counter+=1
        self.ID=subPath._counter

    def __str__(self):
        output="    SubPath {} has {} points\n".format(self.ID,len(self.points))
        for point in self.points :
            output+="        X={},Y={}\n".format(point.x,point.y)
        return output

    def addPoint(self,point):
        self.points.append(point)

    def getPoints(self):
        return self.points

    def isClosed(self,tolerance):
        return distance(self.points[0],self.points[-1])<tolerance

    def isEmpty(self):
        return len(self.points)==0

    def getMinMaxX(self):
        _min=float("inf")
        _max=0
        for point in self.points :
            _min=min(_min,point.x)
            _max=max(_max,point.x)
        return _min,_max

    def getMinMaxY(self):
        _min=float("inf")
        _max=0
        for point in self.points :
            _min=min(_min,point.y)
            _max=max(_max,point.y)
        return _min,_max
