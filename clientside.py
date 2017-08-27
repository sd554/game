#!/usr/bin/env python
# -*- coding: utf-8 -*-

from graphics import *
import os, network, math, random, inputmod

makeGraphicsWindow(1200,600)

###################################################################
##########################  To Do  ################################
###################################################################

# (1-5) Quitting Midgame, Better Scrolling, Leech Class, Username IDs, Silent Class

########### Urgent

# # # Freespoken fix

# # # Assassin fix

########### Priority 1

# # # Quitting midgame

# # # IDs as Usernames

# # # Better scrolling

# # # Numplayers / num connected players

########### Priority 2

# # # Growth storing damage

# # # Mini catapult

# # # Serverside record data

# # # Test utf8

# # # Reveal Survivor when at 0

# # # Passing as Leech/Deadshot

# # # New Classes

########### Future

# # # Icons for MAIN, USER, ETC

# # # Class Reward

# # # Pair Mode, Priest Mode

# # # New Classes

###################################################################
#########################  Classes  ###############################
###################################################################

class Role:
    def __init__(self,name,health=10,power=lambda :1,reveal=False,chat=True,alive=True,aPass=True,analysis=lambda :0,tPass=False,desc=""):
        self.name=name
        self.health=health
        self.power=power
        self.reveal=reveal
        self.chat=chat
        self.alive=alive
        self.aPass=aPass
        self.tPass=tPass
        self.analysis=analysis
        self.desc=desc
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
        self.currentPower=1

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
            r = open("roles.txt","r")
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
                w.requested=False
        elif message=="*damage":
            if not w.phase=="Death":
                newMessage("It is now Damage phase.")
                w.phase="Damage"
                w.passed=False
        elif message=="*newgame":
            w.phase = "Roles"
            w.waiting = True
            w.chosenPlayer = None
            w.requested = False
            w.setshow = False
            w.player = None
            w.role = None
            w.roles = []
            w.players = []
            w.started = False
            w.passed = False
            w.round = 0
            w.view = "Game"
            w.messages = []
            w.offset = 0
            w.lines = 0
            w.offset_2 = 0
        elif message=="*stalemate":
            w.phase="End"
            newMessage("The game ends in stalemate.")
        elif message=="*end":
            w.phase="End"
            winner = False
            for p in w.players:
                if p.alive:
                    if p.name==w.name:
                        newMessage("You have won the game!")
                    else:
                        newMessage(p.name+" ("+p.role.name+") has won the game!")
                        if p.role.name=="Priest":
                            newMessage(p.name+" had "+p.health+" life left.")
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
                            if w.requested:
                                w.connection.send("#getWorld().stalemates-=1")
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
#    w.connection = network.connect('192.168.1.10') #atHomeIP
#    w.connection = network.connect('192.168.1.1') #routerIP
#    w.connection = network.connect('50.53.51.68') #publicRouterIP
#    w.connection = network.connect('10.70.150.13') #catlinIP
    w.connection = network.connect('192.168.1.12') #desktopIP
#    w.connection = network.connect('192.168.1.17')
#    w.connection = network.connect('192.168.1.2')
    if not w.connection==None:
        w.connected=True
        w.connection.on_receive(new_message)

###################################################################
########################  Mousepress  #############################
###################################################################

