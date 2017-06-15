#!/usr/bin/env python
# -*- coding: utf-8 -*-

from graphics import *
from functions import *
import os, network, math, random, inputmod

makeGraphicsWindow(1200,600)

###################################################################
##########################  To Do  ################################
###################################################################

########### Urgent

########### Priority 1

# # # Multiple line msgs

# # # Program Stalemate

# # # New game btn

########### Priority 2

# # # "You have been kicked"

# # # GitHub

# # # Quitting halfway through

# # # implement drawUniform()

# # # Instructions, Class List

# # # Test utf8

# # # Passing as Leech/Deadshot

# # # Assassin Class, Leech Class, Life Swap Class, Teammate Class

########### Future

# # # Icons for MAIN, USER, ETC

# # # Class Reward

# # # Two Team, Pair Modes

# # # Politician Class, Unforgiving Class, Factory Class, Identity Thief Class, Haunter Class

###################################################################
#########################  Classes  ###############################
###################################################################

class Role:
    def __init__(self,name,health=10,power=lambda :1,reveal=False,chat=True,alive=True,aPass=True,analysis=lambda :0):
        self.name=name
        self.health=health
        self.power=power
        self.reveal=reveal
        self.chat=chat
        self.alive=alive
        self.aPass=aPass
        self.analysis=analysis
    def getPower(self):
        return self.power()
    def analyze(self):
        self.analysis()

class Player:
    def __init__(self,name,role=None,health=10,apparent=10,alive=True):
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
        #Class Specific
        self.bond=None
        self.extraTurns=0
        self.nextHit=0
        self.nextTarget=None

###################################################################
########################  Functions  ##############################
###################################################################

def new_message(connection, message):
    w=getWorld()
    if message[:1]=="*":
        if message=="*start":
            newMessage("The game has been started.")
            w.started=True
            w.waiting=False
            r = open("../roles.txt","r")
            for line in r:
                w.roles.append(str.strip(line))
        elif message=="*target":
            if not w.phase=="Death":
                newMessage("It is now Target phase.")
                w.phase="Target"
                w.stalemates=0
                w.passed=False
                w.player.tempPower=0
                if w.role.name=="Catapult" and not w.round%3==0:
                    w.passed=True
                    w.connection.send("#passPhase()")
        elif message=="*analysis":
            if not w.phase=="Death":
                newMessage("It is now Analysis phase.")
                w.phase="Analysis"
                w.passed=False
                w.role.analyze()
        elif message=="*discussion":
            if not w.phase=="Death":
                newMessage("It is now Discussion phase.")
                w.phase="Discussion"
                w.passed=False
                w.round+=1
        elif message=="*damage":
            if not w.phase=="Death":
                newMessage("It is now Damage phase.")
                newMessage("Your actual health is "+str(w.player.health))
                w.phase="Damage"
                w.passed=False
        elif message=="*end":
            w.phase="End"
            winner = False
            for p in w.players:
                if p.alive:
                    if p.name==w.name:
                        newMessage("You have won the game!")
                    else:
                        newMessage(p.name+" ("+p.role.name+") has won the game!")
                    p.win=True
                    winner=True
                    break
            if not winner:
                newMessage("The game ends in a draw!")
        elif message=="*":
            w.connection.send("*"+w.name)
    elif message[:1]=="@":
        text = message[1:]
        targetName = text[:text.index("<")]
        text = text[text.index("<"):][1:]
        senderName = text[:text.index(">")]
        text = text[text.index(">"):][1:]
        if w.player.alive and w.role.chat and (targetName==w.name or targetName=="all" or senderName==w.name):
            newMessage("("+senderName+" -> "+targetName+") "+text)
            if w.passed:
                w.connection.send("#unPass()")
                w.passed=False
    elif message[:1]==">":
        parts = message[1:].split(">")
        for x in range(len(parts)):
            if x%2==1:
                if w.players[x/2].role.name=="Priest":
                    w.players[x/2].health-=int(parts[x-1])
                    w.players[x/2].pastI=0
                else:
                    w.players[x/2].health-=int(parts[x-1])
                    w.players[x/2].apparent-=int(parts[x])
                    w.players[x/2].pastI=int(parts[x])
                w.players[x/2].incoming=0
                w.players[x/2].apparentIncoming=0
                if w.players[x/2].health<=0 and w.players[x/2].alive:
                    if w.players[x/2].extraTurns>0:
                        w.players[x/2].extraTurns-=1
                    else:
                        w.players[x/2].alive=False
                        if w.players[x/2].name==w.name:
                            w.phase="Death"
                            newMessage("You have lost the game!")
                        else:
                            newMessage(w.players[x/2].name+" ("+w.players[x/2].role.name+") has lost the game.")
                            if w.players[x/2]==w.player.bond:
                                w.player.bond=None
    elif message[:1]=="<":
        parts = message[1:].split("<")
        for x in range(len(parts)):
            if x%3==0 and x+1<len(parts):
                for p in w.players:
                    if parts[x+2]==p.name:
                        p.incoming+=int(parts[x+1])
                        p.apparentIncoming+=int(parts[x+1])
                        w.players[x/3].target=p.name
                        break
    elif message[:1]=="!":
        parts = message[1:].split("!")
        for x in range(len(parts)):
            if x%2==0 and len(parts[x])>0:
                for role in w.allroles:
                    if parts[x+1]==role.name:
                        w.players.append(Player(parts[x],role))
        for p in w.players:
            p.health=p.role.health
            p.apparent=p.role.health
            if p.name==w.name:
                w.player=p
        w.phase="Starting"
        newMessage("It is now Starting phase.")
        if w.role.name=="Journalist":
            for p in w.players:
                newMessage(p.name+": "+p.role.name)
        for p in w.players:
            if p.role.name=="Survivor":
                p.extraTurns=2
    elif message[:1]=="^":
        if message[1:]=="Denied" and w.approval==False and w.recent==True:
            w.recent=False
            w.logged=False
            w.taken=False
        elif w.approval==False and w.recent==True:
            w.approval=True
            w.recent=False
            inputmod.box["string"]=""
    elif message[:1]=="#":
        exec message[1:]

