import sys
import glob
import serial
import struct

ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    timeout=1,  # Set a timeout value in seconds
    xonxoff=False,
    rtscts=False,
    dsrdtr=False,
    write_timeout=None,
    inter_byte_timeout=None
)

print("yes")

data = ser.read(11)
print("your mom")
ok = data.decode('utf-8')
#print("asdksadasdsdsadsa")
#data_value = struct.unpack('11B', data)
print(data)



'''def serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        #print("okok")
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result'''