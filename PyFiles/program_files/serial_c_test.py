import serial
import struct
from time import sleep
from serial_communication import SerialCommunication

'''def send_packet(ser):
        red_enable = struct.pack('B', 255)
        green_enable = struct.pack('B', 255)
        blue_enable = struct.pack('B', 255)
        off_time = struct.pack('f', 3.0)
        switch_time = struct.pack('H', 200)
        packet = b"\x16\x55" + red_enable + green_enable + blue_enable + off_time + switch_time
        ser.write(packet)
        print(packet.hex())

def receive(s):
    packet = b"\x16\x22" + b'\x00'*9
    s.write(packet)
    data = s.read(9)
    print(data[0])
    print(data[1])
    print(data[2])
    print(struct.unpack('f', data[3:7])[0])
    print(struct.unpack('H', data[7:9])[0])'''
    
def main():

    values = [1, 30, 50, 3.2, 4.5, 0.05, 1.21, 5.5, 0.40, 150, 200, 100, 3, 4, 5, 6, 7, 8, 9, 10]

    yes = SerialCommunication()
    
    yes.send_packet(values)

    yes.receive_packet()
    

if __name__ == "__main__":
    main()