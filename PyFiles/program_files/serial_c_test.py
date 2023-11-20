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
    red_enable = 1
    green_enable = 0
    blue_enable = 0
    off_time = 3.0
    switch_time = 200
    
    #ser = serial.Serial
    values = [red_enable, green_enable, blue_enable, off_time, switch_time]
    #packet_format = ['B', 'B', 'B', 'f', 'h']
    #data = [1, 0, 0, 3.0, 200]
    #packed_data = struct.pack('<BBBfh', *data)
    #print(repr(packed_data))
    #data = ser.read(struct.calcsize(''.join(packet_format)))  # Read the required number of bytes
    #values = struct.unpack(''.join(packet_format), packed_data)
    #print("Received values:", values)
    
    #byte_sequence = struct.pack('<f', 3.0)
    #print(byte_sequence)
    #float_value = struct.unpack('<f', byte_sequence)[0]
    #print(float_value)

    yes = SerialCommunication()
    
    yes.send_packet(values)

    #data_string = "01000000004040c800"
    #data_bytes = bytes.fromhex(data_string)

    yes.receive_packet()
    

if __name__ == "__main__":
    main()