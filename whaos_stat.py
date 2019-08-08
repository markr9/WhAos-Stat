# -*- coding: utf-8 -*-
"""
Created on Sat May 18 13:50:39 2019

@author: MR
"""

from tkinter.ttk import *
from tkinter import *
import tkinter.messagebox as box
import numpy as np
from random import random
import matplotlib.pyplot as plt

#gui
class Gui1:
    
    def __init__(self,win,ops):
        self.win=win
        self.win.title('Wh AoS')
        self.frame=Frame(win)
        self.widgits()
        self.pos()
        self.commands()
        
    def widgits(self):        
        self.title=Label(self.win,text='Warhammer Age of Sigmar',font=('',12))
        self.btnSingle=Button(self.frame,text='Single')
        self.btnCompare=Button(self.frame,text='Compare')
        
    def pos(self):
        self.title.pack()
        self.frame.pack()
        self.btnSingle.pack(side=LEFT)
        self.btnCompare.pack(side=RIGHT)
        
    def commands(self):
        self.btnSingle.configure(command=lambda:self.setSingle())
        self.btnCompare.configure(command=lambda:self.setMulti())
        self.ops=Mode()
    
    def setSingle(self):
        ops.mode=1
        self.win.destroy()
        
    def setMulti(self):
        ops.mode=2
        self.win.destroy()
    
class Mode:
    mode=0
   
class Gui2:
    runnum=0
    
    def __init__(self,win):
        self.lines=1
        self.win=win
        self.win.title('Wh AoS')
        #self.frame=Frame(win)
        self.totframe=Frame(win)
        self.btnFrame=Frame(self.totframe)
        self.widgits()
        self.pos()
        self.addLine()
        self.commands()
        
    def widgits(self):
        self.canvas=Canvas(self.totframe)
        self.frame=Frame(self.canvas)
        self.scrollbar=Scrollbar(self.totframe,orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set,bg='blue')
        self.title=Label(self.totframe,text='Single unit ability',font=('',12))
        self.btnAdd=Button(self.btnFrame,text='Add line')
        self.btnDel=Button(self.btnFrame,text='Remove line')
        self.btnCal=Button(self.btnFrame,text='Calculate')
        self.txtotal=Label(self.btnFrame,text='Total')
        self.totmeans=Label(self.btnFrame,text=0.0)
        self.totstds=Label(self.btnFrame,text=0.0)
        self.sigmaFrame=Frame(self.totframe)
        self.tot1sigma=Label(self.sigmaFrame,text=0.0)
        self.tot2sigma=Label(self.sigmaFrame,text=0.0)
        self.txsize=Label(self.frame,text='Unit Size')
        self.txatk=Label(self.frame,text='Attacks')
        self.txth=Label(self.frame,text='To Hit')
        self.txtw=Label(self.frame,text='To Wound')
        self.txrend=Label(self.frame,text='Rend')
        self.txdam=Label(self.frame,text='Damage')