def mousePress(w,x,y,b):
    ################### Settings  #######################
    if b==1 and w.started and inbox(1180,580,x,y,20,20):
        if w.setshow:
            w.setshow=False
        else:
            w.setshow=True
    if b==1 and w.started and w.setshow:
        add=0
        for s in w.settings.keys():            
            if inbox(998,563+add,x,y,202,18):
                w.view=w.settings[s]
                w.setshow=False
                if s=="Stalemate Request" and w.player.alive and not w.phase=="Roles":
                    if not w.requested:
                        w.requested=True
                        w.connection.send("#stalemate(\""+w.name+"\")")
                    else:
                        w.requested=False
                        w.connection.send("#unStalemate(\""+w.name+"\")")
            add-=18
    ################# Up/Down Arrows  ###################
    if w.view=="Classes":
        if b==1 and w.started:
            if inbox(400,585,x,y,40,10):
                w.offset_2+=250
            elif inbox(760,585,x,y,40,10):
                w.offset_2-=250
    elif w.view=="Game":
        ################# Up/Down Arrows  ###################
        if b==1 and w.started and w.lines>33:
            if inbox(880,585,x,y,40,10):
                w.offset+=250
            elif inbox(1080,585,x,y,40,10):
                w.offset-=250
        ################# Selecting Roles ###################
        if b==1 and w.role==None and w.started==True:
            ypos=100
            xpos=500
            for r in w.roles:
                if inbox(xpos,ypos,x,y,180,20):
                    for role in w.allroles:
                        if role.name==r:
                            w.role=role
                            break
                    w.connection.send("$"+w.name+"$"+r)
                if w.roles.index(r)%15==14:
                    xpos+=200
                    ypos=70
                ypos+=30
        ###################### Passing  ######################
        if b==1 and (w.phase=="Discussion" or w.phase=="Starting" or w.phase=="Damage" or (w.phase=="Target" and w.role.tPass) or (w.phase=="Analysis" and w.role.aPass)) and not w.passed:
            if inbox(650,85,x,y,90,40):
                if w.chosenPlayer==None:
                    w.passed=True
                    w.connection.send("#passPhase()")
                else:
                    w.chosenPlayer=None
                    inputmod.box["string"]=""
        elif b==1 and w.phase=="Discussion" and w.passed:
            if inbox(650,85,x,y,90,40):
                w.passed=False
                w.connection.send("#unPass()")
        ###################### Chat #1 #######################
        if b==1 and w.phase=="Discussion" and not w.passed and w.role.chat and w.chosenPlayer==None:
            add=0
            for p in w.players:
                if p.alive and p.role.chat and not p.name==w.name:
                    if inbox(610,220+add,x,y,30,30):
                        w.chosenPlayer=p.name
                    add+=35
            if inbox(610,220+add,x,y,30,30):
                w.chosenPlayer="all"
        ##################### Detective ######################
        if b==1 and w.phase=="Analysis" and w.role.name=="Detective" and not w.passed:
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
        if b==1 and w.phase=="Target" and not w.passed:
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
                        elif w.role.name=="Growth":
                            w.player.currentPower=0
                        w.player.tempPower=damage
                        if not w.player.target==None:
                            newMessage("You attacked "+w.player.target+" for "+str(damage)+" damage.")
                            w.connection.send("#target(\""+w.player.target+"\","+str(damage)+",\""+w.name+"\")")
                        w.connection.send("#passPhase()")
                        w.passed=True
                    add+=35
        ################### Deadshot/Leech ####################
        if b==1 and (w.phase=="Starting" or w.phase=="Damage") and (w.role.name=="Deadshot" or w.role.name=="Leech") and w.player.bond==None:
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
        if b==1 and w.phase=="Analysis" and w.role.name=="Shifter" and not w.passed:
            add=0
            for z in range(-1,2):
                if inbox(610,250+add,x,y,90,30):
                    w.connection.send("#changeApparent(\""+w.name+"\","+str(w.player.incoming+z)+")")
                    w.connection.send("#passPhase()")
                    w.passed=True
                add+=35

###################################################################
##########################  Keypress  #############################
###################################################################

def keyPress(w,k):
    if not w.chosenPlayer==None:
        if sameKeys(k,"delete") or sameKeys(k,"backspace") and len(inputmod.box["string"])>0:
            inputmod.box["string"]=inputmod.box["string"][:-1]
        elif sameKeys("return"):
            w.connection.send("@"+w.chosenPlayer+"<"+w.name+">"+inputmod.box["string"])
            w.chosenPlayer=None
            inputmod.box["string"]=""
        else:
            inputmod.write(w,k)
    elif w.waiting and not w.approval and w.view=="Game":
        if sameKeys(k,"delete") or sameKeys(k,"backspace") and len(inputmod.box["string"])>0:
            inputmod.box["string"]=inputmod.box["string"][:-1]
        elif sameKeys(k,"enter"):
            w.logged=True
            w.recent=True
            w.name=inputmod.box["string"]
            w.connection.send("^"+w.name)
        elif isShift():
            if getKeyName(k) in "abcdefghijklmnopqrstuvwxyz" or sameKeys(k,"space"):
                inputmod.write(w,k)
        elif getKeyName(k) in "abcdefghijklmnopqrstuvwxyz1234567890,." or sameKeys(k,"space"):
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

