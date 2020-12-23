from Geometry import *

class Path:
    _counter = 0
    def __init__(self,subpaths=None):
        self.subPaths=[]
        if subpaths!=None:
            self.subPaths=subpaths
        self.color=0
        Path._counter+=1
        self.ID=Path._counter

    def __str__(self):
        output="Path {} has {} subPaths\n".format(self.ID,len(self.subPaths))
        for subpath in self.subPaths :
            output+=subpath.__str__()
        return output

    def addSubPath(self,subpath):
        self.subPaths.append(subpath)

    def getPoints(self):
        points=[]
        for subpath in self.subPaths:
            points+=subpath.getPoints()
        return points

    def getSubPaths(self):
        return self.subPaths

    def intersectionWithVLine(self,lineX):
        intersections=[]
        for subpath in self.subPaths:
            points=subpath.getPoints()
            for index,_ in enumerate(points) :
                point1=points[index-1]
                point2=points[index]
                if point1.x == point2.x :
                    continue
                if point2.x>=lineX and point1.x<lineX \
                or point2.x>lineX and point1.x<=lineX \
                or point2.x<=lineX and point1.x>lineX \
                or point2.x<lineX and point1.x>=lineX :
                    a=None
                    if point2.x>=lineX and point1.x<lineX \
                    or point2.x>lineX and point1.x<=lineX :
                        a=(point2.y-point1.y)/(point2.x-point1.x)
                    if point2.x<=lineX and point1.x>lineX \
                    or point2.x<lineX and point1.x>=lineX :
                        a=(point1.y-point2.y)/(point1.x-point2.x)
                    b= point2.y-(a*point2.x)
                    xInter=lineX
                    yInter=a*lineX+b
                    #Check that this is really a new intersection point
                    newInterPoint=True
                    """for _point in intersections :
                        if distance(_point,Point(xInter,yInter))<0.01 :
                            newInterPoint=False
                            break"""
                    if newInterPoint :
                        intersections.append(Point(xInter,yInter))
        return intersections

    def isEmpty(self):
        return len(self.subPaths)==0

    def isClosed(self,tolerance):
        return all([subpath.isClosed(tolerance) for subpath in self.subPaths])


    def getMinMaxX(self):
        _min=float("inf")
        _max=0
        for subPath in self.subPaths :
            __min,__max=subPath.getMinMaxX()
            _min=min(_min,__min)
            _max=max(_max,__max)
        return _min,_max

    def getMinMaxY(self):
        _min=float("inf")
        _max=0
        for subPath in self.subPaths :
            __min,__max=subPath.getMinMaxY()
            _min=min(_min,__min)
            _max=max(_max,__max)
        return _min,_max
