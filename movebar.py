from random import random
from sys import stdout
from time import sleep
import os

class A:
    def __init__(self,pos,char):
        self.pos=pos
        self.char=str(char)
    def move(self):
        self.pos+= -1
#        if self.pos==-1: self.pos=49
#        elif self.pos==50: self.pos=0


text = '!Msdfafasdfa fdasfasdf asd fas fasf as fasd fa sdfaf af afasf das fda sdfa dfa'
text2 = '!Samuel Wyatt and tla vainadafa'
text3 = '!Thomas Maccaronedas fdasf adf'
texts =[text,text2,text3]

for t in texts:
    aas=[]
    for i,j in enumerate(t):
        aas.append(A(i+47,j))
        #tmps=['n']
    tmp=["/"]+["-"]*48+["\\"]+[' ']*10
    for t in range(len(t)+ 47):
        stdout.write("\b"*60)
        tmp=["/"]+["-"]*48+["\\"]+[' ']*10
        tmps=""
        for a in aas:
            if a.pos!=0 and a.pos!= 49 and a.pos < 50 and a.pos >0:
                tmp[a.pos]=a.char
            a.move()
        for i in range(len(tmp)):
            tmps+=tmp[i]
        #stdout.write("\x1b]2;"+tmps+"\x07")
        stdout.write(tmps)
        stdout.flush()
        os.system('echo "'+tmps+'" > ~/aa.txt')
        sleep(.2)
