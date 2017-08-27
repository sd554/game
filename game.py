#!/usr/bin/env python
# -*- coding: utf-8 -*-

from graphics import *
import math, network, inputmod, time

makeGraphicsWindow(850,600)

###################################################################
#########################  Classes  ###############################
###################################################################

class Connection:
    def __init__(self,c):
        self.c=c

class Player:
    def __init__(self,con,name="Unnamed Player",role=None,health=10,apparent=10,alive=True):
        self.con=con
        self.name=name
        self.role=role
        self.health=health
        self.apparent=apparent
        self.alive=alive
        self.incoming=0
        self.apparentIncoming=0
        self.pastI=0
        self.target=""
        self.tempPower=1
        self.win=False
        ###Class Specific###
        self.bond=None
        self.extraTurns=0
        self.nextHit=0
        self.nextTarget=None

class Role:
    def __init__(self,name,health=10,power=lambda :1,reveal=False,chat=True,alive=True,aPass=True,tPass=False,analysis=lambda :0):
        self.name=name
        self.health=health
        self.power=power
        self.reveal=reveal
        self.chat=chat
        self.alive=alive
        self.aPass=aPass
        self.tPass=tPass
        self.analysis=analysis
    def getPower(self):
        return self.power()
    def analyze(self):
        self.analysis()

###################################################################
########################  Functions  ##############################
###################################################################

def new_client_function(connection):
    w=getWorld()
    w.numplayers+=1
    w.activeplayers+=1
    connection.on_receive(new_message)
    w.connections.append(Connection(connection))
    w.players.append(Player(connection))

def new_message(connection, message):
    w=getWorld()
    if message[:1]=="^":
        taken = False
        if message[1:]=="all" or message[1:]=="Unnamed Player" or message[1:]=="":
            taken=True
        else:
            for p in w.players:
                if p.name==message[1:]:
                    taken=True
                    break
        if not taken:
            for p in w.players:
                if p.con==connection:
                    p.name=message[1:]
                    w.namedplayers+=1
            for con in w.connections:
                con.c.send("^Approved")
        else:
            for con in w.connections:
                con.c.send("^Denied")
    elif message[:1]=="@":
        for con in w.connections:
            con.c.send(message)
    elif message[:1]=="$":
        name = message[1:].partition("$")[0]
        role = message[1:].partition("$")[2]
        for p in w.players:
            if p.name==name and p.role==None:
                for r in w.allroles:
                    if role==r.name:
                        p.role=r
                        p.apparent=r.health
                        p.health=r.health
                        break
                w.roleschosen+=1
                break
    elif message[:1]=="#":
        print message
        exec message[1:]
    elif message[:1]=="*":
        w.connectedPlayers.append(message[1:])
    else:
        print message

def check():
    for con in getWorld().connections:
        con.c.send("*")

def confirm():           
    w=getWorld()
    if len(w.connectedPlayers)==w.numplayers:
        return True
    else:
        for p in w.players:
            if not p.name in w.connectedPlayers:
                kick(p)
    w.connectedPlayers=[]
    return False

def keyPress(w,k):
    pass

def isShift():
    if isKeyPressed("left shift") or isKeyPressed("right shift"):
        return True
    else:
        return False

def mousePress(w,x,y,b):
    if not w.gameStarted and b==1 and w.numplayers>0 and w.namedplayers==w.numplayers and inbox(10,150,x,y,90,40):
        check()
        time.sleep(1)
        if confirm():
            w.gameStarted = True
            for con in w.connections:
                con.c.send("*start")
    elif not w.gameStarted and b==1 and inbox(10,100,x,y,90,40):
        check()
        time.sleep(1)
        confirm()
    elif b==1 and not w.gameStarted:
        ypos=10
        for p in w.players:
            if inbox(460,ypos+5,x,y,30,30):
                kick(p)
            ypos+=45
    elif b==1 and w.phase=="End":
        if inbox(10,150,x,y,160,40):
            for con in w.connections:
                con.c.send("*newgame")
            w.phase="Roles"
            w.activeplayers=w.numplayers
            w.roleschosen=0
            w.round=0
            w.gameStarted=False
            w.stalemates=0
            for p in w.players:
                p.role=None
                p.health=10
                p.apparent=10

