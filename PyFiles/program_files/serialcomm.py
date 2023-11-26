import serial
import glob
import sys
import struct
import time

class SerialCommunication:
    def __init__(self, port='/dev/tty.wlan-debug', baudrate=115200, timeout=0.05):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.packet_size = 26
        self.packet_format = ['B'] * self.packet_size
        #self.packet_format = ['B', 'B', 'B', 'f', 'H']
        #self.packet_size = 9

    def open_serial_connection(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_TWO,
                timeout=self.timeout,
                xonxoff=False,
                rtscts=False,
                dsrdtr=False,
                write_timeout=None,
                inter_byte_timeout=None
            )
            #print(f"Serial connection opened on {self.port}")
        except serial.SerialException as e:
            pass
            #print(f"Error opening serial connection: {e}")

    def close_serial_connection(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            #print("Serial connection closed")

    def send_packet(self, values):
        self.open_serial_connection()
        SYNC_BYTE = b"\x16\x55"
        packet = SYNC_BYTE 
        for format_specifier, value in zip(self.packet_format, values):
            packet += struct.pack(format_specifier, value)
        self.ser.write(packet)
        #print(packet.hex())
        self.close_serial_connection()

    def receive_packet(self):
        # Close the serial connection if it's open
        if self.ser and self.ser.is_open:
            self.ser.close()

        # Open a new serial connection
        self.open_serial_connection()

        packet = b"\x16\x22" + b'\x00'*26
        self.ser.write(packet)
        #data = self.ser.read(struct.calcsize(''.join(self.packet_format)))  # Read the required number of bytes
        data = self.ser.read(26)  # Read the required number of bytes
        self.values = struct.unpack('<' + ''.join(self.packet_format), data)

        #print("Received values:", self.values)

        # Clear data and values before returning
        values_to_return = self.values
        self.values = None

        return values_to_return

    
def list_serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def receive(s):
    packet = b"\x16\x22" + b'\x00'*26
    #s.write(packet)
    print(packet.hex())
    data = s.read()
    print(data)

print(list_serial_ports())

def main():

    values = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    #values = [1, 1, 1, 0.5, 200]
    #print(list_serial_ports())
    yes = SerialCommunication(port='/dev/tty.usbmodem0006210000001')
    
    yes.send_packet(values)

    time.sleep(1)

    yes.receive_packet()


#main()