import serial
import struct
from time import sleep

def send_packet(ser):
        red_enable = struct.pack('B', 1)
        green_enable = struct.pack('B', 0)
        blue_enable = struct.pack('B', 0)
        off_time = struct.pack('f', 3.0)
        switch_time = struct.pack('H', 200)
        packet = b"\x16\x55" + red_enable + green_enable + blue_enable + off_time + switch_time
        ser.write(packet)
        print(packet.hex())

def receive(s):
    packet = b"\x16\x22" + b'\x00'*9
    s.write(packet)
    data = s.read(9)
    print(data)
    #print(data[1])
    #print(data[2])
    #print(struct.unpack('f', data[3:7])[0])
    #print(struct.unpack('H', data[7:9])[0])
    
def main():
    with serial.Serial(port='COM4',baudrate=115200,timeout=1) as s:
        send_packet(s)
        sleep(1)
        receive(s)

if __name__ == "__main__":
    main()