def unPass():
    getWorld().passes-=1

def kick(player):
    w=getWorld()
    w.numplayers-=1
    w.activeplayers-=1
    if not player.name=="Unnamed Player":
        w.namedplayers-=1
    player.con.send("#getWorld().kicked=True")
    player.con.close()
    w.players.remove(player)

def passPhase():
    w=getWorld()
    w.passes+=1
    if w.passes==w.activeplayers:
        if w.phase=="Discussion":
            w.phase="Target"
            for p in w.players:
                p.tempPower=0
            for con in w.connections:
                con.c.send("*target")
            w.passes=0
        elif w.phase=="Target":
            w.phase="Analysis"
            string=""
            for p in w.players:
                string=string+"<"+p.name+"<"+str(p.tempPower)+"<"+p.target
            for con in w.connections:
                con.c.send(string)
                con.c.send("*analysis")
            w.passes=0
        elif w.phase=="Analysis":
            w.phase="Damage"
            w.round+=1
            string=""
            #Damage
            for p in w.players:
                if p.incoming>2 and p.role.name=="Shielder":
                    val=p.incoming-2
                    p.incoming-=val
                    p.apparentIncoming-=val
                elif p.role.name=="Accursed":
                    p.incoming+=1
                    p.apparentIncoming+=1
                elif p.role.name=="Leech":
                    for pl in w.players:
                        if pl.name==p.bond.name:
                            print p.incoming
                            print pl.incoming
                            p.incoming+=pl.incoming
                            p.apparentIncoming+=pl.incoming
                            print p.incoming
                            break
                if p.role.name=="Priest":
                    p.health-=p.incoming
                    p.pastI=p.incoming
                else:
                    p.health-=p.incoming
                    p.apparent-=p.apparentIncoming
                    p.pastI=p.apparentIncoming
                if p.health<=0 and p.alive:
                    if p.extraTurns>0:
                        p.extraTurns-=1
                    else:
                        p.alive=False
                        w.activeplayers-=1
            for p in w.players:
                for pl in w.players:
                    if p.alive and p.target==pl.name and not pl.alive and p.role.name=="Assassin":
                        p.health+=3
                        p.apparent+=3
                        p.incoming-=3
                        p.apparentIncoming-=3
                        p.con.send("#assassinKill(\""+pl.name+"\")")
            for p in w.players:
                string=string+">"+str(p.incoming)+">"+str(p.apparentIncoming)
                p.incoming=0
                p.apparentIncoming=0
            if w.activeplayers>=2:
                for con in w.connections:
                    con.c.send(string)
                    con.c.send("*damage")
            else:
                for con in w.connections:
                    con.c.send(string)
                    con.c.send("*end")
                w.phase="End"
            w.passes=0
        elif w.phase=="Damage" or w.phase=="Starting":
            if w.stalemates>0:
                for con in w.connections:
                    con.c.send("#newMessage('The stalemate counter has been reset')")
                w.stalemates=0
            w.phase="Discussion"
            for con in w.connections:
                con.c.send("*discussion")
            w.passes=0

def target(target,damage,player):
    for p in getWorld().players:
        if (p.name==target and not p.role.name=="Leech") or (p.name==target and p.role.name=="Leech" and p.bond.name==player):
            p.incoming+=damage
            p.apparentIncoming+=damage
        if p.name==player:
            p.target=target
            p.tempPower=damage
        if p.role.name=="Freespoken" and p.name==player:
            for con in getWorld().connections:
                con.c.send("#newMessage(\""+player+" attacked "+target+"\")")

def stalemate(name):
    getWorld().stalemates+=1
    for con in getWorld().connections:
        con.c.send("#newMessage(\""+name+" requested a stalemate.\")")
        if getWorld().stalemates==getWorld().activeplayers:
            con.c.send("*stalemate")
            getWorld().phase="End"

def unStalemate(name):
    getWorld().stalemates-=1
    for con in getWorld().connections:
        con.c.send("#newMessage(\""+name+" unrequested a stalemate.\")")

onMousePress(mousePress)
onAnyKeyPress(keyPress)

###################################################################
##################  Role Specific Functions  ######################
###################################################################

