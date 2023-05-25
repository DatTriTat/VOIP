import pyaudio
import socket
import tkinter
import threading

po=tkinter.Tk()

chunk = 1024
p = pyaudio.PyAudio()

stream = p.open(format = pyaudio.paInt16,
                channels = 1,
                rate = 10240,
                output = True)

host = 'localhost'
port = 65535
backlog = 5
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)

client, address = s.accept()

def li():
    while 1:
        data = client.recv(size)
        if data:
            stream.write(data)
            client.send(b'ACK')

def start_li_thread():
    li_thread = threading.Thread(target=li)
    print("check")
    li_thread.start()
    
po.title("Server")
m=tkinter.Button(po,width=40,text='Start',command=start_li_thread,fg='black')
m1=tkinter.Button(po,width=50,text='Exit',command=po.destroy)
m.pack()
m1.pack()
po.mainloop()
client.close()
stream.close()
p.terminate()