def newMessage(new):
    getWorld().messages = [new] + getWorld().messages

def connect():
    w=getWorld()
    w.connection = network.connect('192.168.1.10') #atHomeIP
#    w.connection = network.connect('192.168.1.1') #routerIP
#    w.connection = network.connect('50.53.51.68') #publicRouterIP
#    w.connection = network.connect('10.70.150.13') #catlinIP
#    w.connection = network.connect('192.168.1.12') #desktopIP
#    w.connection = network.connect('192.168.1.17')
#    w.connection = network.connect('192.168.1.2')
    if not w.connection==None:
        w.connected=True
        w.connection.on_receive(new_message)

###################################################################
######################  Mouse/Keypress  ###########################
###################################################################

def mousePress(w,x,y,b):
    if w.started and inbox(1180,580,x,y,20,20):
        if w.setshow:
            w.setshow=False
        else:
            w.setshow=True
            
    if w.view=="Game":
        ################# Up/Down Arrows  ###################
        if b=="left" and w.started and len(w.messages)>33:
            if inbox(880,585,x,y,40,10):
                w.offset+=250
            elif inbox(1080,585,x,y,40,10):
                w.offset-=250
        ################# Selecting Roles ###################
        if b=="left" and w.role==None and w.started==True:
            ypos=100
            xpos=500
            for r in w.roles:
                if inbox(xpos,ypos,x,y,250,20):
                    for role in w.allroles:
                        if role.name==r:
                            w.role=role
                            break
                    w.connection.send("$"+w.name+"$"+r)
                if w.roles.index(r)%15==14:
                    xpos+=200
                    ypos=70
                ypos+=30
        ##################### Passing  ######################
        if (w.phase=="Discussion" or w.phase=="Starting" or w.phase=="Damage" or (w.phase=="Analysis" and w.role.aPass)) and not w.passed:
            if inbox(650,500,x,y,90,40):
                if w.chosenPlayer==None:
                    w.passed=True
                    w.connection.send("#passPhase()")
                else:
                    w.chosenPlayer=None
                    inputmod.box["string"]=""
        ###################### Chat #1 #######################
        if b=="left" and w.phase=="Discussion" and not w.passed and w.role.chat and w.chosenPlayer==None:
            add=0
            for p in w.players:
                if p.alive and p.role.chat and not p.name==w.name:
                    if inbox(610,220+add,x,y,30,30):
                        w.chosenPlayer=p.name
                    add+=35
            if inbox(610,220+add,x,y,30,30):
                w.chosenPlayer="all"
        ##################### Detective ######################
        if b=="left" and w.phase=="Analysis" and w.role.name=="Detective" and not w.passed:
            add=0
            for p in w.players:
                if p.alive:
                    if inbox(610,220+add,x,y,30,30):
                        if p.target=="" or p.target==None:
                            newMessage(p.name+" did not attack.")
                        else:
                            newMessage(p.name+" attacked "+p.target)
                        w.connection.send("#passPhase()")
                        w.passed=True
                    add+=35
        #################### Target Phase ####################
        if b=="left" and w.phase=="Target" and not w.passed:
            add=0
            for p in w.players:
                if p.alive and (not w.role.name=="Deadshot" or w.player.bond==p):
                    if inbox(610,250+add,x,y,30,30):
                        w.player.target=p.name
                        damage=w.role.getPower()
                        if w.role.name=="Healer" and p.name==w.name:
                            damage=-damage
                        elif w.role.name=="Lag":
                            hit=w.player.nextHit
                            trg=w.player.nextTarget
                            w.player.nextHit=damage
                            w.player.nextTarget=p.name
                            w.player.target=trg
                            damage=hit
                        w.player.tempPower=damage
                        if not w.player.target==None:
                            newMessage("You attacked "+w.player.target+" for "+str(damage)+" damage.")
                            w.connection.send("#target(\""+w.player.target+"\","+str(damage)+",\""+w.name+"\")")
                        w.connection.send("#passPhase()")
                        w.passed=True
                    add+=35
        ################### Deadshot/Leech ####################
        if (w.phase=="Starting" or w.phase=="Damage") and (w.role.name=="Deadshot" or w.role.name=="Leech") and w.player.bond==None:
            add=0
            for p in w.players:
                if p.alive and (w.role.name=="Deadshot" or not w.name==p.name):
                    if inbox(610,250+add,x,y,30,30):
                        w.player.bond=p
                        if w.role.name=="Deadshot":
                            newMessage("You targeted "+p.name)
                        else:
                            newMessage("You selected "+p.name+" as a host.")
                        w.connection.send("#sendBond(\""+p.name+"\",\""+w.name+"\")")
                        w.connection.send("#passPhase()")
                        w.passed=True
                    add+=35
        ###################### Shifter ########################
        if b=="left" and w.phase=="Analysis" and w.role.name=="Shifter" and not w.passed:
            add=0
            for z in range(-1,2):
                if inbox(610,250+add,x,y,90,30):
                    w.connection.send("#changeApparent(\""+w.name+"\","+str(w.player.incoming+z)+")")
                    w.connection.send("#passPhase()")
                    w.passed=True
                add+=35

