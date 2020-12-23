from numpy import cos,sin,arccos
import numpy as np
import math
from Geometry import *


#Implementation of the algorithme from https://www.w3.org/TR/SVG11/implnote.html#ArcImplementationNotes

def angle_between_vects(v1,v2):
    if v1[0][0]*v2[1][0]-v1[1][0]*v2[0][0] >= 0 :
        return arccos((np.dot(np.transpose(v1),v2))/(norme2(v1)*norme2(v2)))
    else :
        return -arccos((np.dot(np.transpose(v1),v2))/(norme2(v1)*norme2(v2)))


def norme2(v):
    return math.sqrt(pow(v[0][0],2)+pow(v[1][0],2))

def get_arc_parameters(x1,y1,x2,y2,fa,fs,rx,ry,rot):
    rot = (rot*math.pi)/180
    M1=np.array([[math.cos(rot),math.sin(rot)],[-math.sin(rot),math.cos(rot)]])
    V1=np.array([[(x1-x2)/2],[(y1-y2)/2]])
    Vaux1=np.dot(M1,V1)
    #print("Shape of M1=",M1.shape,"\n")
    #print("Shape of V1=",V1.shape,"\n")
    #print("Shape of Vaux1=",Vaux1.shape,"\n")

    _x1=Vaux1[0][0]
    _y1=Vaux1[1][0]
    try :
        _Coef=math.sqrt(   (     pow(rx,2)*pow(ry,2)  -  pow(rx,2)*pow(_y1,2)   -   pow(ry,2)*pow(_x1,2))/\
                       (     pow(rx,2)*pow(_y1,2)   +   pow(ry,2)*pow(_x1,2))       )
    except ValueError :
        print("Arc not rendered !\n")
        return None,None,None,None

    if fa==fs:
        _Coef*=-1
    _C=_Coef*np.array([[(rx*_y1)/ry],[(-ry*_x1)/rx]])
    #print("Shape of _C=",_C.shape,"\n")
    _Cx=_C[0][0]
    _Cy=_C[1][0]
    C=np.dot(np.array([[math.cos(rot),-math.sin(rot)],[math.sin(rot),math.cos(rot)]]),np.array([[_Cx],[_Cy]]))+np.array([[(x1+x2)/2],[(y1+y2)/2]])
    #print("Shape of C=",C.shape,"\n")
    theta1=angle_between_vects(
                np.array([[1],[0]]),\
                np.array([[(_x1-_Cx)/rx],[(_y1-_Cy)/ry]])\
                )

    deltaTheta=angle_between_vects(
                np.array([[(_x1-_Cx)/rx],[(_y1-_Cy)/ry]]),\
                np.array([[(-_x1-_Cx)/rx],[(-_y1-_Cy)/ry]])\
    )
    #print("Shape of deltaTheta=",deltaTheta.shape,"\n")
    theta1=theta1[0][0]
    deltaTheta=deltaTheta[0][0]
    deltaTheta=deltaTheta%(math.pi*2)

    if fs==0 and deltaTheta>0 :
        deltaTheta-=(math.pi*2)
    elif fs==1 and deltaTheta<0 :
        deltaTheta+=(math.pi*2)
    return C[0][0],C[1][0],theta1,deltaTheta

def evalute_arc(x1,y1,x2,y2,fa,fs,rx,ry,rot):

    if rx==0 or ry==0 :
        print("Rx or ry ==0 !!")
        return([[x1,y1],[x2,y2]])

    Cx,Cy,Theta,Delta=get_arc_parameters(x1,y1,x2,y2,fa,fs,rx,ry,rot)
    #print("Cx= {}, Cy={}, Theta={}, Delta={}\n".format(Cx,Cy,Theta,Delta))

    if not Cx and not Cy and not Theta and not Delta  :
        return([[x1,y1],[x2,y2]])

    points=[]
    M=np.array([[math.cos(rot),-math.sin(rot)],[math.sin(rot),math.cos(rot)]])
    C=np.array([[Cx],[Cy]])
    for t in np.linspace(Theta,Theta+Delta,int((abs(Delta)*180)/math.pi)):
        V=np.array([[rx*math.cos(t)],[ry*math.sin(t)]])
        P=np.dot(M,V)+C
        points.append([P[0][0],P[1][0]])
    return np.array([[p[0],p[1]] for p in points])
