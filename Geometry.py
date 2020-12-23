import math

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __str__(self):
        return "X="+str(self.x)+",Y="+str(self.y)

    def calculateReelXY(self,p):

        def calculateX(x):
            if p.svgRatio>p.bedRatio : #Fitting to Y dimension
                return (((x-p.minX)/(p.maxX-p.minX))*(p.availableYdim/p.svgRatio)*p.sizeFactor)+p.offsetX+p.leftMargin
            else : #Fitting to X dimension
                return ((((x-p.minX)/(p.maxX-p.minX))*(p.availableXdim)*p.sizeFactor))+p.offsetX+p.leftMargin

        def calculateY(y):
            if p.svgRatio>p.bedRatio : #Fitting to Y dimension
                return ((((y-p.minY)/(p.maxY-p.minY))*(p.availableYdim)*p.sizeFactor))+p.offsetY+p.bottomMargin
            else : #Fitting to X dimension
                return (((y-p.minY)/(p.maxY-p.minY))*(p.availableXdim*p.svgRatio)*p.sizeFactor)+p.offsetY+p.bottomMargin

        x=calculateX(self.x)
        y=calculateY(self.y)

        if p.xFlip :
            x=calculateX(p.maxX)-x+p.offsetX+p.leftMargin
        if p.yFlip :
            y=calculateY(p.maxY)-y+p.offsetY+p.bottomMargin

        return Point(x,y)

class Segment:
    def __init__(self,point1,point2):
        self.start=point1
        self.end=point2
        self.drawn=False

    def length(self):
        return distance(self.start,self.point2)

    def sortSegment(self,order):
        if (order==1 and self.start.y>self.end.y) or (order==-1 and  self.start.y<self.end.y):
                aux=self.start
                self.start=self.end
                self.end=aux
    def __str__(self):
        return "        SEGMENT: X1="+str(self.start.x)+" Y1="+str(self.start.y)+" : X2="+str(self.end.x)+" , Y2="+str(self.end.x)+"\n"

def distance(point1,point2):
    return (math.sqrt(pow((point2.x-point1.x),2)+pow((point2.y-point1.y),2)))