def keyPress(w,k):
    if not w.chosenPlayer==None:
        if k==42:
            inputmod.box["string"]=inputmod.box["string"][:-1]
        elif k==40:
            w.connection.send("@"+w.chosenPlayer+"<"+w.name+">"+inputmod.box["string"])
            w.chosenPlayer=None
            inputmod.box["string"]=""
        elif len(inputmod.box["string"])<25:
            inputmod.write(w,k)
    elif w.waiting and not w.approval and w.view=="Game":
        if k==42 and len(inputmod.box["string"])>0:
            inputmod.box["string"]=inputmod.box["string"][:-1]
        elif k==40:
            w.logged=True
            w.recent=True
            w.name=inputmod.box["string"]
            w.connection.send("^"+w.name)
        elif isShift():
            if len(inputmod.box["string"])<18 and ((k>=4 and k<=29) or k==44):
                inputmod.write(w,k)
        elif len(inputmod.box["string"])<18 and ((k>=4 and k<=29) or (k>=30 and k<=39) or k==54 or k==55 or k==44):
            inputmod.write(w,k)

def isShift():
    if isKeyPressed("left shift") or isKeyPressed("right shift"):
        return True
    else:
        return False

onMousePress(mousePress)
onAnyKeyPress(keyPress)

###################################################################
##################  Role Specific Functions  ######################
###################################################################

def detect():
    pass
##    selected=False
##    player=""
##    char=None
##    while not selected:
##        player=raw_input("Select a player: ")
##        for p in getWorld().players:
##            if p.name==player:
##                selected=True
##                char=p
##                break
##    print player+" attacked "+char.target+"."

def inaccuratePower():
    return random.randint(-2,4)

def shotPower():
    return random.randint(1,3)

def finishPower():
    if getWorld().round>7:
        return 3
    else:
        return 1

###################################################################
##########################  Start  ################################
###################################################################

