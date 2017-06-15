from graphics import *

def boxIntersect(aRight,aLeft,aTop,aBottom,bRight,bLeft,bTop,bBottom):
    seperate = aRight<bLeft or aLeft>bRight or aTop>bBottom or aBottom<bTop
    return not seperate

def leftIntersect(aLeft,aTop,aBottom,bRight,bLeft,bTop,bBottom):
    seperate = aLeft<bLeft or aLeft>bRight or aTop>bBottom or aBottom<bTop
    return not seperate

def rightIntersect(aRight,aTop,aBottom,bRight,bLeft,bTop,bBottom):
    seperate = aRight<bLeft or aRight>bRight or aTop>bBottom or aBottom<bTop
    return not seperate

def topIntersect(aRight,aLeft,aTop,bRight,bLeft,bTop,bBottom):
    seperate = aRight<bLeft or aLeft>bRight or aTop>bBottom or aTop<bTop
    return not seperate

def bottomIntersect(aRight,aLeft,aBottom,bRight,bLeft,bTop,bBottom):
    seperate = aRight<bLeft or aLeft>bRight or aBottom>bBottom or aBottom<bTop
    return not seperate

def inbox(boxx,boxy,pointx,pointy,boxwidth=50,boxheight=50):
    if pointx>=boxx and pointx<=boxx+boxwidth:
        if pointy>=boxy and pointy<=boxy+boxheight:
            return True
        else:
            return False
    else:
        return False

def inimage(pointx,pointy,imgx,imgy,img):
    width,height=getImageWidth(img)/2,getImageHeight(img)/2
    if pointx>=imgx-width and pointx<=imgx+width:
        if pointy>=imgy-height and pointy<=imgy+height:
            return True
    return False

def distance(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**.5

def radiusIntersect(x1,y1,x2,y2,r1,r2):
    if distance(x1,y1,x2,y2)<(r1+r2):
        return True
    else:
        return False    
