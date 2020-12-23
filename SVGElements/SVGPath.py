import numpy as np
from svg.path import parse_path
from svg.path.path import Line,CubicBezier,Move,Arc,Close,QuadraticBezier
from cubicbezier import evaluate_bezier
from arc import *
import math
from Geometry import *
from subPath import *
from Path import *
import re
from Transform import parseTransform

class SVGPath :
    __ID=0
    def __init__(self,path,transform):
        SVGPath.__ID+=1
        self.ID=SVGPath.__ID
        self.transformString=transform
        self.pathString=path
        self.transform=parseTransform(transform)

    def renderStroke(self,p):
        parsed_path = parse_path(self.pathString)
        result_path=Path()
        result_subpath=subPath()
        for e in parsed_path:
            previousX1=None
            previousY1=None
            if isinstance(e, Line):
                point1=self.transform(Point(e.start.real,e.start.imag))
                point2=self.transform(Point(e.end.real,e.end.imag))
                p.minX=min(point1.x,point2.x,p.minX)
                p.minY=min(point1.y,point2.y,p.minY)
                p.maxX=max(point1.x,point2.x,p.maxX)
                p.maxY=max(point1.y,point2.y,p.maxY)
                if not previousX1==point1.x and not previousY1==point1.y :
                    result_subpath.addPoint(point1)
                result_subpath.addPoint(point2)
                previousX1=point1.x
                previousY1=point1.y
            elif isinstance(e, CubicBezier):
                P0x=e.start.real
                P0y=e.start.imag
                P1x=e.control1.real
                P1y=e.control1.imag
                P2x=e.control2.real
                P2y=e.control2.imag
                P3x=e.end.real
                P3y=e.end.imag
                rendred_points = evaluate_bezier(Point(P0x,P0y),Point(P1x,P1y),Point(P2x,P2y),Point(P3x,P3y), 20)
                for rendred_point in rendred_points :
                    point=self.transform(Point(rendred_point.x,rendred_point.y))
                    p.minX=min(point.x,p.minX)
                    p.minY=min(point.y,p.minY)
                    p.maxX=max(point.x,p.maxX)
                    p.maxY=max(point.y,p.maxY)
                    result_subpath.addPoint(point)
            elif isinstance(e, QuadraticBezier):
                P0x=e.start.real
                P0y=e.start.imag
                P1x=e.control.real
                P1y=e.control.imag
                P2x=P1x
                P2y=P1y
                P3x=e.end.real
                P3y=e.end.imag
                rendred_points = evaluate_bezier(Point(P0x,P0y),Point(P1x,P1y),Point(P2x,P2y),Point(P3x,P3y), 20)
                for rendred_point in rendred_points :
                    point=self.transform(Point(rendred_point.x,rendred_point.y))
                    p.minX=min(point.x,p.minX)
                    p.minY=min(point.y,p.minY)
                    p.maxX=max(point.x,p.maxX)
                    p.maxY=max(point.y,p.maxY)
                    result_subpath.addPoint(point)
            elif isinstance(e, Arc):
                rendred_points=evalute_arc(e.start.real,
                                           e.start.imag,
                                           e.end.real,
                                           e.end.imag,
                                           e.arc,
                                           e.sweep,
                                           e.radius.real,
                                           e.radius.imag,
                                           e.rotation)
                for rendred_point in rendred_points :
                    point=self.transform(Point(rendred_point[0],rendred_point[1]))
                    p.minX=min(point.x,p.minX)
                    p.minY=min(point.y,p.minY)
                    p.maxX=max(point.x,p.maxX)
                    p.maxY=max(point.y,p.maxY)
                    result_subpath.addPoint(point)

            elif isinstance(e, Move):
                result_subpath=subPath()
                point=self.transform(Point(e.end.real,e.end.imag))
                p.minX=min(point.x,p.minX)
                p.minY=min(point.y,p.minY)
                p.maxX=max(point.x,p.maxX)
                p.maxY=max(point.y,p.maxY)
                result_subpath.addPoint(point)
            elif isinstance(e, Close):
                point=self.transform(Point(e.end.real,e.end.imag))
                p.minX=min(point.x,p.minX)
                p.minY=min(point.y,p.minY)
                p.maxX=max(point.x,p.maxX)
                p.maxY=max(point.y,p.maxY)
                result_subpath.addPoint(point)
                result_path.addSubPath(result_subpath)
                result_subpath=subPath()
            else :
                print(e)
        if not result_subpath.isEmpty():
            result_path.addSubPath(result_subpath)
        if not result_path.isEmpty():
            return(result_path)

    def toJSON(self):
        shapeJS={}
        shapeJS["type"]="path"
        shapeJS["ID"]=self.ID
        shapeJS["d"]=self.pathString
        shapeJS["transform"]=self.transformString
        return shapeJS