def inaccuratePower():
    pass

def shotPower():
    pass

def finishPower():
    pass

def grow():
    pass

def growPower():
    pass

def changeApparent(name,value):
    for p in getWorld().players:
        if p.name==name:
            p.apparentIncoming=value

def sendBond(target,player):
    person1=None
    person2=None
    for p in getWorld().players:
        if p.name==player:
            person1=p
        if p.name==target:
            person2=p
    person1.bond=person2

def always(num):
    return num

###################################################################
##########################  Start  ################################
###################################################################

def start(w):
    w.numplayers = 0
    w.namedplayers = 0
    w.activeplayers = 0
    w.roleschosen = 0
    w.passes = 0
    w.connectedPlayers = []

    w.connections = []
    w.gameStarted = False
    w.stalemates = 0
    
    w.players = []
    w.round = 0
    w.phase = "Roles"
    w.allroles = [Role("Faithful",reveal=True),
                  Role("Hidden"),
                  Role("Detective",aPass=False),
                  Role("Shielder"),
                  Role("Accursed",power=lambda :3),
                  Role("Priest",reveal=True),
                  Role("Inaccuracy",power=inaccuratePower),
                  Role("Journalist"),
                  Role("Leech"),
                  Role("Healer"),
                  Role("Survivor"),
                  Role("Lag",power=lambda :2),
                  Role("Catapult",power=lambda :5),
                  Role("Finisher",power=finishPower),
                  Role("Freespoken",reveal=True,power=lambda :2),
                  Role("Glass Cannon",reveal=True,power=lambda :3,health=5),
                  Role("Shifter",aPass=False),
                  Role("Deadshot",reveal=True,power=shotPower),
                  Role("Tower",reveal=True,health=18),
                  Role("Assassin"),
                  Role("Growth",tPass=True,analysis=grow,power=growPower)]
    network.listen(new_client_function)

###################################################################
##########################  Update  ###############################
###################################################################

def update(w):
    if w.gameStarted and w.phase=="Roles" and w.roleschosen==w.numplayers:
        w.phase="Starting"
        string="!"
        for p in w.players:
            string=string+p.name+"!"+p.role.name+"!"
            if p.role.name=="Survivor":
                p.extraTurns=2
        for con in w.connections:
            con.c.send(string)

###################################################################
###########################  Draw  ################################
###################################################################

def draw(w):
    drawString("Number of Players: "+str(w.numplayers),10,10,15,font="Tahoma")
    drawString("Number of Connected Players: "+str(w.activeplayers),10,35,15,font="Tahoma")
    if not w.gameStarted:
        fillRectangle(10,100,90,40,color="red")
        drawRectangle(10,100,90,40,thickness=2)
        drawString("Check",15,100,color="white",font="Tahoma")
    if w.namedplayers==w.numplayers and w.numplayers>0 and not w.gameStarted:
        fillRectangle(10,150,90,40,color="green")
        drawRectangle(10,150,90,40,thickness=2)
        drawString("Start",15,150,color="white",font="Tahoma")
    elif w.gameStarted:
        drawString("Phase: "+w.phase,10,85,15,font="Tahoma")
        drawString("Round: "+str(w.round),10,60,15,font="Tahoma")
        if w.phase=="End":
            fillRectangle(10,150,160,40,color="red")
            drawRectangle(10,150,160,40,thickness=2)
            drawString("New Game",15,150,color="white",font="Tahoma")
    ypos=10
    for p in w.players:
        display=None
        if not p.role==None:
            display=p.role.name
        if w.gameStarted:
            drawString(p.health,460,ypos+5)
        else:
            fillRectangle(460,ypos+5,30,30,color="red")
            drawRectangle(460,ypos+5,30,30,thickness=2)
            drawString("K",462,ypos,color="white",font="Tahoma")
        if p.win:
            drawString(p.name,500,ypos,color=(0,255,0),font="Tahoma")
            drawString(display,500,ypos+32,15,color=(0,255,0),font="Tahoma")
        else:
            drawString(p.name,500,ypos,font="Tahoma")
            drawString(display,500,ypos+32,15,font="Tahoma")
        ypos+=45
        
runGraphics(start,update,draw)