def start(w):
    w.connection = None
    w.connected = False
    w.kicked = False
    w.logged = False
    w.waiting = True
    w.approval = False
    w.recent = False
    w.taken = False
    w.chosenPlayer = None
    w.stalemates = 0
    
    w.settings = {"Stalemate Request":"Game",
                  "Classes":"Classes",
                  "Instructions":"Instructions"}
    w.setshow = False
    
    w.name = "Player"
    w.player = None
    w.role = None
    w.roles = []
    w.allroles = [Role("Faithful",reveal=True),
                  Role("Hidden"),
                  Role("Detective",aPass=False),
                  Role("Shielder"),
                  Role("Accursed",power=lambda :3),
                  Role("Priest",reveal=True),
                  Role("Shifter",aPass=False),
                  Role("Inaccuracy",power=inaccuratePower),
                  Role("Glass Cannon",reveal=True,power=lambda :3,health=5),
                  Role("Journalist"),
                  Role("Deadshot",reveal=True,power=shotPower),
                  Role("Leech"),
                  Role("Healer"),
                  Role("Survivor"),
                  Role("Lag",power=lambda :2),
                  Role("Catapult",power=lambda :5),
                  Role("Finisher",power=finishPower),
                  Role("Freespoken",reveal=True,power=lambda :2)]
    w.players = []
    w.started = False
    w.passed = False
    w.round = 0
    w.phase = "Roles"
    w.view = "Game"
    w.messages = []
    w.offset=0

###################################################################
##########################  Update  ###############################
###################################################################

def update(w):
    if not w.connected:
        connect()

###################################################################
###########################  Draw  ################################
###################################################################

def drawUniform(string,x,y,s,c):
    drawString(string,x,y,size=s,color=c,font="Times")