def inaccuratePower():
    return random.randint(-2,4)

def shotPower():
    return random.randint(1,3)

def finishPower():
    if getWorld().round>7:
        return 3
    else:
        return 1

def grow():
    getWorld().player.currentPower+=1
    newMessage("You're new power is "+str(getWorld().player.currentPower)+".")

def growPower():
    return getWorld().player.currentPower

def assassinKill(player):
    newMessage("You killed "+player+", and gain 3 life.")
    getWorld().player.health+=3
    getWorld().player.apparent+=3

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
    w.requested = False
    
    w.settings = {"Stalemate Request":"Game",
                  "Classes":"Classes",
                  "Instructions":"Instructions",
                  "Game":"Game"}
    w.setshow = False
    
    w.name = "Unnamed Player"
    w.player = None
    w.role = None
    w.roles = []
    w.allroles = [Role("Faithful",reveal=True,desc="OPEN."),
                  Role("Hidden",desc="CLOSED."),
                  Role("Detective",aPass=False,desc="CLOSED; during analysis, you may determine who any one player attacked."),
                  Role("Shielder",desc="CLOSED; can take a maximum of 2 damage each turn"),
                  Role("Accursed",power=lambda :3,desc="CLOSED; 3 power; takes 1 additional damage each turn."),
                  Role("Priest",reveal=True,desc="OPEN; life total is hidden to opponents."),
                  Role("Shifter",aPass=False,desc="CLOSED; you may shift your apparent damage each turn plus or minus 1."),
                  Role("Inaccuracy",power=inaccuratePower,desc="CLOSED; -2 to 4 power"),
                  Role("Glass Cannon",reveal=True,power=lambda :3,health=5,desc="OPEN; 3 power; 5 health."),
                  Role("Journalist",desc="CLOSED; you know everyone's class."),
                  Role("Deadshot",reveal=True,power=shotPower,desc="OPEN; 1 to 4 power; has to attack the same player until the player is dead."),
                  Role("Healer",desc="CLOSED; any damage you deal to yourself gains you life instead."),
                  Role("Survivor",desc="CLOSED; survives two turns after going to 2 life"),
                  Role("Lag",power=lambda :2,desc="CLOSED; 2 power; each attack's damage is taken the turn after declared."),
                  Role("Catapult",power=lambda :5,desc="CLOSED; 5 power; attacks once every three turns."),
                  Role("Finisher",power=finishPower,desc="CLOSED; 1 power rounds 1-7, 3 power rounds 8+"),
                  Role("Freespoken",reveal=True,power=lambda :2,desc="OPEN; 2 power; who you attack is posted in chat."),
                  Role("Tower",reveal=True,health=18,desc="OPEN; 18 health."),
                  Role("Assassin",desc="CLOSED; if you do the final damage to a player, you gain 3 life."),
                  Role("Growth",tPass=True,analysis=grow,power=growPower,desc="CLOSED; you may skip a Target Phase; if you do, your power is +1 for next turn.")]
    w.players = []
    w.started = False
    w.passed = False
    w.round = 0
    w.phase = "Roles"
    w.view = "Game"
    w.messages = []
    w.offset=0
    w.offset_2=0
    w.lines=0

###################################################################
##########################  Update  ###############################
###################################################################

def update(w):
    if not w.connected:
        connect()

###################################################################
###########################  Draw  ################################
###################################################################

