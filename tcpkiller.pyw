#coding=utf-8
import sys
try:
    from tkinter import *
    from tkinter import messagebox
    from tkinter import filedialog
except:
    from Tkinter import *
    errtk=Tk()
    Label(errtk,text=' Python版本错误,无法继续! ').pack()
    mainloop()
    sys.exit(-1)
import socket
import threading
import os
import time

ver='V4' #version

#load config
try:
    f=open('config.txt','r')
    configs={}
    for a in f.readlines():
        configs[a.split(':')[0]]=''.join(a.split(':')[1:]).strip()
    f.close()
    
    xs=int(configs['x'])
    ys=int(configs['y'])
    delay=float(configs['delay'])
    file=configs['file']
    target=int(configs['target'])
    host=configs['host']
    port=int(configs['port'])
except:
    xs=7 #x-size
    ys=5 #y-size
    delay=0.25
    target=0
    host=''
    port=80
    file='content.txt'

socket.setdefaulttimeout(10.0) #timeout
shouldq=1
inited=False
okt=0


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
    def loadfile():
        global file
        file=filedialog.askopenfilename()
        filename.set('请求文件: '+os.path.basename(file))
    
    def helps():
        import webbrowser
        webbrowser.open('https://github.com/xmcp/TCPKiller/blob/master/README.md')

    def initt():
        global inited,host,port,content,xs,ys,delay,file,target
        host=hostvar.get()
        port=portvar.get()
        xs=xvar.get()
        ys=yvar.get()
        delay=delayvar.get()
        target=targetvar.get()
        try:
            f=open(file,'br')
            content=f.read()
            f.close()
        except:
            messagebox.showerror('TCPKiller','文件加载失败')
        else:
            try:
                f=open('config.txt','w')
                f.write('x:%s\n'%xs)
                f.write('y:%s\n'%ys)
                f.write('host:%s\n'%host)
                f.write('port:%s\n'%port)
                f.write('target:%s\n'%target)
                f.write('delay:%s\n'%delay)
                f.write('file:%s\n'%file)
                f.close()
            except:
                messagebox.showerror('TCPKiller','配置文件写入失败')
            else:
                inited=True
                setup.destroy()
    
    global hostvar,portvar,setup
    setup=Tk()
    
    hostvar=StringVar() #target-hostname
    hostvar.set(host)
    portvar=IntVar() #target-port
    portvar.set(port)
    xvar=IntVar()
    xvar.set(xs)
    yvar=IntVar()
    yvar.set(ys)
    delayvar=DoubleVar()
    delayvar.set(delay)
    targetvar=IntVar()
    targetvar.set(target)
    filename=StringVar()
    filename.set('请求文件: '+os.path.basename(file))

    ipselect=Entry(setup,textvariable=hostvar)
    portselect=Entry(setup,textvariable=portvar)
    xselect=Entry(setup,textvariable=xvar)
    yselect=Entry(setup,textvariable=yvar)
    delayselect=Entry(setup,textvariable=delayvar)
    targetselect=Entry(setup,textvariable=targetvar)
    setupdone=Button(setup,text='完成',command=initt)

    setup.title('神通 '+ver)
    setup.resizable(False,False)

    Label(setup).grid(row=0,column=0)
    #row1
    Label(setup,text='主机').grid(row=1,column=0)
    ipselect.grid(row=1,column=1,columnspan=3,sticky=(W,E))
    Label(setup,text='端口').grid(row=1,column=4)
    portselect.grid(row=1,column=5)
    #row2
    Label(setup,text='线程(X轴)').grid(row=2,column=0)
    xselect.grid(row=2,column=1)
    Label(setup,text='线程(Y轴)').grid(row=2,column=2)
    yselect.grid(row=2,column=3)
    Label(setup,text='延时(s)').grid(row=2,column=4)
    delayselect.grid(row=2,column=5)
    #row3
    Label(setup,text='目标次数').grid(row=3,column=0)
    targetselect.grid(row=3,column=1)
    Button(setup,textvariable=filename,command=loadfile,relief=FLAT).grid(row=3,column=2,columnspan=2,sticky=(W))
    setupdone.grid(row=3,column=4)
    Button(setup,text='我该如何填写?',command=helps,relief=FLAT).grid(row=3,column=5,sticky=(W,E))
    Label(setup).grid(row=4,column=0)
    mainloop()

def stats(callback):
    global target,shouldq
    cached=0
    tall=0.5
    try:
        while 1:
            if shouldq==0:
                callback.title('成功%s  速率%s (%s)'%(okt,2*(okt-cached),int(okt//tall)))
                tall+=0.5
                if target!=0 and okt>=target:
                    shouldq=1
                    messagebox.showinfo('TCPKiller','%d次目标完成!\n平均速率:%d  用时:%ds'%(target,okt//tall,tall))
            else:
                callback.title('神通 '+ver)
            cached=okt
            time.sleep(0.5)
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