def draw(w):
    if w.kicked:
        drawString("You have been kicked. Reload this page to try again.",10,10)
    #################### Connecting #####################
    if not w.connected:
        drawString("Connecting...",320,200,font="Times")
    ##################### Waiting #######################
    elif w.waiting:
        drawString("Waiting...",320,200,font="Times")
        if not w.approval:
            drawString("Name: ",320,240,size=20,font="Tahoma")
            inputmod.drawinputbox(320,265,35)
            drawRectangle(320,265,450,38)
            drawString("Your name must be less than 19 characters and can only",320,305,size=15,font="Times")
            drawString("contain letters, numbers, spaces, periods, and commas.",320,325,size=15,font="Times")
            if w.taken:
                drawString("That name is already taken.",320,345,size=15,font="Times")
    ################## Selecting Roles ##################
    elif w.view=="Game":
        if w.started and w.role==None:
            drawString("Pick a Role:",500,50,font="Times")
            ypos=100
            xpos=500
            for r in w.roles:
                drawString(r,xpos,ypos,20,font="Times")
                if w.roles.index(r)%15==14:
                    xpos+=200
                    ypos=70
                ypos+=30
        elif w.started:
            drawLine(600,0,600,600,thickness=2)
            drawLine(800,0,800,600,thickness=2)
            drawString(w.name,610,20,18,font="Times")
            drawString(w.role.name,610,45,15,font="Times")
            drawString("Phase: "+w.phase,610,140,20,font="Times")
            drawString("Round: "+str(w.round),610,160,20,font="Times")
            #################### Textbar ######################
            if True:
                add=w.offset
                for message in w.messages:
                    drawString(" > "+message,800,5+add,size=15,font="Times")
                    add+=16
            if len(w.messages)>33:
                fillRectangle(800,580,1200,20,color="white")
                drawRectangle(800,580,1200,20,thickness=2)
                fillPolygon([(880,595),(920,595),(900,585)],color="red")
                drawPolygon([(880,595),(920,595),(900,585)],thickness=2)
                fillPolygon([(1080,585),(1120,585),(1100,595)],color="red")
                drawPolygon([(1080,585),(1120,585),(1100,595)],thickness=2)
            ################## Pass Button #####################
            if (w.phase=="Discussion" or w.phase=="Starting" or w.phase=="Damage" or (w.phase=="Analysis" and w.role.aPass)) and not w.passed:
                fillRectangle(650,500,90,40,color="red")
                drawRectangle(650,500,90,40,thickness=2)
                if w.chosenPlayer==None:
                    drawString("Pass",655,502,size=15,color="white",font="Times")
                else:
                    drawString("Cancel",655,502,size=15,color="white",font="Times")
            ################## Target Phase ####################
            elif w.phase=="Target" and not w.passed:
                add=0
                drawString("Pick a Target",610,200,15,font="Times")
                for p in w.players:
                    if p.alive and (not w.role.name=="Deadshot" or w.player.bond==p):
                        fillRectangle(610,250+add,30,30,color="red")
                        drawRectangle(610,250+add,30,30,thickness=2)
                        drawString(p.name,650,255+add,12,font="Times")
                        add+=35
            ################## Deadshot/Leech ##################
            if (w.phase=="Starting" or w.phase=="Damage") and (w.role.name=="Deadshot" or w.role.name=="Leech") and w.player.bond==None:
                add=0
                if w.role.name=="Deadshot":
                    drawString("Select a Target",610,200,15,font="Times")
                else:
                    drawString("Select a Host",610,200,15,font="Times")
                for p in w.players:
                    if p.alive and (w.role.name=="Deadshot" or not w.name==p.name):
                        fillRectangle(610,250+add,30,30,color="red")
                        drawRectangle(610,250+add,30,30,thickness=2)
                        drawString(p.name,650,255+add,12,font="Times")
                        add+=35
            ##################### Shifter ######################
            if not w.passed and w.phase=="Analysis" and w.role.name=="Shifter":
                for p in w.players:
                    if p.name==w.name:
                        drawString("You are taking "+str(p.incoming)+" damage.",610,200,size=12,font="Times")
                        add=0
                        for x in range(-1,2):
                            fillRectangle(610,250+add,90,30,color="red")
                            drawRectangle(610,250+add,90,30,thickness=2)
                            drawString(str(p.incoming+x)+" damage",615,255+add,10,font="Times")
                            add+=35
            #################### Detective #####################
            elif not w.passed and w.phase=="Analysis" and w.role.name=="Detective":
                add=0
                drawString("Select a Player:",610,200,15,font="Times")
                for p in w.players:
                    if p.alive:
                        fillRectangle(610,220+add,30,30,color="red")
                        drawRectangle(610,220+add,30,30,thickness=2)
                        drawString(p.name,650,225+add,12,font="Times")
                        add+=35
            ###################### Chat ########################
            elif not w.passed and w.phase=="Discussion" and w.role.chat:
                if w.chosenPlayer==None:
                    add=0
                    drawString("Players:",610,200,15,font="Times")
                    for p in w.players:
                        if p.alive and p.role.chat and not p.name==w.name:
                            fillRectangle(610,220+add,30,30,color="red")
                            drawRectangle(610,220+add,30,30,thickness=2)
                            drawString(p.name,650,225+add,12,font="Times")
                            add+=35
                    fillRectangle(610,220+add,30,30,color="red")
                    drawRectangle(610,220+add,30,30,thickness=2)
                    drawString("all",650,225+add,12,font="Times")
                else:
                    drawString(w.chosenPlayer,610,182,size=15,font="Times")
                    drawString("Text (max 24 chars):",610,200,size=15,font="Times")
                    inputmod.drawinputbox(610,220,15)
                    drawRectangle(610,220,180,17)
            ################# Drawing Players ##################
            if len(w.players)>0:
                num=0
                ypos=0
                de=math.ceil(len(w.players)/3.0)
                for p in w.players:
                    display=p.role.name
                    c="black"
                    if p.role.reveal==False and not w.role.name=="Journalist":
                        display="?"
                    if p.win:
                        c="green"
                    if w.players.index(p)%3==0:
                        ypos=0
                    elif w.players.index(p)%3==1:
                        ypos=225
                    else:
                        ypos=450
                    if p.alive:
                        spot=600*num/de
                        if p.role.name=="Priest":
                            drawString("?",5+spot,ypos,40,color=c,font="Times")
                        else:
                            drawString(p.apparent,5+spot,ypos,40,color=c,font="Times")
                        if not p.pastI==0:
                            drawString("("+str(-1*p.pastI)+")",spot+50,ypos,20,color=c,font="Times")
                        drawString(p.name,5+spot,ypos+50,15,color=c,font="Times")
                        drawString(display,5+spot,ypos+75,15,color=c,font="Times")
                    if w.players.index(p)%3==2:
                        num+=1
    elif w.view=="Instructions":
        pass
    elif w.view=="Classes":
        pass
    if w.started:
        fillRectangle(1180,580,20,20,color="gray")
        drawRectangle(1180,580,20,20,thickness=2)
        if w.setshow:
            add=0
            for opt in w.settings.keys():
                fillRectangle(998,563+add,202,18,color="white")
                drawString(opt,1000,565+add,size=15,font="Times")
                drawRectangle(998,563+add,202,18)
                add-=18

runGraphics(start,update,draw)
