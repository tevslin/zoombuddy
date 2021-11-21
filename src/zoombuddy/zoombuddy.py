# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 09:49:24 2021

@author: tevsl
"""

import tkinter as tk
from tkinter import ttk

import numpy as np
import time
import warnings
warnings.filterwarnings("ignore")

import ping3
ping3.EXCEPTIONS = True

######## Note ping3 does not work in user mode in rasperian
    
for dns in ['8.8.8.8','1.1.1.1','208.67.222.222']:
    msg=''
    try:
        resp=ping3.ping(dns,unit='ms',timeout=.3)
        msg=str(round(resp))
    except ping3.errors.HostUnknown:
        msg='host unknown'
    except ping3.errors.Timeout:        
        msg='timeout'
    except ping3.errors.PingError:
        msg='unknown error'

class avgobj:
    def __init__(self):
        self.count=0
        self.total=0
    def updateavg(self,newvalue):
        self.count+=1
        self.total+=newvalue
        return "{:5.2f}".format(self.total/self.count)
        

class mainwindow:
    def __init__(self,callafter,aftertime,title='Zoombuddy'):
       
        self.root = tk.Tk()
        self.root.title(title)
        self.frm = ttk.Frame(self.root, padding=10)
        self.row=-1 #current row
        self.column=0 #current column
        self.callafter=callafter
        self.aftertime=aftertime
        self.doingafter=None
        self.dict={}
        
    def addpair(self,label,vname,vinit='N/A',newrow=True):
        
        if newrow:
            self.row+=1
            self.column=0      
        ttk.Label (self.root,text=label).grid(column=self.column,row=self.row)
        if vname is None: #if just another constant
            ttk.Label (self.root,text=vinit).grid(column=self.column+1,row=self.row)
        else:
            strvar=tk.StringVar(self.root,vinit,name=vname)
            self.dict[vname]=strvar
            ttk.Label(self.root,textvariable=strvar).grid(column=self.column+1,row=self.row)
        self.column+=2
        
    def addbutton(self,vinit,command,vname=None,newrow=True,column=None):      
        
        if newrow:
            self.row+=1
            self.column=0
        if not column is None: #if clomn specified
            self.column=column
        if vname is None: #if not variable text
            ttk.Button(self.root,text=vinit,command=command).grid(column=self.column,row=self.row)
        else:
            strvar=tk.StringVar(self.root,vinit)
            self.dict[vname]=strvar
            ttk.Button(self.root,textvariable=strvar,command=command).grid(column=self.column,row=self.row)
        self.column+=1
        
    def doafter(self):
        self.doingafter=self.root.after(self.aftertime,self.callafter)
        
    def mainloop(self):
        self.root.mainloop()
        
    def cancel(self):
        self.root.after_cancel(self.doingafter)
        
    def setvar(self,name,value):
        self.dict[name].set(value)


def circlist(thelist,theitem,maxlength):
    #adds theitem to the bottom of thelist and pops the top if maxlength exceeded
    thelist.append(theitem)
    if len(thelist)> maxlength:
        thelist.pop(0)

def getduration(oldtime):
    from datetime import timedelta  
    elapsed=timedelta(seconds=round(time.time()-oldtime))
    return str(elapsed)
        
def goodresult(curtask,index,ms):
    curtask["lastgood"]=time.time()
    curtask['conseq']+=1
    curtask['results'].append({"time":curtask['lastgood'],"index":index,"ms":ms}) #put it on the list
    circlist(curtask["results"],{"time":curtask['lastgood'],"index":index,"ms":ms},curtask['resultlim'])

    
    
    
def do_ping(curtask,index):
    import subprocess
   
    
    pingmin=4
    jittermin=10
    pingfailmax=5 #seconds until failure declared
    
    global failstart #tracks ongoing failure
    global possfailstart
    global failcount
    global lastfailend
    
    ms=-1
    try:
        resp=ping3.ping(curtask['script'][index],unit='ms',timeout=curtask['timeout'])
        ms=round(resp)
        returncode=0
    except ping3.errors.HostUnknown:
        returncode=1
    except ping3.errors.Timeout:        
        returncode=2
    except ping3.errors.PingError:
        returncode=3
    #glop=subprocess.run("ping "+curtask['script'][index]+' -n 1 -w '+str(curtask['timeout']),capture_output=True, shell=True)
    if returncode==0:  #if it succeeded
        if failstart>0: #if we were in a failure
            mw.setvar("duration",getduration(failstart))
            mw.setvar("avgduration",avgduration.updateavg(time.time()-failstart))
            failstart=0 #we're not failing any more
            lastfailend=time.time()
            
        if lastfailend>0:
            x=getduration(lastfailend)
            mw.setvar("lastfail",x)        
    
        #lines=glop.stdout.decode().splitlines()
        #thetime=''
        #for line in lines:
            #ix=line.find('time')
            #if ix>=0:   #if this line has time
                #pline=line[ix+5:] #get the line starting at number
                #ix=pline.find('ms')
                #if ix>0:    #if end found
                    #thetime=pline[:ix]
        if ms>0:   #if could find time  
           # ms=int(thetime)
            goodresult(curtask,index,ms)
            if len(curtask['results'])>=pingmin: #if have enough samples
                relresults=curtask["results"][-pingmin:]
                x=np.mean([res['ms'] for res in relresults])
                mw.setvar('latency',"{:4.1f}".format(x))
                mw.setvar('avglatency',avglatency.updateavg(x))
            # now work on jitter
               
                circlist(pingqs[index],ms,jittermin+1) #put the time at the bottom of the q
                if len(pingqs[index])>1: # if there's anything else on the list
                    pingqs[index][-2]=abs(pingqs[index][-2]-pingqs[index][-1]) #turn it into jitter
                    jit=np.mean([np.median(q) for q in pingqs[:-1] if len(q)>=2])
                    if not np.isnan(jit): #if enough to calculate
                        mw.setvar("jitter","{:4.1f}".format(jit))
                        mw.setvar("avgjitter",avgjitter.updateavg(jit))
                    
    else:   #if ping failed
    # at some point must show failure cause somewhere. skipping for now
        if curtask['conseq']>0: #if last did not fail       
            curtask['conseq']=0 #break the string
            possfailstart=time.time() #remember possible failure start
        faillength=time.time()-possfailstart
        #print('fail length',faillength)
        if pingfailmax<faillength: #if we reached limit of our patience
            if not failstart>0: #if not already in outage
                failstart=possfailstart
                mw.setvar("lastfail",'now')
                failcount+=1
                mw.setvar("failcount",failcount)
            else:
                mw.setvar("duration",getduration(failstart))
                
        
    #print("results",glop) #debugging
    


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
    mw.doafter() #set next iteration
    
#button processor
            
def killall(): #action for quit button
    global killsw
    
    killsw=True #in case lingering calls
    print("shutting down....")
    if mw.doingafter is not None:
        mw.cancel()
    mw.root.destroy()

def pausetoggle():  #action for pause button
    global pausesw
    
    if pausesw: #if already paused
        pausesw=False #resume
        mw.setvar("pausebutton","Pause")
    else: #if not paused
        pausesw=True
        mw.setvar("pausebutton","Resume")


# initialization

pingtasks=[('8.8.8.8',1),('1.1.1.1',1),('208.67.222.222',1)] #locations to ping and weighting
pingqs=[[] for i in range(len(pingtasks))]


pingdict={"task":do_ping,"interval":1,"timeout":1,"label":"latency in ms","results":[],"conseq":0,"resultlim":12,
          "lastgood":time.time()}  # will come from preferences
pingdict["script"]=maketaskarray(pingtasks) #add scripts and output array
featuredict={'ping':pingdict}    #will add at least speedtest and monitor

thequeue=[] #revolving q of tasks to schedule
for feature, dictionary in featuredict.items():    #create a queue and thread for each feature
    thequeue.append({"name":feature,"interval":dictionary["interval"],"last":0,"index":0})
        


doafter=None #pending doafter
killsw=False
pausesw=False
failstart= 0 #any nonzero value means failure underway. blocks execution of nonping tests
possfailstart=0 #time of last test if it failed
failcount=0
lastfailend=0
avgduration=avgobj()
avglatency=avgobj()
avgjitter=avgobj()



buttonignore=True #because buttons call their code during setup     
mw=mainwindow(checkstatus,200)   #create the window
mw.addpair('time since failure:','lastfail')
mw.addpair('failure count:','failcount',vinit=str(0),newrow=False)
mw.addpair('last failure duration:','duration')
mw.addpair('average:','avgduration',newrow=False)
mw.addpair ('current latency in ms:',"latency")
mw.addpair ("average:","avglatency",newrow=False)
mw.addpair ('current jitter in ms:',"jitter")
mw.addpair ("average:","avgjitter",newrow=False)
mw.addbutton("Pause",pausetoggle,vname="pausebutton")
mw.addbutton("Quit",killall,newrow=False,column=3)
 

buttonignore=False #now buttons are good to go
mw.doafter()
mw.mainloop()
print('goodby')