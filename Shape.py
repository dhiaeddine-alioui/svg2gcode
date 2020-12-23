from Geometry import *
from Skin import *
import numpy as np

class Shape :
    _counter=0
    def __init__(self,path):
        self.wall=path
        self.skin=None
        self.wallColor=None
        self.skinColor=None
        Shape._counter+=1
        self.ID=Shape._counter


    def generateSkin(self,p,state):
        skin=Skin()
        if self.wall.isClosed(p.closeTolerance) :
            minXpath,maxXpath=self.wall.getMinMaxX()
            start=int(minXpath/p.svg_interspace)
            end =int(maxXpath/p.svg_interspace)+1
            samples=np.linspace(start*p.svg_interspace,end*p.svg_interspace,end-start)
            for xDroit in samples :
                line=SkinLine()
                intersectionsPoints=self.wall.intersectionWithVLine(xDroit)
                if len(intersectionsPoints)>0 :
                    if len(intersectionsPoints)%2!=0:
                        state.debugPoints+=intersectionsPoints
                    intersectionsPoints.sort(key=lambda point:point.y)
                    for index in range(0,int(len(intersectionsPoints)/2)) :
                        point1=Point(intersectionsPoints[index*2].x,intersectionsPoints[index*2].y)
                        point2=Point(intersectionsPoints[index*2+1].x,intersectionsPoints[index*2+1].y)
                        line.addSegment(Segment(point1,point2))
                if not line.isEmpty() :
                    skin.addLine(line)
        self.skin=skin

    def codeWall(self,p,state):

        output=""
        output+=";STROKE\n"
        for subpath in self.wall.getSubPaths() :
            subPathPltX=[]
            subPathPltY=[]
            points=subpath.getPoints()
            for svgPoint in points:
                if(svgPoint==points[0]) :
                    output+="G0 Z"+str(p.penUp)+" F300\n"

                reelPoint=svgPoint.calculateReelXY(p)

                subPathPltX.append(reelPoint.x-p.offsetX)
                subPathPltY.append(reelPoint.y-p.offsetY)
                output+="G0 X"+str(round(reelPoint.x,3))+" Y"+str(round(reelPoint.y,3))+" F4200\n"

                if(svgPoint==points[0]) :
                    output+="G0 Z"+str(p.penDown)+" F300\n"
                    state.travelDistances+=(distance(reelPoint,state.lastPosition))
                state.lastPosition=reelPoint

            state.PltX.append(subPathPltX)
            state.PltY.append(subPathPltY)

        return output

    def codeSkin(self,p,state):

        output=""
        if len(self.skin.getLines())==0:
            return ""
        output+=";FILL\n"
        currentLineIndex=0
        direction="leftToRight"
        while True :
            segment = self.skin.linesList[currentLineIndex].getClosetSegment(state)
            if segment != None:
                segmentStartPoint=segment.start.calculateReelXY(p)
                segmentEndPoint=segment.end.calculateReelXY(p)

                if distance(state.lastPosition,segmentEndPoint)<distance(state.lastPosition,segmentStartPoint):
                    __point=segmentEndPoint
                    segmentEndPoint=segmentStartPoint
                    segmentStartPoint=__point

                if distance(state.lastPosition,segmentStartPoint) > p.zHopTolerance or p.alwaysZhop :
                    output+="G0 Z"+str(p.penUp)+" F300\n"
                    output+="G0 X"+str(round(segmentStartPoint.x,3))+" Y"+str(round(segmentStartPoint.y,3))+" F4200\n"
                    output+="G0 Z"+str(p.penDown)+" F300\n"
                    state.travelDistances+=distance(state.lastPosition,segmentStartPoint)
                else :
                    output+="G0 X"+str(round(segmentStartPoint.x,3))+" Y"+str(round(segmentStartPoint.y,3))+" F4200\n"
                output+="G0 X"+str(round(segmentEndPoint.x,3))+" Y"+str(round(segmentEndPoint.y,3))+" F4200\n"
                state.lastPosition=segmentEndPoint
                segment.drawn=True


                state.PltX.append([segmentStartPoint.x-p.offsetX,segmentEndPoint.x-p.offsetX])
                state.PltY.append([segmentStartPoint.y-p.offsetY,segmentEndPoint.y-p.offsetY])


            if direction=="leftToRight" :
                nextLineIndex=self.skin.getNextLinesIdx(currentLineIndex)
                if nextLineIndex==None:
                    direction="rightToLeft"
                    nextLineIndex=self.skin.getPreviousLinesIdx(currentLineIndex)
                    if nextLineIndex==None:
                        break

            if direction=="rightToLeft" :
                nextLineIndex=self.skin.getPreviousLinesIdx(currentLineIndex)
                if nextLineIndex ==None :
                    direction="leftToRight"
                    nextLineIndex=self.skin.getNextLinesIdx(currentLineIndex)
                    if nextLineIndex==None:
                        break
            currentLineIndex=nextLineIndex

        return output

    def __str__(self):
        output=""
        output+="Shape {} \n".format(self.ID)
        if self.wall :
            output+="    Stroke has {} points\n".format(len(self.wall.getPoints()))
        else :
            output+="    No stroke\n"

        if self.skin :
            output+="    Fill has {} lines\n".format(len(self.skin.getLines()))
        else :
            output+="    No fill\n"

        output+="    Color : {}\n".format(self.wallColor)
        return output