def draw(w):
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
            if not w.role==None:
                drawString(w.role.name,610,45,15,font="Times")
            drawString("Phase: "+w.phase,610,140,20,font="Times")
            drawString("Round: "+str(w.round),610,160,20,font="Times")
            #################### Textbar ######################
            if True:
                add=w.offset
                for message in w.messages:
                    message=" > "+message
                    words = message.split(" ")
                    string=""
                    for word in words:
                        temp=string+word+" "
                        if len(temp)>47:
                            if len(string)>0:
                                drawString(string,805,5+add,size=15,font="Anonymous Pro")
                                add+=16
                            string=word+" "
                        else:
                            string=temp
                    if len(string)>0:
                        drawString(string,805,5+add,size=15,font="Anonymous Pro")
                    add+=16
                if add/16>w.lines:
                    w.lines=add/16
            if w.lines>33:
                fillRectangle(800,580,400,20,color="white")
                drawRectangle(800,580,400,20,thickness=2)
                fillPolygon([(880,595),(920,595),(900,585)],color="red")
                drawPolygon([(880,595),(920,595),(900,585)],thickness=2)
                fillPolygon([(1080,585),(1120,585),(1100,595)],color="red")
                drawPolygon([(1080,585),(1120,585),(1100,595)],thickness=2)
            ################## Pass Button #####################
            if (w.phase=="Discussion" or w.phase=="Starting" or w.phase=="Damage" or (w.phase=="Analysis" and w.role.aPass) or (w.phase=="Target" and w.role.tPass)) and not w.passed:
                fillRectangle(650,85,90,40,color="red")
                drawRectangle(650,85,90,40,thickness=2)
                if w.chosenPlayer==None:
                    drawString("Pass",655,87,size=15,color="white",font="Times")
                else:
                    drawString("Cancel",655,87,size=15,color="white",font="Times")
            elif w.phase=="Discussion" and w.passed:
                fillRectangle(650,85,90,40,color="red")
                drawRectangle(650,85,90,40,thickness=2)
                drawString("Unpass",655,87,size=15,color="white",font="Times")
            ################## Target Phase ####################
            if w.phase=="Target" and not w.passed:
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
                    inputmod.drawWidthBox(612,220,21,15)
                    drawRectangle(610,220,180,68)
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
                        if p.role.name=="Priest" and p.name==w.name:
                            drawString(p.health,5+spot,ypos,40,color=c,font="Times")
                        elif p.role.name=="Priest":
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
        drawString("In this game, your goal is to be the last player left with a positive life total.",5,5,20,font="Times")
        drawString("There are four phases in this game:",5,30,20,font="Times")
        drawString(" 1) Discussion Phase - Talk strategy privately with other players, or message them all at once.",5,55,20,font="Times")
        drawString(" 2) Target Phase - Pick a player. This is the player who you are attacking this round.",5,80,20,font="Times")
        drawString(" 3) Analysis Phase - Certain classes may look at the damage that is dealt before it becomes visible during Damage Phase.",5,105,20,font="Times")
        drawString(" 4) Damage Phase - Everyone now can see how much damage everybody else took.",5,130,20,font="Times")
        drawString("Each player has a class that will benefit them throughout the game. Classes have the following properties:",5,155,20,font="Times")
        drawString(" - Health: This is the starting health the player will have.",5,180,20,font="Times")
        drawString(" - Power: How much damage they deal during Target Phase.",5,205,20,font="Times")
        drawString(" - Visibility: Most classes are invisible, or closed. This means other players do not know what class you are.",5,230,20,font="Times")
        drawString(" - Other: Each class may also have other capabilities.",5,255,20,font="Times")
    elif w.view=="Classes":
        add=w.offset_2
        for r in w.allroles:
            drawString(r.name+" - "+r.desc,5,5+add,size=25,font="Times")
            add+=35
        fillRectangle(0,580,1200,20,color="white")
        fillPolygon([(400,595),(440,595),(420,585)],color="red")
        drawPolygon([(400,595),(440,595),(420,585)],thickness=2)
        fillPolygon([(760,585),(800,585),(780,595)],color="red")
        drawPolygon([(760,585),(800,585),(780,595)],thickness=2)
    if w.started:
        fillRectangle(1180,580,20,20,color="gray")
        drawRectangle(1180,580,20,20,thickness=2)
        if w.setshow:
            add=0
            for opt in w.settings.keys():
                fillRectangle(998,563+add,202,18,color="white")
                if opt=="Stalemate Request" and w.requested:
                    drawString("Unrequest Stalemate",1000,564+add,size=15,font="Tahoma")
                else:
                    drawString(opt,1000,564+add,size=15,font="Tahoma")
                drawRectangle(998,563+add,202,18)
                add-=18

runGraphics(start,update,draw)