#        self.txoutch=Label(self.frame,text='Chance')
#        self.txoutuch=Label(self.frame,text='Unit Chance')
#        self.txoutd=Label(self.frame,text='Damage Output')
#        self.txouttd=Label(self.frame,text='Unit Damage')
#        self.txoutmw=Label(self.frame,text='Mortal wounds')
#        self.txoutumw=Label(self.frame,text='Unit Mortal Wounds')
        self.txtype=Label(self.frame,text='Type')
        self.txmeans=Label(self.frame,text='Means (2+,3+,4+,5+,6+,7+,sum)')
        self.txstd=Label(self.frame,text='S.D (2+,3+,4+,5+,6+,7+,sum)')
        self.tx1sd=Label(self.frame,text='1 sigma range')
        self.tx2sd=Label(self.frame,text='2 sigma range')
        
        self.widgitset=[]
        self.widgitset2=[]
        
    def pos(self):
        self.totframe.pack()
        self.title.pack()
        self.btnFrame.pack()
        self.btnAdd.pack(side='left')
        self.btnDel.pack(side='left')
        self.btnCal.pack(side='left')
        self.totstds.pack(side='right')
        self.totmeans.pack(side='right')
        self.txtotal.pack(side='right')
        self.sigmaFrame.pack()
        self.tot1sigma.pack(side='left')
        self.tot2sigma.pack(side='right')
        
        self.scrollbar.pack(side='right',fill=Y)
        self.canvas.pack(fill="both",expand=True)
        self.canvas.create_window((0,0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>",self.onFrameConfigure)
        
        
        #self.frame.pack()
        self.txsize.grid(row=0,column=0)
        self.txatk.grid(row=0,column=1)
        self.txth.grid(row=0,column=2,columnspan=2)
        self.txtw.grid(row=0,column=4,columnspan=2)
        self.txrend.grid(row=0,column=6)
        self.txdam.grid(row=0,column=7)
#        self.txoutch.grid(row=0,column=8)
#        self.txoutuch.grid(row=0,column=9)
#        self.txoutd.grid(row=0,column=10)
#        self.txouttd.grid(row=0,column=11)
#        self.txoutmw.grid(row=0,column=12)
#        self.txoutumw.grid(row=0,column=13)
        self.txtype.grid(row=0,column=8)
        self.txmeans.grid(row=0,column=9)
        self.txstd.grid(row=0,column=10)
        self.tx1sd.grid(row=0,column=11)
        self.tx2sd.grid(row=0,column=12)
        
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def addLine(self):
        #alFrame=Frame(self.win)
        size=Combobox(self.frame,width=2)
        i=1
        value=[]
        while i<=50:
            value.append(i)
            i+=1
        size.configure(values=value)
        size.set(1)
        atk=Combobox(self.frame,width=4)
        i=1
        value=['D3','D6','2D3','2D6']
        while i<=12:
            value.append(i)
            i+=1
        atk.configure(values=value)
        atk.set(1)
        th=Combobox(self.frame,values=['auto',2,3,4,5,6],width=1)
        th.set(4)
        pth=Label(self.frame,text='+')
        tw=Combobox(self.frame,values=[2,3,4,5,6],width=1)
        tw.set(4)
        ptw=Label(self.frame,text='+')
        rend=Combobox(self.frame,values=[0,-1,-2,-3],width=2)
        rend.set(0)
        dam=Combobox(self.frame,values=['D3','D6','2D3',1,2,3,4,5,6],width=4)
        dam.set(1)
#        outch=Label(self.frame,text=0.0)#,width=6)
#        outuch=Label(self.frame,text=0.0)#,width=12)
#        outd=Label(self.frame,text=0.0)#,width=9)
#        outtd=Label(self.frame,text=0.0)#,width=10)
#        outmw=Label(self.frame,text=0.0)
#        outumw=Label(self.frame,text=0.0)
        types=Label(self.frame,text='Normal\nMortal Wounds')
        means=Label(self.frame,text=0.0)
        stds=Label(self.frame,text=0.0)
        sigma1=Label(self.frame,text=0.0)
        sigma2=Label(self.frame,text=0.0)
        
        widgitline=[size,atk,th,pth,tw,ptw,rend,dam,types,means,stds,sigma1,sigma2]
        self.widgitset.append(widgitline)
        
        #alFrame.pack()
        size.grid(row=self.lines,column=0)
        atk.grid(row=self.lines,column=1)
        th.grid(row=self.lines,column=2,sticky=E)
        pth.grid(row=self.lines,column=3,sticky=W)
        tw.grid(row=self.lines,column=4,sticky=E)
        ptw.grid(row=self.lines,column=5,sticky=W)
        rend.grid(row=self.lines,column=6)
        dam.grid(row=self.lines,column=7)
#        outch.grid(row=self.lines,column=8)
#        outuch.grid(row=self.lines,column=9)
#        outd.grid(row=self.lines,column=10)
#        outtd.grid(row=self.lines,column=11)
#        outmw.grid(row=self.lines,column=12)
#        outumw.grid(row=self.lines,column=13)
        types.grid(row=self.lines,column=8)
        means.grid(row=self.lines,column=9)
        stds.grid(row=self.lines,column=10)
        sigma1.grid(row=self.lines,column=11)
        sigma2.grid(row=self.lines,column=12)
        
        #ops: re-roll 1s, re-roll 6s, re-roll all (hit+wound+attacks+damage), modifiers (all), 6s (hit+wound), multiply (hit+wound), mortal (hit+wound), rend mod (hit+wound), (6s dam x2 +1) add (6/6+ extra atk)
        opsFrame=Frame(self.frame)
        atkFrame=Frame(opsFrame)
        hitFrame=Frame(opsFrame)
        hit2Frame=Frame(opsFrame)
        woundFrame=Frame(opsFrame)
        wound2Frame=Frame(opsFrame)
        #rendFrame=Frame(opsFrame)
        #damageFrame=Frame(opsFrame)
        
        txatkop=Label(atkFrame,text='Attack options:')
        atkrrop=IntVar()
        cbatkrrop=Checkbutton(atkFrame,text='Re-roll',onvalue=1,offvalue=0,variable=atkrrop)
        cbatkmod=Combobox(atkFrame,values=[-3,-2,-1,0,1,2,3],width=2)
        cbatkmod.set(0)
        txatkmod=Label(atkFrame,text='Modifier')
        
        txrendop=Label(atkFrame,text='Rend options:')
        cbrendmod=Combobox(atkFrame,values=[-3,-2,-1,0],width=2)
        cbrendmod.set(0)
        txrendmod=Label(atkFrame,text='Modifier to')
        
        txdamop=Label(atkFrame,text='Damage options:')
        cbdammod=Combobox(atkFrame,values=['D3','D6','2D3','2D6',0,1,2,3,4,5,6,'x2','x3'],width=4)
        cbdammod.set(0)
        txdammod=Label(atkFrame,text='Modifier to +')
        cbdammod2=Combobox(atkFrame,values=['D3','D6','2D3','2D6',0,1,2,3,4,5,6,'-D3','-D6','-2D3','-2D6',-1,-2,-3,-4,-5,-6],width=5)
        cbdammod2.set(0)
        txdammod2=Label(atkFrame,text='Modifier')
        
        txsvop=Label(atkFrame,text='Save options:')
        cvop=IntVar()
        cbcvop=Checkbutton(atkFrame,text='Cover',onvalue=1,offvalue=0,variable=cvop)
        cbsvmod=Combobox(atkFrame,values=[-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6],width=5)
        cbsvmod.set(0)
        txsvmod=Label(atkFrame,text='Modifier')
        
        txhitop=Label(hitFrame,text='To hit options:')
        hitrrop=IntVar()
        cbhitrrop=Checkbutton(hitFrame,text='Re-roll',onvalue=1,offvalue=0,variable=hitrrop)
        hitrr1op=IntVar()
        cbhitrr1op=Checkbutton(hitFrame,text='Re-roll 1s',onvalue=1,offvalue=0,variable=hitrr1op)
        hitrr6op=IntVar()
        cbhitrr6op=Checkbutton(hitFrame,text='Re-roll 6s',onvalue=1,offvalue=0,variable=hitrr6op)
        cbhitmod=Combobox(hitFrame,values=[-3,-2,-1,0,1,2,3],width=2)
        cbhitmod.set(0)
        txhitmod=Label(hitFrame,text='Modifier')
        
        cbhit6op=Combobox(hitFrame,values=[0,2,3,'D3','D6','2D3','2D6'],width=4)
        cbhit6op.set(0)
        txhit6op=Label(hitFrame,text='6s x hits')
        cbhit6pop=Combobox(hitFrame,values=[0,2,3,'D3','D6','2D3','2D6'],width=4)
        cbhit6pop.set(0)
        txhit6pop=Label(hitFrame,text='6+ x hits')
        cbhitxop=Combobox(hitFrame,values=[0,2,3,'D3','D6','2D3','2D6'],width=4)
        cbhitxop.set(0)
        txhitxop=Label(hitFrame,text='hit x hits')
        
#        hit62op=IntVar()
#        cbhit62op=Checkbutton(hitFrame,text='6s 2 hits',onvalue=1,offvalue=0,variable=hit62op)
#        hit63op=IntVar()
#        cbhit63op=Checkbutton(hitFrame,text='6s 3 hits',onvalue=1,offvalue=0,variable=hit63op)
#        hit6p2op=IntVar()
#        cbhit6p2op=Checkbutton(hitFrame,text='6+ 2 hits',onvalue=1,offvalue=0,variable=hit6p2op)
#        hit6p3op=IntVar()
#        cbhit6p3op=Checkbutton(hitFrame,text='6+ 3 hits',onvalue=1,offvalue=0,variable=hit6p3op)
#        hitd3op=IntVar()
#        cbhitd3op=Checkbutton(hitFrame,text='hit D3 hits',onvalue=1,offvalue=0,variable=hitd3op)
#        hitd6op=IntVar()
#        cbhitd6op=Checkbutton(hitFrame,text='hit D6 hits',onvalue=1,offvalue=0,variable=hitd6op)
        
        hit6aop=IntVar()
        cbhit6aop=Checkbutton(hitFrame,text='6s +1a',onvalue=1,offvalue=0,variable=hit6aop)
        hit6paop=IntVar()
        cbhit6paop=Checkbutton(hitFrame,text='6+ +1a',onvalue=1,offvalue=0,variable=hit6paop)
        cbhit6rend=Combobox(hitFrame,values=[-3,-2,-1,0],width=2)
        cbhit6rend.set(0)
        txhit6rend=Label(hitFrame,text='6s Rend')
        cbhit6prend=Combobox(hitFrame,values=[-3,-2,-1,0],width=2)
        cbhit6prend.set(0)
        txhit6prend=Label(hitFrame,text='6+ Rend')
        cbhit6dam=Combobox(hit2Frame,values=['D3','D6','2D3','2D6',0,1,2,3,4,5,6,'x2','x3'],width=5)
        cbhit6dam.set(0)
        txhit6dam=Label(hit2Frame,text='6s Damage  modifier to +')
        cbhit6dam2=Combobox(hit2Frame,values=['D3','D6','2D3','2D6',0,1,2,3,4,5,6],width=5)
        cbhit6dam2.set(0)
        txhit6dam2=Label(hit2Frame,text='6s Damage  modifier')
        cbhit6pdam=Combobox(hit2Frame,values=['D3','D6','2D3','2D6',0,1,2,3,4,5,6,'x2','x3'],width=5)
        cbhit6pdam.set(0)
        txhit6pdam=Label(hit2Frame,text='6+ Damage  modifier to +')
        cbhit6pdam2=Combobox(hit2Frame,values=['D3','D6','2D3','2D6',0,1,2,3,4,5,6],width=5)
        cbhit6pdam2.set(0)
        txhit6pdam2=Label(hit2Frame,text='6+ Damage  modifier')
        cbhit6mw=Combobox(hit2Frame,values=['D3','D6','2D3','2D6',0,1,2,3,4,5,6,'D3 atk end','D6 atk end','2D3 atk end','2D6 atk end','1 atk end','2 atk end','3 atk end','4 atk end','5 atk end','6 atk end'],width=10)
        cbhit6mw.set(0)
        txhit6mw=Label(hit2Frame,text='6s mortal wound')
        cbhit6pmw=Combobox(hit2Frame,values=['D3','D6','2D3','2D6',0,1,2,3,4,5,6,'D3 atk end','D6 atk end','2D3 atk end','2D6 atk end','1 atk end','2 atk end','3 atk end','4 atk end','5 atk end','6 atk end'],width=10)
        cbhit6pmw.set(0)
        txhit6pmw=Label(hit2Frame,text='6+ mortal wound')
        cbhitmw=Combobox(hit2Frame,values=[0,'D3 atk end','D6 atk end','2D3 atk end','2D6 atk end','1 atk end','2 atk end','3 atk end','4 atk end','5 atk end','6 atk end'],width=10)
        cbhitmw.set(0)
        txhitmw=Label(hit2Frame,text='mortal wound hit')
        
        txwoundop=Label(woundFrame,text='To wound options:')
        woundrrop=IntVar()
        cbwoundrrop=Checkbutton(woundFrame,text='Re-roll',onvalue=1,offvalue=0,variable=woundrrop)
        woundrr1op=IntVar()
        cbwoundrr1op=Checkbutton(woundFrame,text='Re-roll 1s',onvalue=1,offvalue=0,variable=woundrr1op)
        woundrr6op=IntVar()
        cbwoundrr6op=Checkbutton(woundFrame,text='Re-roll 6s',onvalue=1,offvalue=0,variable=woundrr6op)
        
        cbwoundmod=Combobox(woundFrame,values=[-3,-2,-1,0,1,2,3],width=2)
        cbwoundmod.set(0)
        txwoundmod=Label(woundFrame,text='Modifier')
        
        cbwound6op=Combobox(woundFrame,values=[0,2,3,'D3','D6','2D3','2D6'],width=4)
        cbwound6op.set(0)
        txwound6op=Label(woundFrame,text='6s x wounds')
        cbwound6pop=Combobox(woundFrame,values=[0,2,3,'D3','D6','2D3','2D6'],width=4)
        cbwound6pop.set(0)
        txwound6pop=Label(woundFrame,text='6+ x wounds')
        cbwoundxop=Combobox(woundFrame,values=[0,2,3,'D3','D6','2D3','2D6'],width=4)
        cbwoundxop.set(0)
        txwoundxop=Label(woundFrame,text='wound x wounds')
        
#        wound62op=IntVar()
#        cbwound62op=Checkbutton(woundFrame,text='6s 2 wounds',onvalue=1,offvalue=0,variable=wound62op)
#        wound63op=IntVar()
#        cbwound63op=Checkbutton(woundFrame,text='6s 3 wounds',onvalue=1,offvalue=0,variable=wound63op)
#        wound6p2op=IntVar()
#        cbwound6p2op=Checkbutton(woundFrame,text='6+ 2 wound',onvalue=1,offvalue=0,variable=wound6p2op)
#        wound6p3op=IntVar()
#        cbwound6p3op=Checkbutton(woundFrame,text='6+ 3 wound',onvalue=1,offvalue=0,variable=wound6p3op)
#        woundd3op=IntVar()
#        cbwoundd3op=Checkbutton(woundFrame,text='wound D3 wounds',onvalue=1,offvalue=0,variable=woundd3op)
#        woundd6op=IntVar()
#        cbwoundd6op=Checkbutton(woundFrame,text='wound D6 wounds',onvalue=1,offvalue=0,variable=woundd6op)
        
        wound6aop=IntVar()
        cbwound6aop=Checkbutton(woundFrame,text='6s +1a',onvalue=1,offvalue=0,variable=wound6aop)
        wound6paop=IntVar()
        cbwound6paop=Checkbutton(woundFrame,text='6+ +1a',onvalue=1,offvalue=0,variable=wound6paop)
        cbwound6rend=Combobox(woundFrame,values=[-3,-2,-1,0],width=2)
        cbwound6rend.set(0)
        txwound6rend=Label(woundFrame,text='6s Rend')
        cbwound6prend=Combobox(woundFrame,values=[-3,-2,-1,0],width=2)
        cbwound6prend.set(0)
        txwound6prend=Label(woundFrame,text='6+ Rend')
        cbwound6dam=Combobox(wound2Frame,values=['D3','D6','2D3','2D6',0,1,2,3,4,5,6,'x2','x3'],width=5)
        cbwound6dam.set(0)
        txwound6dam=Label(wound2Frame,text='6s Damage  modifier to +')
        cbwound6dam2=Combobox(wound2Frame,values=['D3','D6','2D3','2D6',0,1,2,3,4,5,6],width=5)
        cbwound6dam2.set(0)
        txwound6dam2=Label(wound2Frame,text='6s Damage  modifier')
        cbwound6pdam=Combobox(wound2Frame,values=['D3','D6','2D3','2D6',0,1,2,3,4,5,6,'x2','x3'],width=5)
        cbwound6pdam.set(0)
        txwound6pdam=Label(wound2Frame,text='6+ Damage  modifier to +')
        cbwound6pdam2=Combobox(wound2Frame,values=['D3','D6','2D3','2D6',0,1,2,3,4,5,6],width=5)
        cbwound6pdam2.set(0)
        txwound6pdam2=Label(wound2Frame,text='6+ Damage  modifier')
        cbwound6mw=Combobox(wound2Frame,values=['D3','D6','2D3','2D6',0,1,2,3,4,5,6,'D3 atk end','D6 atk end','2D3 atk end','2D6 atk end','1 atk end','2 atk end','3 atk end','4 atk end','5 atk end','6 atk end'],width=10)
        cbwound6mw.set(0)
        txwound6mw=Label(wound2Frame,text='6s mortal wound')
        cbwound6pmw=Combobox(wound2Frame,values=['D3','D6','2D3','2D6',0,1,2,3,4,5,6,'D3 atk end','D6 atk end','2D3 atk end','2D6 atk end','1 atk end','2 atk end','3 atk end','4 atk end','5 atk end','6 atk end'],width=10)
        cbwound6pmw.set(0)
        txwound6pmw=Label(wound2Frame,text='6+ mortal wound')
        cbwoundmw=Combobox(wound2Frame,values=[0,'D3 atk end','D6 atk end','2D3 atk end','2D6 atk end','1 atk end','2 atk end','3 atk end','4 atk end','5 atk end','6 atk end'],width=10)
        cbwoundmw.set(0)
        txwoundmw=Label(wound2Frame,text='mortal wound wound')
        
        #sd ranges
        sd1r=Label(self.frame,text=0.0)
        sd2r=Label(self.frame,text=0.0)
        sd1r.grid(row=self.lines+1,column=0,columnspan=7)
        sd2r.grid(row=self.lines+1,column=7,columnspan=7)
        
        widgitline2={'txatkop':txatkop,'cbatkrrop':cbatkrrop,'atkrrop':atkrrop,'cbatkmod':cbatkmod,'txatkmod':txatkmod,'txrendop':txrendop,'cbrendmod':cbrendmod,'txrendmod':txrendmod,'txdamop':txdamop,'cbdammod':cbdammod,'txdammod':txdammod,'cbdammod2':cbdammod2,'txdammod2':txdammod2,'txsvop':txsvop,'cvop':cvop,'cbcvop':cbcvop,'cbsvmod':cbsvmod,'txsvmod':txsvmod,
                     'txhitop':txhitop,'cbhitrrop':cbhitrrop,'hitrrop':hitrrop,'cbhitrr1op':cbhitrr1op,'hitrr1op':hitrr1op,'cbhitrr6op':cbhitrr6op,'hitrr6op':hitrr6op,'cbhitmod':cbhitmod,'txhitmod':txhitmod,'cbhit6op':cbhit6op,'txhit6op':txhit6op,'cbhit6pop':cbhit6pop,'txhit6pop':txhit6pop,'cbhitxop':cbhitxop,'txhitxop':txhitxop,'cbhit6aop':cbhit6aop,'hit6aop':hit6aop,'cbhit6paop':cbhit6paop,'hit6paop':hit6paop,'cbhit6rend':cbhit6rend,'txhit6rend':txhit6rend,'cbhit6prend':cbhit6prend,'txhit6prend':txhit6prend,'cbhit6dam':cbhit6dam,'txhit6dam':txhit6dam,'cbhit6dam2':cbhit6dam2,'txhit6dam2':txhit6dam2,'cbhit6pdam':cbhit6pdam,'txhit6pdam':txhit6pdam,'cbhit6pdam2':cbhit6pdam2,'txhit6pdam2':txhit6pdam2,'cbhit6mw':cbhit6mw,'txhit6mw':txhit6mw,'cbhit6pmw':cbhit6pmw,'txhit6pmw':txhit6pmw,'cbhitmw':cbhitmw,'txhitmw':txhitmw,
                     'txwoundop':txwoundop,'cbwoundrrop':cbwoundrrop,'woundrrop':woundrrop,'cbwoundrr1op':cbwoundrr1op,'woundrr1op':woundrr1op,'cbwoundrr6op':cbwoundrr6op,'woundrr6op':woundrr6op,'cbwoundmod':cbwoundmod,'txwoundmod':txwoundmod,'cbwound6op':cbwound6op,'txwound6op':txwound6op,'cbwound6pop':cbwound6pop,'txwound6pop':txwound6pop,'cbwoundxop':cbwoundxop,'txwoundxop':txwoundxop,'cbwound6aop':cbwound6aop,'wound6aop':wound6aop,'cbwoun6paop':cbwound6paop,'wound6paop':wound6paop,'cbwound6rend':cbwound6rend,'txwound6rend':txwound6rend,'cbwound6prend':cbwound6prend,'txwound6prend':txwound6prend,'cbwound6dam':cbwound6dam,'txwound6dam':txwound6dam,'cbwound6dam2':cbwound6dam2,'txwound6dam2':txwound6dam2,'cbwound6pdam':cbwound6pdam,'txwound6pdam':txwound6pdam,'cbwound6pdam2':cbwound6pdam2,'txwound6pdam2':txwound6pdam2,'cbwound6mw':cbwound6mw,'txwound6mw':txwound6mw,'cbwound6pmw':cbwound6pmw,'txwound6pmw':txwound6pmw,'cbwoundmw':cbwoundmw,'txwoundmw':txwoundmw,
                     'opsFrame':opsFrame,'atkFrame':atkFrame,'hitFrame':hitFrame,'hit2Frame':hit2Frame,'woundFrame':woundFrame,'wound2Frame':wound2Frame,
                     'sd1':sd1r,'sd2':sd2r}
        
        self.widgitset2.append(widgitline2)
        
        opsFrame.grid(row=self.lines+2,column=0,columnspan=14)
        
        atkFrame.pack()
        txatkop.pack(side='left')
        cbatkrrop.pack(side='left')
        cbatkmod.pack(side='left')
        txatkmod.pack(side='left')
        txrendop.pack(side='left')
        cbrendmod.pack(side='left')
        txrendmod.pack(side='left')
        txdamop.pack(side='left')
        cbdammod.pack(side='left')
        txdammod.pack(side='left')
        cbdammod2.pack(side='left')
        txdammod2.pack(side='left')
        txsvop.pack(side='left')
        cbcvop.pack(side='left')
        cbsvmod.pack(side='left')
        txsvmod.pack(side='left')

        hitFrame.pack()
        hit2Frame.pack()
        txhitop.pack(side='left')
        cbhitrrop.pack(side='left')
        cbhitrr1op.pack(side='left')
        cbhitrr6op.pack(side='left')
        #cbhit62op.pack(side='left')
        #cbhit63op.pack(side='left')
        cbhitmod.pack(side='left')
        txhitmod.pack(side='left')
        cbhit6op.pack(side='left')
        txhit6op.pack(side='left')
        cbhit6pop.pack(side='left')
        txhit6pop.pack(side='left')
        cbhitxop.pack(side='left')
        txhitxop.pack(side='left')
        #cbhit6p2op.pack(side='left')
        #cbhit6p3op.pack(side='left')
        #cbhitd3op.pack(side='left')
        #cbhitd6op.pack(side='left')
        cbhit6aop.pack(side='left')
        cbhit6paop.pack(side='left')
        cbhit6rend.pack(side='left')
        txhit6rend.pack(side='left')
        cbhit6prend.pack(side='left')
        txhit6prend.pack(side='left')
        cbhit6dam.pack(side='left')
        txhit6dam.pack(side='left')
        cbhit6dam2.pack(side='left')
        txhit6dam2.pack(side='left')
        cbhit6pdam.pack(side='left')
        txhit6pdam.pack(side='left')
        cbhit6pdam2.pack(side='left')
        txhit6pdam2.pack(side='left')
        cbhit6mw.pack(side='left')
        txhit6mw.pack(side='left')
        cbhit6pmw.pack(side='left')
        txhit6pmw.pack(side='left')
        cbhitmw.pack(side='left')
        txhitmw.pack(side='left')
        
        woundFrame.pack()
        wound2Frame.pack()
        txwoundop.pack(side='left')
        cbwoundrrop.pack(side='left')
        cbwoundrr1op.pack(side='left')
        cbwoundrr6op.pack(side='left')
        #cbwound62op.pack(side='left')
        #cbwound63op.pack(side='left')
        cbwoundmod.pack(side='left')
        txwoundmod.pack(side='left')
        cbwound6op.pack(side='left')
        txwound6op.pack(side='left')
        cbwound6pop.pack(side='left')
        txwound6pop.pack(side='left')
        cbwoundxop.pack(side='left')
        txwoundxop.pack(side='left')
        #cbwound6p2op.pack(side='left')
        #cbwound6p3op.pack(side='left')
        #cbwoundd3op.pack(side='left')
        #cbwoundd6op.pack(side='left')
        cbwound6aop.pack(side='left')
        cbwound6paop.pack(side='left')
        cbwound6rend.pack(side='left')
        txwound6rend.pack(side='left')
        cbwound6prend.pack(side='left')
        txwound6prend.pack(side='left')
        cbwound6dam.pack(side='left')
        txwound6dam.pack(side='left')
        cbwound6dam2.pack(side='left')
        txwound6dam2.pack(side='left')
        cbwound6pdam.pack(side='left')
        txwound6pdam.pack(side='left')
        cbwound6pdam2.pack(side='left')
        txwound6pdam2.pack(side='left')
        cbwound6mw.pack(side='left')
        txwound6mw.pack(side='left')
        cbwound6pmw.pack(side='left')
        txwound6pmw.pack(side='left')
        cbwoundmw.pack(side='left')
        txwoundmw.pack(side='left')
        
        self.lines+=3
        self.btnDel.configure(state=NORMAL)
        
        self.sizerest()
        
    def sizerest(self):
        self.frame.update()
        h=self.frame.winfo_height()
        w=self.frame.winfo_width()
        self.canvas.configure(width=w,height=h)
        #print(h,w)
        
    def removeLine(self):
        for x in self.widgitset[-1]:
            x.destroy()
        for y in self.widgitset2[-1].copy():
            try:
                self.widgitset2[-1][y].destroy()
            except Exception:
                del self.widgitset2[-1][y]
        self.widgitset.pop()
        self.widgitset2.pop()
        self.lines-=2
        if self.lines==3:
            self.btnDel.configure(state=DISABLED)
        self.sizerest()
        
    def adddata(self,data,line,line2,v):
        #print(data)
        tx='%.3f'%data[0][0]+', '+'%.3f'%data[0][2]+', '+'%.3f'%data[0][4]+', '+'%.3f'%data[0][6]+', '+'%.3f'%data[0][8]+', '+'%.3f'%data[0][10]+', '+'%.3f'%data[2][0]+'\n'+'%.3f'%data[0][1]+', '+'%.3f'%data[0][3]+', '+'%.3f'%data[0][5]+', '+'%.3f'%data[0][7]+', '+'%.3f'%data[0][9]+', '+'%.3f'%data[0][11]+', '+'%.3f'%data[2][1]
        tx2='%.3f'%data[1][0]+', '+'%.3f'%data[1][2]+', '+'%.3f'%data[1][4]+', '+'%.3f'%data[1][6]+', '+'%.3f'%data[1][8]+', '+'%.3f'%data[1][10]+', '+'%.3f'%data[3][0]+'\n'+'%.3f'%data[1][1]+', '+'%.3f'%data[1][3]+', '+'%.3f'%data[1][5]+', '+'%.3f'%data[1][7]+', '+'%.3f'%data[1][9]+', '+'%.3f'%data[1][11]+', '+'%.3f'%data[3][1]
        sd1=[data[0][0]+data[1][0],data[0][2]+data[1][2],data[0][4]+data[1][4],data[0][6]+data[1][6],data[0][8]+data[1][8],data[0][10]+data[1][10],data[2][0]+data[3][0],data[0][1]+data[1][1],data[0][3]+data[1][3],data[0][5]+data[1][5],data[0][7]+data[1][7],data[0][9]+data[1][9],data[0][11]+data[1][11],data[2][1]+data[3][1]]
        sd11=[data[0][0]-data[1][0],data[0][2]-data[1][2],data[0][4]-data[1][4],data[0][6]-data[1][6],data[0][8]-data[1][8],data[0][10]-data[1][10],data[2][0]-data[3][0],data[0][1]-data[1][1],data[0][3]-data[1][3],data[0][5]-data[1][5],data[0][7]-data[1][7],data[0][9]-data[1][9],data[0][11]-data[1][11],data[2][1]-data[3][1]]
        tx3='%.3f'%+sd11[0]+'-'+'%.3f'%+sd1[0]+', '+'%.3f'%sd11[1]+'-'+'%.3f'%sd1[1]+', '+'%.3f'%sd11[2]+'-'+'%.3f'%sd1[2]+', '+'%.3f'%sd11[3]+'-'+'%.3f'%sd1[3]+', '+'%.3f'%sd11[4]+'-'+'%.3f'%sd1[4]+', '+'%.3f'%sd11[5]+'-'+'%.3f'%sd1[5]+', '+'%.3f'%sd11[6]+'-'+'%.3f'%sd1[6]+'\n'+'%.3f'%sd11[7]+'-'+'%.3f'%sd1[7]+', '+'%.3f'%sd11[8]+'-'+'%.3f'%sd1[8]+', '+'%.3f'%sd11[9]+'-'+'%.3f'%sd1[9]+', '+'%.3f'%sd11[10]+'-'+'%.3f'%sd1[10]+', '+'%.3f'%sd11[11]+'-'+'%.3f'%sd1[11]+', '+'%.3f'%sd11[12]+'-'+'%.3f'%sd1[12]+', '+'%.3f'%sd11[13]+'-'+'%.3f'%sd1[13]
        sd2=[data[0][0]+data[1][0]*2,data[0][2]+data[1][2]*2,data[0][4]+data[1][4]*2,data[0][6]+data[1][6]*2,data[0][8]+data[1][8]*2,data[0][10]+data[1][10]*2,data[2][0]+data[3][0]*2,data[0][1]+data[1][1]*2,data[0][3]+data[1][3]*1,data[0][5]+data[1][5]*2,data[0][7]+data[1][7]*2,data[0][9]+data[1][9]*2,data[0][11]+data[1][11]*2,data[2][1]+data[3][1]*2]
        sd21=[data[0][0]-data[1][0]*2,data[0][2]-data[1][2]*2,data[0][4]-data[1][4]*2,data[0][6]-data[1][6]*2,data[0][8]-data[1][8]*2,data[0][10]-data[1][10]*2,data[2][0]-data[3][0]*2,data[0][1]-data[1][1]*2,data[0][3]-data[1][3]*1,data[0][5]-data[1][5]*2,data[0][7]-data[1][7]*2,data[0][9]-data[1][9]*2,data[0][11]-data[1][11]*2,data[2][1]-data[3][1]*2]
        tx4='%.3f'%+sd21[0]+'-'+'%.3f'%+sd2[0]+', '+'%.3f'%sd21[1]+'-'+'%.3f'%sd2[1]+', '+'%.3f'%sd21[2]+'-'+'%.3f'%sd2[2]+', '+'%.3f'%sd21[3]+'-'+'%.3f'%sd2[3]+', '+'%.3f'%sd21[4]+'-'+'%.3f'%sd2[4]+', '+'%.3f'%sd21[5]+'-'+'%.3f'%sd2[5]+', '+'%.3f'%sd21[6]+'-'+'%.3f'%sd2[6]+'\n'+'%.3f'%sd21[7]+'-'+'%.3f'%sd2[7]+', '+'%.3f'%sd21[8]+'-'+'%.3f'%sd2[8]+', '+'%.3f'%sd21[9]+'-'+'%.3f'%sd2[9]+', '+'%.3f'%sd21[10]+'-'+'%.3f'%sd2[10]+', '+'%.3f'%sd21[11]+'-'+'%.3f'%sd2[11]+', '+'%.3f'%sd21[12]+'-'+'%.3f'%sd2[12]+', '+'%.3f'%sd21[13]+'-'+'%.3f'%sd2[13]
        #'%.3f'%+sd2[0]+', '+'%.3f'%sd2[1]+', '+'%.3f'%sd2[2]+', '+'%.3f'%sd2[3]+', '+'%.3f'%sd2[4]+', '+'%.3f'%sd2[5]+', '+'%.3f'%sd2[6]+'\n'+'%.3f'%sd2[7]+', '+'%.3f'%sd2[8]+', '+'%.3f'%sd2[9]+', '+'%.3f'%sd2[10]+', '+'%.3f'%sd2[11]+', '+'%.3f'%sd2[12]+', '+'%.3f'%sd2[13]
        
        if v==1:
            line[9].configure(text=tx)
            line[10].configure(text=tx2)
            line[11].configure(text='See below')
            line2['sd1'].configure(text=tx3)
            line[12].configure(text='See below')
            line2['sd2'].configure(text=tx4)
        else:
            self.totmeans.configure(text='Means: '+tx)
            self.totstds.configure(text='S.D.: '+tx2)
            self.tot1sigma.configure(text=tx3)
            self.tot2sigma.configure(text=tx4)
    
    def roll(self,values,rolls,results):
        i=0
        while i<rolls:
                a=int(random()*6+1)
                #results[a-1]+=1
                values[i]=a
                #effects.append(0)
                i+=1
                
        j=0
        while j<6:
            results[j]=values.count(j+1)
            j+=1
        b=max(results)
        c=min(results)
        ##diff=np.round((b-c)/rolls*100,3)
        ##print('rolls 1-6',results,'total',rolls,'variance',diff,'%')
        return values
    
    def attacks(self,atks,line2):
        try: 
            int(atks)
            atks+=int(line2['cbatkmod'].get())
        except Exception:
            halves={'D3':2,'D6':3,'2D3':4,'2D6':7}
            atks2=self.dxconvert(atks)
            if line2['atkrrop']==1:
                if atks2<halves[atks]:
                    atks2=self.dxconvert(atks)
            atks=atks2+int(line2['cbatkmod'].get())
        return atks
    
    def calculate(self):
        Gui2.runnum+=1
        print('\nrun number',Gui2.runnum)
        graph=Graph()
        #total=0
        #totalmw=0
        self.sv=0 #value rotate each round
        rounds=6e5
        ii=0
        while ii<len(self.widgitset):
            print('weapon',ii+1,'total',len(self.widgitset))
            line=self.widgitset[ii]
            line2=self.widgitset2[ii]
            self.sv=-1
        #for line in self.widgitset:
            #get roll
            scale=10
            atkmod=self.attacks(line[1].get(),line2)
            rolls=atkmod*int(line[0].get())#*scale
            rollresults=[]
            mwresults=[]
            #saveresults=[]
            z=0
            while z<rounds:
                if z%10000==0:
                    print(z)
                results=[0,0,0,0,0,0]
                values=[0]*rolls
                effects=[0]*rolls
                mw=[0,0] #instances,total
                
    #            for x in values:
    #                effects.append(0)
                
                #save this round
                self.sv+=1
                if self.sv>5:
                    self.sv=0
    
                #hit
                values,effects,mw=self.tohit(line,line2,values,effects,mw,results,rolls)
                ##print('start',rolls,'end',len(values))
                h=len(values)/rolls
                ##print('hit',len(values)/rolls,h,'mortal wounds',mw[1])#review
                #multi hits
                values,effects=self.multi6s(values,effects,line2,'hit')
                w=s=1
                #wound
                if len(values)!=0:
                    a=len(values)
                    values,effects,mw=self.towound(line,line2,values,effects,mw,results)
                    ##print('start',rolls,'end',len(values))
                    w=len(values)/a
                    ##print('wound',len(values)/rolls,w,'mortal wounds',mw[1])
                    #multi wounds
                    values,effects=self.multi6s(values,effects,line2,'wound')
                #saves
                if len(values)!=0:
                    a=len(values)
                    values,effects=self.tosave(values,effects,results,line,line2)
                    s=len(values)/a
                    ##print('save fails',len(values)/rolls,s)#mw[0]
                
                ##print('sucess chance',len(values)/rolls,h*w*s,'mortal wounds',mw[1])
                model=len(values)
                ###print(model)
                modelmw=mw[1]#/scale
                ##print('model chance',model,'mortal wounds',modelmw)
                #unit=model*int(line[0].get())
                #unitmw=modelmw*int(line[0].get())
                #print('unit chance',unit,'mortal wounds',unitmw)
                #line[8].configure(text='%.5f'%model)
                #line[9].configure(text='%.5f'%unit)
                #line[12].configure(text='%.5f'%modelmw)
                #line[13].configure(text='%.5f'%unitmw)
                
                #damage
                damagemodel=0
                if len(values)!=0:
                    dam=self.todamage(values,effects,line,line2)/len(values)
                    ##print('damage',dam)
                    damagemodel=(dam*model)#/scale
                    ###print(damagemodel,dam,model)
                    #damageunit=unit*dam
                    ##print('model damage',damagemodel)
                    #print('unit damage',damageunit)
                    #line[10].configure(text='%.5f'%damagemodel)
                    #line[11].configure(text='%.5f'%damageunit)
                
                    #total+=damageunit
                #totalmw+=unitmw
                rollresults.append(damagemodel)
                mwresults.append(modelmw)
                #saveresults.append(self.sv+2)
                z+=1
            
            print('result',len(rollresults),len(mwresults))#,len(saveresults))
            #print(rollresults)#,saveresults)
            allmeans,allstds,totmean,totstd=graph.plotdata(rollresults,mwresults)
            dataset=[allmeans,allstds,totmean,totstd]
            self.adddata(dataset,line,line2,1)
            ii+=1
            #widgitline[size,atk,th,pth,tw,ptw,rend,dam,outch,outuch,outd,outtd]
        #self.total.configure(text='%.5f'%total)
        #self.totalmw.configure(text='%.5f'%totalmw)
        summeans,sumstds,sumtotmean,sumtotstd=graph.plottotal()
        datasettot=[summeans,sumstds,sumtotmean,sumtotstd]
        self.adddata(datasettot,line,line2,2)
        
        print('Complete!')
        
            
    def tohit(self,line,line2,values,effects,mw,results,rolls):
        #hit
        if line[2].get()=='auto':
            hittarget=1
            mod=0
        else:
            hittarget=int(line[2].get())
            mod=int(line2['cbhitmod'].get())
        values=self.roll(values,rolls,results)
        rerolled=[]
        effectsr=[]
        if hittarget!=1:
            #re-rolls: yours then oppoenents
            #re-roll 1s
            if line2['hitrr1op'].get()==1:
                values,rerolled,effects,effectsr=self.reroll1s(values,rerolled,effects,effectsr)
            #re-roll failed (before mod)
            if line2['hitrrop'].get()==1:
                values,rerolled,effects,effectsr=self.rerollfail(values,rerolled,hittarget,mod,effects,effectsr)
            #re-roll 6s
            if line2['hitrr6op'].get()==1:
                values,rerolled,effects,effectsr=self.reroll6s(values,rerolled,effects,effectsr)
            #extra atks 
            if (line2['hit6aop'].get()==1 or line2['hit6paop'].get()==1):
                values,effects,mw=self.ex6s1a(values,rerolled,line,line2,mod,hittarget,effects,effectsr,'hit',mw)
            #put together all values
            for x in rerolled:
                values.append(x)
            for y in effectsr:
                effects.append(y)
            #unmod effects
            #remove all 1s
            values,effects=self.fail1s(values,effects)
            #mw 6
            if (line2['cbhit6mw'].get()!='0' or line2['cbhit6pmw'].get()!='0'):
                values,mw=self.mw6s(values,line2,mod,mw,'hit')
        #mw ending roll
        if line2['cbhitmw'].get()!='0':
            j=0
            while j<len(values):
                if values[j]>=hittarget:
                    x=self.dxconvert(line2['cbhitmw'].get())
                    mw[0]+=1
                    mw[1]+=x
                j+=1
            #end fn
            #do
            #print(values,effects)
            ##print('mod',mod,'rr',len(rerolled),'values',len(values),'effects',len(effects),'mw',mw)
            return [],[],mw
        if hittarget!=1:
            #rend and damage on 6
            if (line2['cbhit6rend'].get()!='0' or line2['cbhit6prend'].get()!='0' or line2['cbhit6dam'].get()!='0' or line2['cbhit6dam2'].get()!='0' or line2['cbhit6pdam'].get()!='0' or line2['cbhit6pdam2'].get()!='0'):
                effects=self.renddameffects(values,effects,mod,1)
        #hit or missed
        values,effects=self.rollpass(values,effects,hittarget,mod,'hit')
#        #multi hits
#        values,effects=self.multi6s(values,effects,hittarget,mod,line2,'hit')

        #print(values,effects)
        ##print('mod',mod,'rr',len(rerolled),'values',len(values),'effects',len(effects),'mw',mw)
        
        return values,effects,mw
    
    def towound(self,line,line2,values,effects,mw,results):
        #wound
        values=self.roll(values,len(values),results)
        woundtarget=int(line[4].get())
        mod=int(line2['cbwoundmod'].get())
        rerolled=[]
        effectsr=[]
        #re-rolls: yours then oppoenents
        #re-roll 1s
        if line2['woundrr1op'].get()==1:
            values,rerolled,effects,effectsr=self.reroll1s(values,rerolled,effects,effectsr)
        #re-roll failed (before mod)
        if line2['woundrrop'].get()==1:
            values,rerolled,effects,effectsr=self.rerollfail(values,rerolled,woundtarget,mod,effects,effectsr)
        #re-roll 6s
        if line2['woundrr6op'].get()==1:
            values,rerolled,effects,effectsr=self.reroll6s(values,rerolled,effects,effectsr)
        #extra atks 
        if (line2['wound6aop'].get()==1 or line2['wound6paop'].get()==1):
            values,effects,mw=self.ex6s1a(values,rerolled,line,line2,mod,woundtarget,effects,effectsr,'wound',mw)
        #put together all values
        for x in rerolled:
            values.append(x)
        for y in effectsr:
            effects.append(y)
        #unmod effects
        #remove all 1s
        values,effects=self.fail1s(values,effects)
        #mw 6
        if (line2['cbwound6mw'].get()!='0' or line2['cbwound6pmw'].get()!='0'):
            values,mw=self.mw6s(values,line2,mod,mw,'wound')
        #mw ending roll
        if line2['cbwoundmw'].get()!='0':
            j=0
            while j<len(values):
                if values[j]>=woundtarget:
                    x=self.dxconvert(line2['cbwoundmw'].get())
                    mw[0]+=1
                    mw[1]+=x
                j+=1
            #end fn
            #do
            #print(values,effects)
            ##print('mod',mod,'rr',len(rerolled),'values',len(values),'effects',len(effects),'mw',mw)
            return [],[],mw
        #rend and damage on 6
        if (line2['cbwound6rend'].get()!='0' or line2['cbwound6prend'].get()!='0' or line2['cbwound6dam'].get()!='0' or line2['cbwound6dam2'].get()!='0' or line2['cbwound6pdam'].get()!='0' or line2['cbwound6pdam2'].get()!='0'):
            effects=self.renddameffects(values,effects,mod,3)
        #wound or not
        values,effects=self.rollpass(values,effects,woundtarget,mod,'wound')
#        #multi wounds
#        values,effects=self.multi6s(values,effects,woundtarget,mod,line2,'wound')
        
        #print(values,effects)
        ##print('mod',mod,'rr',len(rerolled),'values',len(values),'effects',len(effects),'mw',mw)
        
        return values,effects,mw
            
    def tosave(self,values,effects,results,line,line2):
        values=self.roll(values,len(values),results)
        mod=0
        mod+=(int(line2['cvop'].get())+int(line2['cbsvmod'].get()))
        mod2=[int(line2['cbhit6rend'].get()),int(line2['cbhit6prend'].get()),int(line2['cbwound6rend'].get()),int(line2['cbwound6prend'].get()),int(line[6].get()),int(line2['cbrendmod'].get())]
        values,effects=self.rollpass(values,effects,mod,mod2,'save')
        
        #print(values,effects)
        ##print('mod',mod,'values',len(values),'effects',len(effects))
        
        return values,effects
    
    def todamage(self,values,effects,line,line2):
        base=line[7].get()
        #base mod for all values
        modtobase=line2['cbdammod'].get()
        modaddbase=self.dxconvert(line2['cbdammod2'].get())
        multiply=1
        if modtobase!='0':
            #x2x3
            if (modtobase=='x2' or modtobase=='x3'):
                if modtobase=='x2':
                    multiply=2
                else:
                    multiply=3
                base=base
            else:
                base=modtobase
        #dam by effect
        total=0
        i=len(values)-1
        ##print(len(values))
        while i>=0:
            damtot=0
            modadd=modaddbase
            if effects[i]!=0:
                #print(effects[i])
                if effects[i]==1:
                    try:
                        damtot=max([int(base),int(line2['cbhit6dam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbhit6dam'].get()])
                    modadd+=self.dxconvert(line2['cbhit6dam2'].get())
                    if (line2['cbhit6dam'].get()=='x2' and multiply!=3):
                        multiply=2
                    elif line2['cbhit6dam'].get()=='x3':
                        multiply=3
                elif effects[i]==3:
                    try:
                        damtot=max([int(base),int(line2['cbwound6dam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbwound6dam'].get()])
                    modadd+=self.dxconvert(line2['cbwound6dam2'].get())
                    if (line2['cbwound6dam'].get()=='x2' and multiply!=3):
                        multiply=2
                    elif line2['cbwound6dam'].get()=='x3':
                        multiply=3
                elif effects[i]==5:
                    try:
                        damtot=max([int(base),int(line2['cbhit6pdam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbhit6pdam'].get()])
                    modadd+=self.dxconvert(line2['cbhit6pdam2'].get())
                    if (line2['cbhit6pdam'].get()=='x2' and multiply!=3):
                        multiply=2
                    elif line2['cbhit6pdam'].get()=='x3':
                        multiply=3
                elif effects[i]==11:
                    try:
                        damtot=max([int(base),int(line2['cbwound6pdam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbwound6pdam'].get()])
                    modadd+=self.dxconvert(line2['cbwound6pdam2'].get())
                    if (line2['cbwound6pdam'].get()=='x2' and multiply!=3):
                        multiply=2
                    elif line2['cbwound6pdam'].get()=='x3':
                        multiply=3
                elif effects[i]==4:
                    try:
                        damtot=max([int(base),int(line2['cbhit6dam'].get()),int(line2['cbwound6dam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbhit6dam'].get(),line2['cbwound6dam'].get()])
                    modadd+=(self.dxconvert(line2['cbhit6dam2'].get())+self.dxconvert(line2['cbwound6dam2'].get()))
                    if ((line2['cbhit6dam'].get()=='x2' or line2['cbwound6dam'].get()=='x2') and multiply!=3):
                        multiply=2
                    elif (line2['cbhit6dam'].get()=='x3' or line2['cbwound6dam'].get()=='x3'):
                        multiply=3
                elif effects[i]==9:
                    try:
                        damtot=max([int(base),int(line2['cbhit6dam'].get()),int(line2['cbwound6dam'].get()),int(line2['cbhit6pdam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbhit6dam'].get(),line2['cbwound6dam'].get(),line2['cbhit6pdam'].get()])
                    modadd+=(self.dxconvert(line2['cbhit6dam2'].get())+self.dxconvert(line2['cbwound6dam2'].get())+self.dxconvert(line2['cbhit6pdam2'].get()))
                    if ((line2['cbhit6dam'].get()=='x2' or line2['cbwound6dam'].get()=='x2' or line2['cbhit6pdam'].get()=='x2') and multiply!=3):
                        multiply=2
                    elif (line2['cbhit6dam'].get()=='x3' or line2['cbwound6dam'].get()=='x3' or line2['cbhit6pdam'].get()=='x3'):
                        multiply=3
                elif effects[i]==8:
                    try:
                        damtot=max([int(base),int(line2['cbwound6dam'].get()),int(line2['cbhit6pdam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbwound6dam'].get(),line2['cbhit6pdam'].get()])
                    modadd+=(self.dxconvert(line2['cbwound6dam2'].get())+self.dxconvert(line2['cbhit6pdam2'].get()))
                    if ((line2['cbwound6dam'].get()=='x2' or line2['cbhit6pdam'].get()=='x2') and multiply!=3):
                        multiply=2
                    elif (line2['cbwound6dam'].get()=='x3' or line2['cbhit6pdam'].get()=='x3'):
                        multiply=3
                elif effects[i]==6:
                    try:
                        damtot=max([int(base),int(line2['cbhit6dam'].get()),int(line2['cbhit6pdam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbhit6dam'].get(),line2['cbhit6pdam'].get()])
                    modadd+=(self.dxconvert(line2['cbhit6dam2'].get())+self.dxconvert(line2['cbhit6pdam2'].get()))
                    if ((line2['cbhit6dam'].get()=='x2' or line2['cbhit6pdam'].get()=='x2') and multiply!=3):
                        multiply=2
                    elif (line2['cbhit6dam'].get()=='x3' or line2['cbhit6pdam'].get()=='x3'):
                        multiply=3
                elif effects[i]==16:
                    try:
                        damtot=max([int(base),int(line2['cbhit6pdam'].get()),int(line2['cbwound6pdam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbhit6pdam'].get(),line2['cbwound6pdam'].get()])
                    modadd+=(self.dxconvert(line2['cbhit6pdam2'].get())+self.dxconvert(line2['cbwound6pdam2'].get()))
                    if ((line2['cbhit6pdam'].get()=='x2' or line2['cbwound6pdam'].get()=='x2') and multiply!=3):
                        multiply=2
                    elif (line2['cbhit6pdam'].get()=='x3' or line2['cbwound6pdam'].get()=='x3'):
                        multiply=3
                elif effects[i]==14:
                    try:
                        damtot=max([int(base),int(line2['cbwound6dam'].get()),int(line2['cbwound6pdam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbwound6dam'].get(),line2['cbwound6pdam'].get()])
                    modadd+=(self.dxconvert(line2['cbwound6dam2'].get())+self.dxconvert(line2['cbwound6pdam2'].get()))
                    if ((line2['cbwound6dam'].get()=='x2' or line2['cbwound6pdam'].get()=='x2') and multiply!=3):
                        multiply=2
                    elif (line2['cbwound6dam'].get()=='x3' or line2['cbwound6pdam'].get()=='x3'):
                        multiply=3
                elif effects[i]==12:
                    try:
                        damtot=max([int(base),int(line2['cbhit6dam'].get()),int(line2['cbwound6pdam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbhit6dam'].get(),line2['cbwound6pdam'].get()])
                    modadd+=(self.dxconvert(line2['cbhit6dam2'].get())+self.dxconvert(line2['cbwound6pdam2'].get()))
                    if ((line2['cbhit6dam'].get()=='x2' or line2['cbwound6pdam'].get()=='x2') and multiply!=3):
                        multiply=2
                    elif (line2['cbhit6dam'].get()=='x3' or line2['cbwound6pdam'].get()=='x3'):
                        multiply=3
                elif effects[i]==20:
                    try:
                        damtot=max([int(base),int(line2['cbhit6dam'].get()),int(line2['cbwound6dam'].get()),int(line2['cbhit6pdam'].get()),int(line2['cbwound6pdam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbhit6dam'].get(),line2['cbwound6dam'].get(),line2['cbhit6pdam'].get(),line2['cbwound6pdam'].get()])
                    modadd+=(self.dxconvert(line2['cbhit6dam2'].get())+self.dxconvert(line2['cbwound6dam2'].get())+self.dxconvert(line2['cbhit6pdam2'].get())+self.dxconvert(line2['cbwound6pdam2'].get()))
                    if ((line2['cbhit6dam'].get()=='x2' or line2['cbwound6dam'].get()=='x2' or line2['cbhit6pdam'].get()=='x2' or line2['cbwound6pdam'].get()=='x2') and multiply!=3):
                        multiply=2
                    elif (line2['cbhit6dam'].get()=='x3' or line2['cbwound6dam'].get()=='x3' or line2['cbhit6pdam'].get()=='x3' or line2['cbwound6pdam'].get()=='x3'):
                        multiply=3
                elif effects[i]==19:
                    try:
                        damtot=max([int(base),int(line2['cbwound6dam'].get()),int(line2['cbhit6pdam'].get()),int(line2['cbwound6pdam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbwound6dam'].get(),line2['cbhit6pdam'].get(),line2['cbwound6pdam'].get()])
                    modadd+=(self.dxconvert(line2['cbwound6dam2'].get())+self.dxconvert(line2['cbhit6pdam2'].get())+self.dxconvert(line2['cbwound6pdam2'].get()))
                    if ((line2['cbwound6dam'].get()=='x2' or line2['cbhit6pdam'].get()=='x2' or line2['cbwound6pdam'].get()=='x2') and multiply!=3):
                        multiply=2
                    elif (line2['cbwound6dam'].get()=='x3' or line2['cbhit6pdam'].get()=='x3' or line2['cbwound6pdam'].get()=='x3'):
                        multiply=3
                elif effects[i]==15:
                    try:
                        damtot=max([int(base),int(line2['cbhit6dam'].get()),int(line2['cbwound6dam'].get()),int(line2['cbwound6pdam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbhit6dam'].get(),line2['cbwound6dam'].get(),line2['cbwound6pdam'].get()])
                    modadd+=(self.dxconvert(line2['cbhit6dam2'].get())+self.dxconvert(line2['cbwound6dam2'].get())+self.dxconvert(line2['cbwound6pdam2'].get()))
                    if ((line2['cbhit6dam'].get()=='x2' or line2['cbwound6dam'].get()=='x2' or line2['cbwound6pdam'].get()=='x2') and multiply!=3):
                        multiply=2
                    elif (line2['cbhit6dam'].get()=='x3' or line2['cbwound6dam'].get()=='x3' or line2['cbwound6pdam'].get()=='x3'):
                        multiply=3
                elif effects[i]==17:
                    try:
                        damtot=max([int(base),int(line2['cbhit6dam'].get()),int(line2['cbhit6pdam'].get()),int(line2['cbwound6pdam'].get())])
                    except Exception:
                        damtot=self.compare([base,line2['cbhit6dam'].get(),line2['cbhit6pdam'].get(),line2['cbwound6pdam'].get()])
                    modadd+=(self.dxconvert(line2['cbhit6dam2'].get())+self.dxconvert(line2['cbhit6pdam2'].get())+self.dxconvert(line2['cbwound6pdam2'].get()))
                    if ((line2['cbhit6dam'].get()=='x2' or line2['cbhit6pdam'].get()=='x2' or line2['cbwound6pdam'].get()=='x2') and multiply!=3):
                        multiply=2
                    elif (line2['cbhit6dam'].get()=='x3' or line2['cbhit6pdam'].get()=='x3' or line2['cbwound6pdam'].get()=='x3'):
                        multiply=3
                else:
                    print('er sv effects')
            else:
                damtot=base
            damtot=self.dxconvert(damtot)
            #x2 and x3
            damtot*=multiply
            #mod
            damtot+=modadd
            total+=damtot
            i-=1
            
        ##print('damage',total)
        return total
    
    def compare(self,values):
        i=0
        values2=[]
        convert={'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'D3':2,'D6':3.5,'2D3':4,'2D6':7,'x2':0,'x3':0,'0':0}
        #rank=['x2','x3',1,2,'D3',3,'D6',4,'2D3',5,6,'2D6']
        while i<len(values):
            #print('v',values[i])
            values2.append(convert[values[i]])
            i+=1
        a=max(values2)
        b=values2.count(a)
        #multi values
        if (b!=1 and a==0):
            print('er damage=0')
            maxv=0
        elif (b!=1 and a==2):
            c=int(random()*2)
            if c==0:
                maxv=2
            elif c==1:
                maxv=self.dxconvert('D3')
            else:
                print('error compare')
        elif (b!=1 and a==4):
            c=int(random()*2)
            if c==0:
                maxv=4
            elif c==1:
                maxv=self.dxconvert('2D3')
            else:
                print('error compare')
        elif (b!=1 and a==7):
            c=int(random()*2)
            if c==0:
                maxv=7
            elif c==1:
                maxv=self.dxconvert('2D6')
            else:
                print('error compare')
        #non numerical
        else:
            if a==2:
                if 'D3' in values:
                    maxv=self.dxconvert('D3')
                else:
                    maxv=2
            elif a==4:
                if '2D3' in values:
                    maxv=self.dxconvert('2D3')
                else:
                    maxv=4
            elif a==7:
                if '2D6' in values:
                    maxv=self.dxconvert('2D6')
                else:
                    maxv=7
            elif a==3.5:
                if 'D6' in values:
                    maxv=self.dxconvert('D6')
                else:
                    print('er 3.5 no D6')
            else:
                #print('a,',a,type(a))
                maxv=self.dxconvert(a)
            #print(maxv)
            
        return maxv
            
    def reroll6s(self,values,rerolled,effects,effectsr):
        i=len(values)-1
        while i>-1:
            if values[i]==6:
                a=int(random()*6+1)
                rerolled.append(a)
                effectsr.append(effects[i])
                values.pop(i)
                effects.pop(i)
            i-=1
        return values,rerolled,effects,effectsr
    
    def reroll1s(self,values,rerolled,effects,effectsr):
        i=len(values)-1
        while i>-1:
            if values[i]==1:
                a=int(random()*6+1)
                rerolled.append(a)
                effectsr.append(effects[i])
                values.pop(i)
                effects.pop(i)
            i-=1
        return values,rerolled,effects,effectsr
    
    def rerollfail(self,values,rerolled,target,mod,effects,effectsr):
        i=len(values)-1
        if mod<0:
            mod=0
        while i>-1:
            if values[i]==6:
                pass
            elif (((values[i]+mod)<target) or (values[i]==1)):
                a=int(random()*6+1)
                rerolled.append(a)
                effectsr.append(effects[i])
                values.pop(i)
                effects.pop(i)
            i-=1
        return values,rerolled,effects,effectsr
    
    def ex6s1a(self,values,rerolled,line,line2,mod,hittarget,effects,effectsr,rtype,mw):
        if rtype=='hit':
            six=line2['hit6aop'].get()
            sixp=line2['hit6paop'].get()
            rr=[line2['hitrr1op'].get(),line2['hitrrop'].get(),line2['hitrr6op'].get()]
        elif rtype=='wound':
            six=line2['wound6aop'].get()
            sixp=line2['wound6paop'].get()
            rr=[line2['woundrr1op'].get(),line2['woundrrop'].get(),line2['woundrr6op'].get()]
        else:
            print('er extra atk')
        count=0
        for x in values:
            if (x==6 and six==1):
                count+=1
            if ((x+mod)>=6 and sixp==1):
                count+=1
        for y in rerolled:
            if (y==6 and six==1):
                count+=1
            if ((y+mod)>=6 and sixp==1):
                count+=1
        valuestemp=[0]*count
        rerolledtemp=[]
        effectstemp=[0]*count
        effectsrtemp=[]
        #wound extra hits- need hit roll
        if rtype=='wound':
            valuestemp,effectstemp,mw=self.tohit(line,line2,valuestemp,effectstemp,mw,[0,0,0,0,0,0],count)
        
        valuestemp=self.roll(valuestemp,len(valuestemp),[0,0,0,0,0,0])
#        i=0
#        while i<count:
#            a=int(random()*6+1)
#            valuestemp.append(a)
#            effectstemp.append(0)
#            i+=1
        #re-rolls: yours then oppoenents
        #re-roll 1s
        if rr[0]==1:
            valuestemp,rerolledtemp,effectstemp,effectsrtemp=self.reroll1s(valuestemp,rerolledtemp,effectstemp,effectsrtemp)
        #re-roll failed (before mod)
        if rr[1]==1:
            valuestemp,rerolledtemp,effectstemp,effectsrtemp=self.rerollfail(valuestemp,rerolledtemp,hittarget,mod,effectstemp,effectsrtemp)
        #re-roll 6s
        if rr[2]==1:
            valuestemp,rerolledtemp,effectstemp,effectsrtemp=self.reroll6s(valuestemp,rerolledtemp,effectstemp,effectsrtemp)
        
        for xx in valuestemp:
            values.append(xx)
            effects.append(0)
        for yy in rerolledtemp:
            values.append(yy)
            effects.append(0)
        return values,effects,mw
    
    def fail1s(self,values,effects):
        i=len(values)-1
        while i>=0:
            if values[i]==1:
                values.pop(i)
                effects.pop(i)
            i-=1
        return values,effects
    
    def mw6s(self,values,line2,mod,mw,rtype):
        if rtype=='hit':
            six=line2['cbhit6mw'].get()
            sixp=line2['cbhit6pmw'].get()
        elif rtype=='wound':
            six=line2['cbwound6mw'].get()
            sixp=line2['cbwound6pmw'].get()
        else:
            print('er mw 6s')
        tot=0
        totp=0
        if (six!='0' or sixp!='0'):
            i=len(values)-1
            while i>=0:
                if (values[i]==6 and six!='0'):
                    tot+=1
                if ((values[i]+mod)>=6 and sixp!='0'):
                    totp+=1
                if ((values[i]==6 and six!='0' and six.find('atk')!=-1) or ((values[i]+mod)>=6 and sixp!='0' and sixp.find('atk')!=-1)):
                    values.pop(i)
                i-=1
        j=0
        while j<tot:
            x=self.dxconvert(six)
            mw[0]+=1
            mw[1]+=x
            j+=1
        k=0
        while k<totp:
            x=self.dxconvert(sixp)
            mw[0]+=1
            mw[1]+=x
            k+=1
        return values,mw
        
    def dxconvert(self,x):
        if type(x)==type('str'):
            if x.find('atk')!=-1:
                x=x.replace(' atk end','')
        try:
            int(x)
        except Exception:
            if (x=='D3' or x=='D3 atk end'):
                x=int(random()*3+1)
            elif x=='-D3':
                x=-int(random()*3+1)
            elif (x=='D6' or x=='D6 atk end'):
                x=int(random()*6+1)
            elif x=='-D6':
                x=-int(random()*6+1)
            elif (x=='2D3' or x=='2D3 atk end'):
                x=int(random()*3+1)+int(random()*3+1)
            elif x=='-2D3':
                x=-(int(random()*3+1)+int(random()*3+1))
            elif (x=='2D6' or x=='2D6 atk end'):
                x=int(random()*6+1)+int(random()*6+1)
            elif x=='-2D6':
                x=-(int(random()*6+1)+int(random()*6+1))
            else:
                print('type not found')
        return int(x)
    
    def renddameffects(self,values,effects,mod,to):
        i=0
        while i<len(values):
            if values[i]==6:
                effects[i]+=to
#                if (effects[i]!=0 and effects[i]!=to):
#                    effects[i]==3
#                else:
#                    effects[i]=to
            if (values[i]+mod)>=6:
                effects[i]+=(to*3+2)
#                if (effects[i]!=0 and effects[i]!=to):
#                    effects[i]==3
#                else:
#                    effects[i]=to
            i+=1
        return effects
    
    def rollpass(self,values,effects,target,mod,rtype):
        valuespass=[]
        effectspass=[]
        if (rtype=='hit' or rtype=='wound'):
            ##print(len(values),len(effects))
            i=len(values)-1
            while i>=0:
                #6 auto pass
                if values[i]==6:
                    valuespass.append(values[i])
                    effectspass.append(effects[i])
                    values.pop(i)
                    effects.pop(i)
                elif (values[i]+mod)>=target:
                    valuespass.append(values[i])
                    effectspass.append(effects[i])
                    values.pop(i)
                    effects.pop(i)
                i-=1
        elif rtype=='save':
            mod2=mod
            mod=target
            ##print(mod,mod2)
            savetarget=[2,3,4,5,6,7]
            i=len(values)-1
            ##print(len(values))
            while i>=0:
                a=self.sv
                #a=2
                target=savetarget[a]
                #print(target)
                if effects[i]!=0:
                    #print(effects[i])
                    if effects[i]==1:
                        modtot=mod+min([mod2[0],mod2[4],mod2[5]])
                    elif effects[i]==3:
                        modtot=mod+min([mod2[2],mod2[4],mod2[5]])
                    elif effects[i]==5:
                        modtot=mod+min([mod2[1],mod2[4],mod2[5]])
                    elif effects[i]==11:
                        modtot=mod+min([mod2[3],mod2[4],mod2[5]])
                    elif effects[i]==4:
                        modtot=mod+min([mod2[0],mod2[2],mod2[4],mod2[5]])
                    elif effects[i]==9:
                        modtot=mod+min([mod2[0],mod2[1],mod2[2],mod2[4],mod2[5]])
                    elif effects[i]==8:
                        modtot=mod+min([mod2[1],mod2[2],mod2[4],mod2[5]])
                    elif effects[i]==6:
                        modtot=mod+min([mod2[0],mod2[1],mod2[4],mod2[5]])
                    elif effects[i]==16:
                        modtot=mod+min([mod2[1],mod2[3],mod2[4],mod2[5]])
                    elif effects[i]==14:
                        modtot=mod+min([mod2[2],mod2[3],mod2[4],mod2[5]])
                    elif effects[i]==12:
                        modtot=mod+min([mod2[0],mod2[3],mod2[4],mod2[5]])
                    elif effects[i]==20:
                        modtot=mod+min([mod2[0],mod2[1],mod2[2],mod2[3],mod2[4],mod2[5]])
                    elif effects[i]==19:
                        modtot=mod+min([mod2[1],mod2[2],mod2[3],mod2[4],mod2[5]])
                    elif effects[i]==15:
                        modtot=mod+min([mod2[0],mod2[2],mod2[3],mod2[4],mod2[5]])
                    elif effects[i]==17:
                        modtot=mod+min([mod2[0],mod2[1],mod2[3],mod2[4],mod2[5]])
                    else:
                        print('er sv effects')
                else:
                    modtot=min(mod2[4],mod2[5])+mod
                ##print(modtot)
                if values[i]!=1:
                    if (values[i]+modtot)>=target:
                        values.pop(i)
                        effects.pop(i)
                i-=1
            ##print(len(values))
            valuespass=values
            effectspass=effects
        else:
            print('er rollpass')
        return valuespass,effectspass
        
    def multi6s(self,values,effects,line2,rtype):
        addvalues=[]
        addeffects=[]
        if rtype=='hit':
#            a=int(line2['hit62op'].get())
#            b=int(line2['hit63op'].get())
#            c=int(line2['hit6p2op'].get())
#            d=int(line2['hit6p3op'].get())
#            e=int(line2['hitd3op'].get())
#            f=int(line2['hitd6op'].get())
            a=line2['cbhit6op'].get()
            b=line2['cbhit6pop'].get()
            c=line2['cbhitxop'].get()
            mod=int(line2['cbhitmod'].get())
        elif rtype=='wound':
#            a=int(line2['wound62op'].get())
#            b=int(line2['wound63op'].get())
#            c=int(line2['wound6p2op'].get())
#            d=int(line2['wound6p3op'].get())
#            e=int(line2['woundd3op'].get())
#            f=int(line2['woundd6op'].get())
            a=line2['cbwound6op'].get()
            b=line2['cbwound6pop'].get()
            c=line2['cbwoundxop'].get()
            mod=int(line2['cbwoundmod'].get())
        else:
            print('er multi 6s')
        
        i=0
        while i<len(values):
            if (a!='0' and values[i]==6):
                j=self.dxconvert(a)
                while j>1:
                    addvalues.append(values[i])
                    addeffects.append(effects[i])
                    j=-1
            if (b!='0' and (values[i]+mod)>=6):
                j=self.dxconvert(b)
                while j>1:
                    addvalues.append(values[i])
                    addeffects.append(effects[i])
                    j=-1
            if (c!='0'): #and (values[i]+mod)>=target, hit/wound should all be passes
                j=self.dxconvert(c)
                #print(j)
                while j>1:
                    #print('run')
                    addvalues.append(values[i])
                    addeffects.append(effects[i])
                    j-=1
                    
#            if (a==1 and values[i]==6):
#                addvalues.append(values[i])
#                addeffects.append(effects[i])
#            if (b==1 and values[i]==6):
#                addvalues.append(values[i])
#                addeffects.append(effects[i])
#                addvalues.append(values[i])
#                addeffects.append(effects[i])
#            if (c==1 and (values[i]+mod)>=6):
#                addvalues.append(values[i])
#                addeffects.append(effects[i])
#            if (d==1 and (values[i]+mod)>=6):
#                addvalues.append(values[i])
#                addeffects.append(effects[i])
#                addvalues.append(values[i])
#                addeffects.append(effects[i])
#            if (e==1 and (values[i]+mod)>=target):
#                j=int(random()*3+1)
#                while j>=0:
#                    addvalues.append(values[i])
#                    addeffects.append(effects[i])
#                    j=-1
#            if (f==1 and (values[i]+mod)>=target):
#                j=int(random()*6+1)
#                while j>=0:
#                    addvalues.append(values[i])
#                    addeffects.append(effects[i])
#                    j=-1
            i+=1
        #print(addvalues)
        for x in addvalues:
            values.append(x)
        for y in addeffects:
            effects.append(y)
        return values,effects
    
    def commands(self):
        self.btnAdd.configure(command=lambda:self.addLine())
        self.btnDel.configure(command=lambda:self.removeLine(),state=DISABLED)
        self.btnCal.configure(command=lambda:self.calculate())
        
#graph
class Graph:
    means=[]
    stds=[]
    meanset=[]
    stdset=[]
    meansmw=[]
    stdsmw=[]
    meansetmw=[]
    stdsetmw=[]
    meanstot=[]
    stdtot=[]
    meansmwtot=[]
    stdmwtot=[]
    
    values2=[]
    values3=[]
    values4=[]
    values5=[]
    values6=[]
    values7=[]
    mw2=[]
    mw3=[]
    mw4=[]
    mw5=[]
    mw6=[]
    mw7=[]
    values=[]
    mws=[]
        
    def plotdata(self,data1,data2):
        maxv1=max(data1)
        maxv2=max(data2)
        values2=[]
        values3=[]
        values4=[]
        values5=[]
        values6=[]
        values7=[]
        mw2=[]
        mw3=[]
        mw4=[]
        mw5=[]
        mw6=[]
        mw7=[]
        i=0
        while i<len(data1):
            if i%6==0:
                values2.append(data1[i])
                mw2.append(data2[i])
            elif i%6==1:
                values3.append(data1[i])
                mw3.append(data2[i])
            elif i%6==2:
                values4.append(data1[i])
                mw4.append(data2[i])
            elif i%6==3:
                values5.append(data1[i])
                mw5.append(data2[i])
            elif i%6==4:
                values6.append(data1[i])
                mw6.append(data2[i])
            elif i%6==5:
                values7.append(data1[i])
                mw7.append(data2[i])
            i+=1
        values=[values2,values3,values4,values5,values6,values7]
        mw=[mw2,mw3,mw4,mw5,mw6,mw7]
        Graph.values.append(data1)
        Graph.values2.append(values2)
        Graph.values3.append(values3)
        Graph.values4.append(values4)
        Graph.values5.append(values5)
        Graph.values6.append(values6)
        Graph.values7.append(values7)
        Graph.mws.append(data2)
        Graph.mw2.append(mw2)
        Graph.mw3.append(mw3)
        Graph.mw4.append(mw4)
        Graph.mw5.append(mw5)
        Graph.mw6.append(mw6)
        Graph.mw7.append(mw7)
        
        x=[[],[],[],[],[],[]]
        y=[[],[],[],[],[],[]]
        xmw=[[],[],[],[],[],[]]
        ymw=[[],[],[],[],[],[]]
        hold=np.linspace(0,maxv1,int(100*maxv1+1))
        holdmw=np.linspace(0,maxv1,int(100*maxv2+1))
        x1=[hold,hold,hold,hold,hold,hold]#[np.linspace(0,int(maxv1,int(100*maxv1+1))]]#,[np.linspace(0,maxv1,int(100*maxv1+1))],[np.linspace(0,maxv1,int(100*maxv1+1))],[np.linspace(0,maxv1,int(100*maxv1+1))],[np.linspace(0,maxv1,int(100*maxv1+1))]]
        #print(hold)
        x1mw=[holdmw,holdmw,holdmw,holdmw,holdmw,holdmw]
        y1=[[],[],[],[],[],[]]
        y1mw=[[],[],[],[],[],[]]
        j=0
        while j<6:
            k=0
            while k<=maxv1:
                x[j].append(k)
                y[j].append(values[j].count(float(k)))
                k+=1
            kk=0
            while kk<=maxv2:
                xmw[j].append(kk)
                ymw[j].append(mw[j].count(float(kk)))
                kk+=1
            j+=1
        #mean and std
        allmeans=[]
        allstds=[]
        n=0
        while n<6:
            #print(values[n])
            mu=np.mean(values[n])
            nu=np.std(values[n])
            Graph.means.append(mu)
            Graph.stds.append(nu)
            Graph.meanset.append(mu)
            Graph.stdset.append(nu)
            print(n+2,'mean',mu,'standard deviation',nu)
            mumw=np.mean(mw[n])
            numw=np.std(mw[n])
            print(n+2,'mean',mumw,'standard deviation',numw)
            Graph.meansmw.append(mumw)
            Graph.stdsmw.append(numw)
            Graph.meansetmw.append(mumw)
            Graph.stdsetmw.append(numw)
            allmeans.append(mu)
            allstds.append(nu)
            allmeans.append(mumw)
            allstds.append(numw)
            m=0
            if maxv1!=0:
                while m<len(x1[n]):
                    yv=((len(values[n]))/np.sqrt(2*np.pi*nu*nu))*np.exp(-((x1[n][m]-mu)**2)/(2*nu*nu))
                    y1[n].append(yv)
                    m+=1
            else:
                y1[n].append(0)
            mm=0
            if maxv2!=0:
                while mm<len(x1mw[n]):
                    yv=((len(mw[n]))/np.sqrt(2*np.pi*numw*numw))*np.exp(-((x1mw[n][mm]-mumw)**2)/(2*numw*numw))
                    y1mw[n].append(yv)
                    mm+=1
            else:
                y1mw[n].append(0)
            n+=1
        #print(len(x1[0]))
        
        #plot
        fig=plt.figure()
        fig.set_size_inches(8,6,forward=True)
        plt.plot(x[0],y[0],marker='x',color='r')
        print(x[5],y[5])
        plt.plot(x[1],y[1],marker='x',color='g')
        plt.plot(x[2],y[2],marker='x',color='b')
        plt.plot(x[3],y[3],marker='x',color='m')
        plt.plot(x[4],y[4],marker='x',color='y')
        plt.plot(x[5],y[5],marker='x',color='c')
        plt.grid('on')
        plt.legend(['2+','3+','4+','5+','6+','7+'])
        #line plots
        #print(y1[0])
        plt.plot(x1[0],y1[0],linestyle='--',color='r')
        plt.plot(x1[1],y1[1],linestyle='--',color='g')
        plt.plot(x1[2],y1[2],linestyle='--',color='b')
        plt.plot(x1[3],y1[3],linestyle='--',color='m')
        plt.plot(x1[4],y1[4],linestyle='--',color='y')
        plt.plot(x1[5],y1[5],linestyle='--',color='c')
        #print(max(y1[0]))
        plt.show()
        
#        fig2=plt.figure()
#        fig2.set_size_inches(12,10,forward=True)
#        plt.plot(xmw[0],ymw[0],marker='x',color='r')
#        print(xmw[5],ymw[5])
#        plt.plot(xmw[1],ymw[1],marker='x',color='g')
#        plt.plot(xmw[2],ymw[2],marker='x',color='b')
#        plt.plot(xmw[3],ymw[3],marker='x',color='m')
#        plt.plot(xmw[4],ymw[4],marker='x',color='y')
#        plt.plot(xmw[5],ymw[5],marker='x',color='c')
#        plt.grid('on')
#        plt.legend(['2+','3+','4+','5+','6+','7+'])
#        #line plots
#        plt.plot(x1mw[0],y1mw[0],linestyle='--',color='r')
#        plt.plot(x1mw[1],y1mw[1],linestyle='--',color='g')
#        plt.plot(x1mw[2],y1mw[2],linestyle='--',color='b')
#        plt.plot(x1mw[3],y1mw[3],linestyle='--',color='m')
#        plt.plot(x1mw[4],y1mw[4],linestyle='--',color='y')
#        plt.plot(x1mw[5],y1mw[5],linestyle='--',color='c')
#        plt.show()
        
        ####
        
        totmean,totstd=self.plotmerge(maxv1,maxv2,data1,data2)
        return allmeans,allstds,totmean,totstd
        
    def plotmerge(self,maxv1,maxv2,data1,data2):
        #data mean, std
        mud=np.mean(data1)
        nud=np.std(data1)
        mumwd=np.mean(data2)
        numwd=np.std(data2)
        numean=np.std(Graph.means)
        numeanmw=np.std(Graph.meansmw)
        print('data:','mean',mud,'standard deviation',nud)
        print('data:','mean',mumwd,'standard deviation',numwd)
        print('std of means',numean,numeanmw)
        totmean=[mud,mumwd]
        totstd=[nud,numwd]
        #calculated mean, std
        i=0
        mu=nu=nu2=0
        mumw=numw=numw2=0
        #nu2=numw2=0
        while i<len(Graph.means):
            mu+=Graph.means[i]
            nu2+=(Graph.stds[i]**2)
            nu+=Graph.stds[i]
            mumw+=Graph.meansmw[i]
            numw2+=(Graph.stdsmw[i]**2)
            numw+=Graph.stdsmw[i]
            #print(nu,nu2)
            i+=1
        mu=mu/len(Graph.means)
        nu3=np.sqrt(nu)/len(Graph.means)
        nu2=np.sqrt(nu/len(Graph.means))
        nu=nu/len(Graph.means)
        print(nu,nu2,nu3)
        mumw=mumw/len(Graph.meansmw)
        numw2=np.sqrt(numw/len(Graph.meansmw))
        numw=numw/len(Graph.meansmw)
        Graph.meanstot.append(mud)
        Graph.stdtot.append(nud)
        Graph.meansmwtot.append(mumwd)
        Graph.stdmwtot.append(numwd)
        #data count occurances
        hold=np.linspace(0,maxv1,int(100*maxv1+1))
        holdmw=np.linspace(0,maxv2,int(100*maxv2+1))
        x=hold
        xmw=holdmw
        x1=[]
        y1=[]
        x1mw=[]
        y1mw=[]
        k=0
        while k<=maxv1:
            x1.append(k)
            y1.append(data1.count(float(k)))
            #print(y1[k])
            k+=1
        kk=0
        while kk<=maxv2:
            x1mw.append(kk)
            y1mw.append(data2.count(float(kk)))
            kk+=1
        #calculated frind y
        y=[]
        ymw=[]
        yd=[]
        ymwd=[]
        j=0
        if maxv1!=0:
            while j<len(x):
                yv=(len(data1)/np.sqrt(2*np.pi*nu*nu))*np.exp(-((x[j]-mu)**2)/(2*nu*nu))
                y.append(yv)
                yvd=(len(data1)/np.sqrt(2*np.pi*nud*nud))*np.exp(-((x[j]-mud)**2)/(2*nud*nud))
                yd.append(yvd)
                j+=1
        else:
            y.append(0)
            yd.append(0)
        jj=0
        if maxv2!=0:
            while jj<len(xmw):
                yv=(len(data2)/np.sqrt(2*np.pi*numw*numw))*np.exp(-((xmw[jj]-mumw)**2)/(2*numw*numw))
                ymw.append(yv)
                yvd=(len(data2)/np.sqrt(2*np.pi*numwd*numwd))*np.exp(-((xmw[jj]-mumwd)**2)/(2*numwd*numwd))
                ymwd.append(yvd)
                jj+=1
        else:
            ymw.append(0)
            ymwd.append(0)
        #plot
        fig=plt.figure()
        fig.set_size_inches(8,6,forward=True)
        plt.plot(x1,y1,marker='x',color='r')
        plt.plot(x,yd,linestyle='--',color='r')
        plt.plot(x,y,linestyle='--',color='g')
        plt.grid('on')
        plt.show()
        print('mean',mud,'standard deviation',nud)
        print('mean',mu,'standard deviation',nu,nu2)
        Graph.means=[]
        Graph.stds=[]
        fig2=plt.figure()
        fig2.set_size_inches(8,6,forward=True)
        plt.plot(x1mw,y1mw,marker='x',color='r')
        plt.plot(xmw,ymwd,linestyle='--',color='r')
        plt.plot(xmw,ymw,linestyle='--',color='g')
        plt.grid('on')
        plt.show()
        print('mean',mumwd,'standard deviation',numwd)
        print('mean',mumw,'standard deviation',numw,numw2)
        #clear at end
        Graph.meansmw=[]
        Graph.stdsmw=[]
        print(len(Graph.values2[0]),len(Graph.values[0]))
        return totmean,totstd
        
    def plottotal(self):
        #accumulate data sets
        p=0
        q=0
        valuestot=[]
        mwtot=[]
        values2=[]
        values3=[]
        values4=[]
        values5=[]
        values6=[]
        values7=[]
        mw2=[]
        mw3=[]
        mw4=[]
        mw5=[]
        mw6=[]
        mw7=[]
        values=[values2,values3,values4,values5,values6,values7]
        mw=[mw2,mw3,mw4,mw5,mw6,mw7]
        print(len(Graph.values2[0]),len(Graph.values2))
        while p<len(Graph.values2[0]):
            q=0
            r2=r3=r4=r5=r6=r7=0
            s2=s3=s4=s5=s6=s7=0
            while q<len(Graph.values2):
                #r+=Graph.valuestot[q][p]
                #s+=Graph.mwtit[q][p]
                r2+=Graph.values2[q][p]
                s2+=Graph.mw2[q][p]
                r3+=Graph.values3[q][p]
                s3+=Graph.mw3[q][p]
                r4+=Graph.values4[q][p]
                s4+=Graph.mw4[q][p]
                r5+=Graph.values5[q][p]
                s5+=Graph.mw5[q][p]
                r6+=Graph.values6[q][p]
                s6+=Graph.mw6[q][p]
                r7+=Graph.values7[q][p]
                s7+=Graph.mw7[q][p]
                q+=1
            valuestot.append(r2)
            mwtot.append(s2)
            valuestot.append(r3)
            mwtot.append(s3)
            valuestot.append(r4)
            mwtot.append(s4)
            valuestot.append(r5)
            mwtot.append(s5)
            valuestot.append(r6)
            mwtot.append(s6)
            valuestot.append(r7)
            mwtot.append(s7)
            values2.append(r2)
            mw2.append(s2)
            values3.append(r3)
            mw3.append(s3)
            values4.append(r4)
            mw4.append(s4)
            values5.append(r5)
            mw5.append(s5)
            values6.append(r6)
            mw6.append(s6)
            values7.append(r7)
            mw7.append(s7)
            p+=1
        maxv1=max(valuestot)
        maxv2=max(mwtot)
        
        x=[[],[],[],[],[],[]]
        y=[[],[],[],[],[],[]]
        xmw=[[],[],[],[],[],[]]
        ymw=[[],[],[],[],[],[]]
        hold=np.linspace(0,maxv1,int(100*maxv1+1))
        holdmw=np.linspace(0,maxv1,int(100*maxv2+1))
        x1=[hold,hold,hold,hold,hold,hold]
        #print(hold)
        x1mw=[holdmw,holdmw,holdmw,holdmw,holdmw,holdmw]
        y1=[[],[],[],[],[],[]]
        y1mw=[[],[],[],[],[],[]]
        j=0
        while j<6:
            k=0
            while k<=maxv1:
                x[j].append(k)
                y[j].append(values[j].count(float(k)))
                k+=1
            kk=0
            while kk<=maxv2:
                xmw[j].append(kk)
                ymw[j].append(mw[j].count(float(kk)))
                kk+=1
            j+=1
        #data mean, std
        means=[]
        stds=[]
        meansmw=[]
        stdsmw=[]
        summeans=[]
        sumstds=[]
        n=0
        while n<6:
            mu=np.mean(values[n])
            nu=np.std(values[n])
            means.append(mu)
            stds.append(nu)
            #Graph.meanset.append(mu)
            #Graph.stdset.append(nu)
            print(n+2,'mean',mu,'standard deviation',nu)
            mumw=np.mean(mw[n])
            numw=np.std(mw[n])
            print(n+2,'mean',mumw,'standard deviation',numw)
            meansmw.append(mumw)
            stdsmw.append(numw)
            #Graph.meansetmw.append(mumw)
            #Graph.stdsetmw.append(numw)
            summeans.append(mu)
            sumstds.append(nu)
            summeans.append(mumw)
            sumstds.append(numw)
            m=0
            if maxv1!=0:
                while m<len(x1[n]):
                    yv=((len(values[n]))/np.sqrt(2*np.pi*nu*nu))*np.exp(-((x1[n][m]-mu)**2)/(2*nu*nu))
                    y1[n].append(yv)
                    m+=1
            else:
                y1[n].append(0)
            mm=0
            if maxv2!=0:
                while mm<len(x1mw[n]):
                    yv=((len(mw[n]))/np.sqrt(2*np.pi*numw*numw))*np.exp(-((x1mw[n][mm]-mumw)**2)/(2*numw*numw))
                    y1mw[n].append(yv)
                    mm+=1
            else:
                y1mw[n].append(0)
            n+=1
        #plot
        fig=plt.figure()
        fig.set_size_inches(8,6,forward=True)
        plt.plot(x[0],y[0],marker='x',color='r')
        print(x[5],y[5])
        plt.plot(x[1],y[1],marker='x',color='g')
        plt.plot(x[2],y[2],marker='x',color='b')
        plt.plot(x[3],y[3],marker='x',color='m')
        plt.plot(x[4],y[4],marker='x',color='y')
        plt.plot(x[5],y[5],marker='x',color='c')
        plt.grid('on')
        plt.legend(['2+','3+','4+','5+','6+','7+'])
        #line plots
        #print(y1[0])
        plt.plot(x1[0],y1[0],linestyle='--',color='r')
        plt.plot(x1[1],y1[1],linestyle='--',color='g')
        plt.plot(x1[2],y1[2],linestyle='--',color='b')
        plt.plot(x1[3],y1[3],linestyle='--',color='m')
        plt.plot(x1[4],y1[4],linestyle='--',color='y')
        plt.plot(x1[5],y1[5],linestyle='--',color='c')
        #print(max(y1[0]))
        plt.show()
        
        mud=np.mean(valuestot)
        nud=np.std(valuestot)
        mumwd=np.mean(mwtot)
        numwd=np.std(mwtot)
        numean=np.std(Graph.meanset)
        numeanmw=np.std(Graph.meansetmw)
        print('data:','mean',mud,'standard deviation',nud)
        print('data:','mean',mumwd,'standard deviation',numwd)
        print('std of means',numean,numeanmw)
        sumtotmean=[mud,mumwd]
        sumtotstd=[nud,numwd]
        #calculated mean, std
        #print('g',Graph.meanset)
        i=0
        mu=nu=nu2=0
        mumw=numw=numw2=0
        #nu2=numw2=0
        while i<len(Graph.meanstot):
            mu+=Graph.meanstot[i]
            nu2+=(Graph.stdtot[i]**2)
            nu+=Graph.stdtot[i]
            mumw+=Graph.meansmwtot[i]
            numw2+=(Graph.stdmwtot[i]**2)
            numw+=Graph.stdmwtot[i]
            #print(nu,nu2)
            i+=1
        #mu=mu/len(Graph.means)
        #nu3=np.sqrt(nu)/len(Graph.means)
        #nu2=np.sqrt(nu/len(Graph.means))
        #nu=nu/len(Graph.means)
        nu=np.sqrt(nu2)
        #print(nu,nu2,nu3)
        #mumw=mumw/len(Graph.meansmw)
        #numw2=np.sqrt(numw/len(Graph.meansmw))
        #numw=numw/len(Graph.meansmw)
        numw=np.sqrt(numw2)
        #data count occurances
        #hold=np.linspace(0,maxv1,int(100*maxv1+1))
        #holdmw=np.linspace(0,maxv2,int(100*maxv2+1))
        xtot=hold
        xmwtot=holdmw
        x1tot=[]
        y1tot=[]
        x1mwtot=[]
        y1mwtot=[]
        k=0
        while k<=maxv1:
            x1tot.append(k)
            y1tot.append(valuestot.count(float(k)))
            k+=1
        kk=0
        while kk<=maxv2:
            x1mwtot.append(kk)
            y1mwtot.append(mwtot.count(float(kk)))
            kk+=1
        #calculated find y
        ytot=[]
        ymwtot=[]
        yd=[]
        ymwd=[]
        j=0
        if maxv1!=0:
            while j<len(xtot):
                yv=(len(valuestot)/np.sqrt(2*np.pi*nu*nu))*np.exp(-((xtot[j]-mu)**2)/(2*nu*nu))
                ytot.append(yv)
                yvd=(len(valuestot)/np.sqrt(2*np.pi*nud*nud))*np.exp(-((xtot[j]-mud)**2)/(2*nud*nud))
                yd.append(yvd)
                j+=1
        else:
            ytot.append(0)
            yd.append(0)
        jj=0
        if maxv2!=0:
            while jj<len(xmwtot):
                yv=(len(mwtot)/np.sqrt(2*np.pi*numw*numw))*np.exp(-((xmwtot[jj]-mumw)**2)/(2*numw*numw))
                ymwtot.append(yv)
                yvd=(len(mwtot)/np.sqrt(2*np.pi*numwd*numwd))*np.exp(-((xmwtot[jj]-mumwd)**2)/(2*numwd*numwd))
                ymwd.append(yvd)
                jj+=1
        else:
            ymwtot.append(0)
            ymwd.append(0)
            
            
        #plot
        fig=plt.figure()
        fig.set_size_inches(8,6,forward=True)
        plt.plot(x1tot,y1tot,marker='x',color='r')
        plt.plot(xtot,yd,linestyle='--',color='r')
        plt.plot(xtot,ytot,linestyle='--',color='g')
        plt.grid('on')
        plt.show()
        print('mean',mud,'standard deviation',nud)
        print('mean',mu,'standard deviation',nu,nu2)
        Graph.means=[]
        Graph.stds=[]
        fig2=plt.figure()
        fig2.set_size_inches(8,6,forward=True)
        plt.plot(x1mwtot,y1mwtot,marker='x',color='r')
        plt.plot(xmwtot,ymwd,linestyle='--',color='r')
        plt.plot(xmwtot,ymwtot,linestyle='--',color='g')
        plt.grid('on')
        plt.show()
        print('mean',mumwd,'standard deviation',numwd)
        print('mean',mumw,'standard deviation',numw,numw2)
        #clear at end
        Graph.meansmw=[]
        Graph.stdsmw=[]
        
        Graph.values=[]
        Graph.values2=[]
        Graph.values3=[]
        Graph.values4=[]
        Graph.values5=[]
        Graph.values6=[]
        Graph.values7=[]
        Graph.mws=[]
        Graph.mw2=[]
        Graph.mw3=[]
        Graph.mw4=[]
        Graph.mw5=[]
        Graph.mw6=[]
        Graph.mw7=[]
        
        Graph.meanset=[]
        Graph.stdset=[]
        Graph.meansetmw=[]
        Graph.stdsetmw=[]
        Graph.meanstot=[]
        Graph.stdtot=[]
        Graph.meansmwtot=[]
        Graph.stdmwtot=[]
        
        return summeans,sumstds,sumtotmean,sumtotstd
    
    
#programe
win=Tk()
ops=Mode()
gui=Gui1(win,ops)
win.mainloop()

win2=Tk()
if ops.mode==1:
    gui2=Gui2(win2)
elif ops.mode==2:
    gui2=Gui2(win2)
    gui3=Gui2(win2)
    gui3.title.destroy()
    gui2.title.configure(text='Compare unit ability')
else:
    print('error options')
    win2.destroy()
        
win2.mainloop()