# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 09:49:24 2021

@author: tevsl
"""

from tkinter import *
from tkinter import ttk

import numpy as np
import time

def circlist(thelist,theitem,maxlength):
    #adds theitem to the bottom of thelist and pops the top if maxlength exceeded
    thelist.append(theitem)
    if len(thelist)> maxlength:
        thelist.pop(0)
        
def goodresult(curtask,index,ms):
    curtask["lastgood"]=time.time()
    curtask['conseq']+=1
    curtask['results'].append({"time":curtask['lastgood'],"index":index,"ms":ms}) #put it on the list
    circlist(curtask["results"],{"time":curtask['lastgood'],"index":index,"ms":ms},curtask['resultlim'])

    
    
    
def do_ping(curtask,index):
    import subprocess
    
    pingmin=4
    jittermin=10
    
    
    glop=subprocess.run("ping "+curtask['script'][index]+' -n 1 -w '+str(curtask['timeout']),capture_output=True)
    if glop.returncode==0:  #if it succeeded
        lines=glop.stdout.decode().splitlines()
        thetime=''
        for line in lines:
            ix=line.find('time')
            if ix>=0:   #if this line has time
                pline=line[ix+5:] #get the line starting at number
                ix=pline.find('ms')
                if ix>0:    #if end found
                    thetime=pline[:ix]
        assert len(thetime)>0, 'cant find time'
        ms=int(thetime)
        goodresult(curtask,index,ms)
        if len(curtask['results'])>=pingmin: #if have enough samples
            relresults=curtask["results"][-pingmin:]
            curtask["display"].set("{:4.1f}".format(np.mean([res['ms'] for res in relresults])))
            
        # now work on jitter
           
            circlist(pingqs[index],ms,jittermin+1) #put the time at the bottom of the q
            if len(pingqs[index])>1: # if there's anything else on the list
                pingqs[index][-2]=abs(pingqs[index][-2]-pingqs[index][-1]) #turn it into jitter
                jit=np.mean([np.median(q) for q in pingqs[:-1] if len(q)==jittermin+1])
                if not np.isnan(jit): #if enough to calculate
                    jitter.set("{:4.1f}".format(jit))

                    
        
    print("results",glop) #debugging
    


def maketaskarray(tasklist):  #formats script of tasks to run and results array for output
    script=[]
    for task in tasklist: #make the script
        for i in range(task[1]): #for weighting
            script.append(task[0])
    return script  
       

def checkstatus():
    global doafter

    if killsw:  #if we're done
        return #return without rescheduling
    if not pausesw: # if not paused
        for task in thequeue: #loop thru the queue
            if task["last"]+task['interval']<=time.time(): #if due to run
                curtask=featuredict[task["name"]] #get full feature record
                curtask["task"](curtask,task["index"]) #call the task
                task["last"]=time.time() #remember when
                task["index"]=(task["index"]+1)%len(curtask["script"]) #update index
                thequeue.append(thequeue.pop(0)) #move to back of queue
                break
    doafter=root.after(100,checkstatus) #set next iteration
    
#button processor
            
def killall(): #action for quit button
    global killsw
    
    killsw=True #in case lingering calls
    print("shutting down....")
    if doafter is not None:
        root.after_cancel(doafter)
    root.destroy()

def pausetoggle():  #action for pause button
    global pausesw
    
    if pausesw: #if already paused
        pausesw=False #resume
        pausebutton.configure(text="Pause")
    else: #if not paused
        pausesw=True
        pausebutton.configure(text="Resume")


# initialization

pingtasks=[('8.8.8.8',1),('1.1.1.1',1),('208.67.222.222',1)] #locations to ping and weighting
pingqs=[[] for i in range(len(pingtasks))]


pingdict={"task":do_ping,"interval":1,"timeout":300,"label":"latency in ms","results":[],"conseq":0,"resultlim":12}  # will come from preferences
pingdict["script"]=maketaskarray(pingtasks) #add scripts and output array
featuredict={'ping':pingdict}    #will add at least speedtest and monitor

thequeue=[] #revolving q of tasks to schedule
for feature, dictionary in featuredict.items():    #create a queue and thread for each feature
    thequeue.append({"name":feature,"interval":dictionary["interval"],"last":0,"index":0})
        
buttonignore=True #because buttons call their code during setup

doafter=None #pending doafter
killsw=False
pausesw=False



root = Tk()
root.title='Zoombuddy'
frm = ttk.Frame(root, padding=10)
frm.grid()
row=1
for feature,value in featuredict.items(): #add an output line for each row
    ttk.Label(frm,text=value["label"]+':').grid(column=0,row=row)
    value["display"]=StringVar()
    value["display"].set("N/A")
    display=ttk.Label(frm,textvariable=value["display"])
    value["widget"]=display    
    display.grid(column=1,row=row)
    row+=1
ttk.Label(frm,text="jitter in ms:").grid(column=0, row=row)
jitter=StringVar()
jitter.set('N/A')
ttk.Label(frm,textvariable=jitter).grid(column=1, row=row)
row+=1
pausebutton=ttk.Button(frm,text="Pause",command=pausetoggle)
pausebutton.grid(column=0,row=row+1)
ttk.Button(frm, text="Quit", command=killall).grid(column=1, row=row+1)
doafter=root.after(100,checkstatus) #set next iteration
buttonignore=False #now buttons are good to go
root.mainloop()
print('goodby')