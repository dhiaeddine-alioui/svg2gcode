from Geometry import *

class SkinLine:
    def __init__(self):
        self.segmentsList=[]
        self.index=None

    def isDrawn(self):
        return all([seg.drawn for seg in self.segmentsList])

    def isEmpty(self):
        return len(self.segmentsList)==0

    def addSegment(self,segment):
        self.segmentsList.append(segment)
    def getSegments(self):
        return self.segmentsList

    def sortLine(self,order):
        for seg in self.segmentsList :
            seg.sortSegment(order)

        if order==1 : #ASC
            self.segmentsList.sort(key=lambda segment:segment.start.y)
        if order==-1 : #DESC
            self.segmentsList.sort(key=lambda segment:segment.start.y,reverse=True)
    def __str__(self):
        output=""
        output+="    LINE: has "+str(len(self.segmentsList))+" segments\n"
        for seg in self.segmentsList :
            output+=seg.__str__()
        return output

    def getClosetSegment(self,state):
        minDistance=float('inf')
        closestSegment=None
        for segment in self.segmentsList:
            if not segment.drawn :
                if distance(state.lastPosition,segment.start) < minDistance or distance(state.lastPosition,segment.end) < minDistance :
                    minDistance=min(distance(state.lastPosition,segment.start),distance(state.lastPosition,segment.end))
                    closestSegment=segment

        return closestSegment


class Skin:
    def __init__(self):
        self.linesList=[]

    def addLine(self,line):
        self.linesList.append(line)

    def getLines(self):
        return self.linesList

    def getNextLinesIdx(self,index):
        if index>len(self.linesList)-2 or index<0:
            return None
        else :
            for i in range(index+1,len(self.linesList)) :
                if not self.linesList[i].isDrawn() :
                    return i
            return None

    def getPreviousLinesIdx(self,index):
        if index>len(self.linesList)-1 or index<1:
            return None
        else :
            for i in range(index-1,-1,-1) :
                if not self.linesList[i].isDrawn() :
                    return i
            return None

    def __str__(self):
        output=""
        output+="SKIN: has "+str(len(self.linesList))+" lines\n"
        for line in self.linesList :
            output+=line.__str__()
        return output
