import serial
import struct
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
 
def send_packet(ser):
        red_enable = struct.pack('B', 1)
        green_enable = struct.pack('B', 0)
        blue_enable = struct.pack('B', 1)
        off_time = struct.pack('f', 1)
        switch_time = struct.pack('H', 200)
        packet = b"\x16\x55" + red_enable + green_enable + blue_enable + off_time + switch_time
        ser.write(packet)
        print(packet.hex())
 
def receive(s):
    packet = b"\x16\x22" + b'\x00'*26
    s.write(packet)
    #print(packet.hex())
    data = s.read(42)
    #print(struct.unpack('d', data[26:34])[0])
    return struct.unpack('d', data[26:34])[0]
   
x = [i for i in range(50)]
y = [0] * 50
   
fig, ax = plt.subplots(1)
 
def animate(i, y,x):
    with serial.Serial(port='/dev/tty.usbmodem0006210000001',baudrate=115200,timeout=0.01) as s:
        newy = receive(s)
 
    y.append(newy)
    y = y[-50:]
   
    ax.clear()
    ax.plot(x,y)
 
ani = animation.FuncAnimation(fig, animate, fargs=(y,x), interval=1, blit=False)
plt.ylim(-5000,5000)
plt.show()
 
   
def main():
    pass
 
if __name__ == "__main__":
    main()