from xml.dom import minidom
import numpy as np
import math
from Geometry import *
from SVGElements.SVGCircle import *
from SVGElements.SVGPath import *
from SVGElements.SVGPolygon import *
from SVGElements.SVGRect import *
from Shape import *

def getEndCode(p):
    CR="\n"
    endCode=";End code"+CR
    endCode+="G0 Z{} F300".format(p.penUp)+CR
    endCode+="G0 X0 Y230 F4200"+CR
    return endCode

def getStartCode(p):
    CR="\n"
    startCode=";Start code"+CR
    startCode+="G28 X Y Z F4200"+CR
    startCode+="G21"+CR
    return startCode

def parseSVGfile(svgfilepath):
    # read the SVG file and extract the SVG Shapes (rect,circle,path,polygon,...)
    try :
        doc = minidom.parse(svgfilepath)
    except :
        print("Error ! File does not exist ! ")
        exit()

    SVGPath.ID=0
    SVGCircle.ID=0
    SVGRect.ID=0
    SVGPolygon.ID=0
    svg_shapes=[]
    svg_shapes+= [SVGPath(path.getAttribute('d'),
                         path.getAttribute('transform'))
                         for path in doc.getElementsByTagName('path')]

    svg_shapes+=[SVGCircle( float(circle.getAttribute('cx')),
                            float(circle.getAttribute('cy')),
                            float(circle.getAttribute('r')),
                            circle.getAttribute('transform')  )
                            for circle in doc.getElementsByTagName('circle')]

    svg_shapes+=[SVGPolygon(polygon.getAttribute('points'),
                             polygon.getAttribute('transform'))
                             for polygon in doc.getElementsByTagName('polygon')]

    svg_shapes+=[SVGRect(float(rect.getAttribute('x')),
                       float(rect.getAttribute('y')),
                       float(rect.getAttribute('width')),
                       float(rect.getAttribute('height')),
                       rect.getAttribute('transform'))
                       for rect in doc.getElementsByTagName('rect')]
    doc.unlink()
    return svg_shapes


def parseJSShapes(SVGshapes,p,state):
    #input : SVGshapes instances of SVGElements
    #output : Shapes instances of Shape Class with all parameters ready to be coded
    shapes=[]
    for SVGshape in SVGshapes:
        shape=Shape(parseSingleJSShape(SVGshape,p))
        shape.wallColor=SVGshape["color"]
        shape.skinColor=SVGshape["color"]
        if SVGshape["fill"] :
            shape.generateSkin(p,state)
        if not SVGshape["stroke"] :
            shape.wall=None
        shapes.append(shape)

    return shapes

def parseSingleJSShape(SVGShapeJS,p):
    #Input : SVG Shape in JS object
    #ouput : Path object containing the parsed SVG Shape
    SVGshape=None
    if SVGShapeJS["type"]=="path":
        SVGshape=SVGPath(SVGShapeJS["d"],SVGShapeJS["transform"])
    if SVGShapeJS["type"]=="circle":
        SVGshape=SVGCircle( float(SVGShapeJS["cx"]),
                            float(SVGShapeJS["cy"]),
                            float(SVGShapeJS["r"]),
                            SVGShapeJS["transform"])
    if SVGShapeJS["type"]=="rect":
        SVGshape=SVGRect(float(SVGShapeJS["x"]),
                         float(SVGShapeJS["y"]),
                         float(SVGShapeJS["width"]),
                         float(SVGShapeJS["height"]),
                         SVGShapeJS["transform"])
    if SVGShapeJS["type"]=="polygon":
        SVGshape=SVGPolygon(SVGShapeJS["points"],SVGShapeJS["transform"])

    return SVGshape.renderStroke(p)


