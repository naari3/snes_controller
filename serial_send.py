import serial
import time
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-f", "--file", dest="filepath",
                  help="tas movie dump file", metavar="FILE")

baud = 115200

STAND_BY = b'\x00'
READY = b'\x01'
REQ_NEXT = b'\x02'


def m3():
    # a = [b'\x00\x01', b'\x00\x01', b'\x01\x00', b'\x01\x00', b'\x00\x02', b'\x00\x02', b'\x02\x00', b'\x02\x00', b'\x00\x04', b'\x00\x04', b'\x00\x08', b'\x00\x08', b'\x04\x00', b'\x04\x00', b'\x10\x00', b'\x10\x00', b'\x20\x00', b'\x20\x00', b'\x40\x00', b'\x40\x00', b'\x80\x00', b'\x80\x00']
    a = [b'\x00\x01',  b'\x01\x00',  b'\x00\x02',  b'\x02\x00',  b'\x00\x04',
         b'\x00\x08',  b'\x04\x00',  b'\x10\x00',  b'\x20\x00',  b'\x40\x00',  b'\x80\x00']
    i = 0
    while True:
        b = a[i % len(a)]
        i += 1
        yield b


def open_file(filepath):
    return open(filepath, 'rb')


def get_port():
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "usbmodem" in port.device:
            return port.device.replace("cu", "tty")


def ready(ser):
    ser.write(STAND_BY)
    while ser.read() != READY:
        pass


def controll(ser, movie):
    while True:
        if ser.read() == REQ_NEXT:
            data = movie.read(2)
            if data != b'':
                ser.write(data)
            else:
                movie.close()


def main():
    (options, args) = parser.parse_args()

    movie = open_file(options.filepath)

    port = serial.Serial()
    port.port = get_port()
    port.baudrate = baud
    with port as ser:

        print("ready...")
        time.sleep(2)
        ready(ser)

        controll(ser, movie)

        print("end")


if __name__ == '__main__':
    main()
