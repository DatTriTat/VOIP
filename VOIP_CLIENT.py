#!/usr/bin/env python
import pyaudio
import socket
import sys
import wave
import tkinter
import threading

po = tkinter.Tk()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 10240
WAVE_OUTPUT_FILENAME = "recording.wav"

counter = 0
is_recording = False 

def counter_label(label):
    counter = 0

    def count():
        nonlocal counter
        counter += 1
        label.config(text=str(counter))
        label.after(1000, count)

    count()

po.title("Client")
label = tkinter.Label(po, fg="dark green")
label.pack()

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

host = 'localhost'
port = 65535
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
frames = []


def listen_thread():
    while True:
        data = stream.read(CHUNK)
        s.send(data)
        s.recv(size)


def record_thread():
    global is_recording
    print("* recording")
    counter_label(label)
    is_recording = True
    frames.clear()
    while is_recording:
        data = stream.read(CHUNK)
        s.send(data)
        frames.append(data)
    print("* done recording")
    if frames:
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    is_recording = False


def lis():
    threading.Thread(target=listen_thread, daemon=True).start()


def rec():
    threading.Thread(target=record_thread, daemon=True).start()


def stop_recording():
    global is_recording
    global counter
    counter = 0
    label.config(text=str(counter))
    is_recording = False


def ex():
    sys.exit(0)


b = tkinter.Button(po, text='Listen', width=40, command=lis, fg='black')
b1 = tkinter.Button(po, text='Record', width=40, command=rec, bg='white')
b2 = tkinter.Button(po, text='Stop', width=25, command=stop_recording)
b3 = tkinter.Button(po, text='Exit', width=40, command=po.destroy)
b.pack()
b1.pack()
b2.pack()
b3.pack()

po.mainloop()
s.close()
stream.close()
p.terminate()