def getPauseCode(pauseX,pauseY,penPosition,p,state) :
    output=""
    output+=";PAUSE\n"
    output+="G0 Z{} F300\n".format(p.penUp+2)
    output+="G0 X{} Y{} F7200\n".format(pauseX,pauseY)
    output+="G0 Z{} F300\n".format(penPosition)
    output+="M0\n"
    state.lastPosition=Point(pauseX,pauseY)
    return output

class State:
    def __init__(self):
        self.lastPosition=Point(0,0)
        self.travelDistances=0
        self.PltX=[]
        self.PltY=[]
        self.debugPoints=[]

class Parameters :
    def __init__(self):
        self.minX=float('inf')
        self.maxX=0
        self.minY=float('inf')
        self.maxY=0
        self.offsetX=None
        self.offsetY=None
        self.bedXdim=None
        self.bedYdim=None
        self.sizeFactor=1
        self.penUp=None
        self.penDown=None
        self.xFlip=False
        self.yFlip=True
        self.bedRatio=None
        self.svgRatio=None
        self.topMargin=None
        self.bottomMargin=None
        self.leftMargin=None
        self.rightMargin=None
        self.availableXdim=None
        self.availableYdim=None
        self.real_interspace=None
        self.scale=None
        self.svg_interspace=None
        self.alwaysZhop=False
        self.closeTolerance=None
        self.zHopTolerance=None

    def setMargins(self,top,bot,left,right):
        self.topMargin=top
        self.bottomMargin=bot
        self.leftMargin=left
        self.rightMargin=right
        self.availableXdim=self.bedXdim-self.offsetX-self.leftMargin-self.rightMargin
        self.availableYdim=self.bedYdim-self.offsetY-self.topMargin-self.bottomMargin

    def setReelInterspace(self,interspace):
        self.real_interspace=interspace
        maxPoint=Point(self.maxX,0).calculateReelXY(self)
        minPoint=Point(self.minX,0).calculateReelXY(self)
        self.svg_interspace=((self.maxX-self.minX)/(maxPoint.x-minPoint.x))*self.real_interspace

    def __str__(self):
        output=""
        output+="Parameters :\n"
        output+="  minX={}".format(self.minX)+"\n"
        output+="  maxX={}".format(self.maxX)+"\n"
        output+="  minY={}".format(self.minY)+"\n"
        output+="  maxY={}".format(self.maxY)+"\n"
        output+="  offsetX={}".format(self.offsetX)+"\n"
        output+="  offsetY={}".format(self.offsetY)+"\n"
        output+="  bedXdim={}".format(self.bedXdim)+"\n"
        output+="  bedYdim={}".format(self.bedYdim)+"\n"
        output+="  sizeFactor={}".format(self.sizeFactor)+"\n"
        output+="  penUp={}".format(self.penUp)+"\n"
        output+="  penDown={}".format(self.penDown)+"\n"
        output+="  xFlip={}".format(self.xFlip)+"\n"
        output+="  yFlip={}".format(self.yFlip)+"\n"
        output+="  bedRatio={}".format(self.bedRatio)+"\n"
        output+="  svgRatio={}".format(self.svgRatio)+"\n"
        output+="  topMargin={}".format(self.topMargin)+"\n"
        output+="  bottomMargin={}".format(self.bottomMargin)+"\n"
        output+="  leftMargin={}".format(self.leftMargin)+"\n"
        output+="  rightMargin={}".format(self.rightMargin)+"\n"
        output+="  availableXdim={}".format(self.availableXdim)+"\n"
        output+="  availableYdim={}".format(self.availableYdim)+"\n"
        output+="  real_interspace={}".format(self.real_interspace)+"\n"
        output+="  scale={}".format(self.scale)+"\n"
        output+="  svg_interspace={}".format(self.svg_interspace)+"\n"
        output+="  alwaysZhop={}".format(self.alwaysZhop)+"\n"
        output+="  closeTolerance={}".format(self.closeTolerance)+"\n"
        output+="  zHopTolerance={}".format(self.zHopTolerance)+"\n"
        return output
