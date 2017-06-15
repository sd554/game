from graphics import *

letters={"`","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","/","1","2","3","4","5","6","7","8","9","0","-","=",",",".",";","[","]"}
shifted={"[":"{","]":"}","1":"!","2":"@","3":"#","4":"$","5":"%","6":"^","7":"&","8":"*","9":"(","0":")","/":"?",".":">",",":"<","\\":"|","\'":"\"","`":"~","-":"_","=":"+",";":":"}
box={"string":"","data":None}

def delstring(string):
	x=list(string)
	x.pop(-1)
	newstring=""
	for letter in x:
		newstring+=letter
	return newstring

def write(w,k):
    if getKeyName(k) in letters:
        add=getKeyName(k)
    else:
        add=""
    if sameKeys(k,"quote"):
        add="\'"
    elif sameKeys(k,"\\"):
        add="\\"
    elif sameKeys(k,"space"):
        add=" "
    elif sameKeys(k, "backspace") and len(box["string"])>0:
        box["string"]=delbox["string"](box["string"])
    if isKeyPressed("left shift") or isKeyPressed("right shift"):
        if add==add.capitalize() and add in shifted:
                add=shifted[add]
        else:
                add=add.capitalize()
    box["string"]+=add
    if sameKeys(k,"enter"):
        box["data"]=box["string"]
        box["string"]=""

def drawinputbox(x,y,size=30):
        string=" "+box["string"]
        drawString(string,x,y,size,font="Arial")
