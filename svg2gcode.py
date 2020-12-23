import numpy as np
import matplotlib.pyplot as plt
import argparse
import math
from utils import *
from Skin import *
from Shape import *
import progressbar

from pylab import rcParams
rcParams['figure.figsize'] = 5,5

parser = argparse.ArgumentParser()
parser.add_argument("SVGFile", help="Put the SVG input file")
args = parser.parse_args()


p=Parameters()
p.offsetX=43
p.offsetY=18
p.bedXdim=230
p.bedYdim=230
p.sizeFactor=1
p.penUp=20
p.penDown=18
p.xFlip=False
p.yFlip=True
p.setMargins(top=0,bot=5,left=5,right=0)
p.scale=1
p.closeTolerance=2 #2mm

#parse SVG file
paths=parseSVG(args.SVGFile,p)
p.bedRatio=p.availableYdim/p.availableXdim
p.svgRatio=(p.maxY-p.minY)/(p.maxX-p.minX)

p.setReelInterspace(0.5)
p.zHopTolerance=2*p.real_interspace
p.alwaysZhop=False

CR="\n"
startCode=";Start code"+CR
startCode+="G28 X Y Z F4200"+CR
startCode+="G21"+CR
startCode+="G0 Z{} F4200".format(p.penUp+5)+CR
startCode+="G0 X{} Y{}".format(p.offsetX+5,p.offsetY+5)+CR
startCode+="G0 Z{} F4200".format(p.penDown)+CR
startCode+="M0\n"
startCode+="G0 Z{} F4200".format(p.penUp)+CR

endCode=";End code"+CR
endCode+="G0 Z20 F300"+CR
endCode+="G0 X0 Y230 F4200"+CR

penCode=";Pen Code"+CR
penCode+="G0 Z{} F300".format(p.penUp)+CR
penCode+="G0 X{} Y{} F7200".format(p.offsetX,p.offsetY)+CR
penCode+="G0 Z{} F300".format(p.penDown-3)+CR
penCode+="G0 Z{} F300".format(p.penUp)+CR


shapes=[]
for path in paths:
    shapes.append(Shape(path))

print(p)
state=State()
finalOutput=""

#Generate Hatching
bar = progressbar.ProgressBar(maxval=len(shapes), \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
print("Generating skins : ")
bar.start()
for index,shape in enumerate(shapes) :
    bar.update(index)
    shape.generateSkin(p,state)
bar.finish()

#Coding walls
bar = progressbar.ProgressBar(maxval=len(shapes), \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
print("Coding walls : ")
bar.start()
for index,shape in enumerate(shapes):
    bar.update(index)
    #finalOutput+=penCode
    finalOutput+=shape.codeWall(p,state)
bar.finish()

finalOutput+=getPauseCode(p.offsetX+2,p.offsetY+2,p.penDown,p,state)
#Coding skin hatching
bar = progressbar.ProgressBar(maxval=len(shapes), \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
print("Coding skins : ")
bar.start()
for index,shape in enumerate(shapes):
    bar.update(index)
    finalOutput+=shape.codeSkin(p,state)
bar.finish()

with open(args.SVGFile+".gcode","w") as file:
    file.write(startCode)
    file.write(finalOutput)
    file.write(endCode)





print("The travel distance is : ",state.travelDistances)
plt.axis([0, 230, 0, 230])
plt.vlines(230-p.offsetX,ymin=0,ymax=230,linestyles='dashed')
plt.vlines(230-p.offsetX-p.rightMargin,ymin=0,ymax=230,linestyles='dashed',color='red')
plt.vlines(p.leftMargin,ymin=0,ymax=230,linestyles='dashed',color='red')
plt.hlines(230-p.offsetY,xmin=0,xmax=230,linestyles='dashed')
plt.hlines(230-p.offsetY-p.topMargin,xmin=0,xmax=230,linestyles='dashed',color='red')
plt.hlines(p.bottomMargin,xmin=0,xmax=230,linestyles='dashed',color='red')
for index in range(0,len(state.PltX)):
    plt.plot(state.PltX[index],state.PltY[index],'b',linewidth="0.5")

debugPointsX=[]
debugPointsY=[]
for point in state.debugPoints :
    reelPoint=point.calculateReelXY(p)
    debugPointsX.append(reelPoint.x-p.offsetX)
    debugPointsY.append(reelPoint.y-p.offsetY)
plt.plot(debugPointsX,debugPointsY, 'ro',markersize="1")
#plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)"""
plt.show()
