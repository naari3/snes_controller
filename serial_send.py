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


def open_file(filepath):
    return open(filepath, 'rb')


def bite_to_input(byte):
    input_list = list('BYsSudlrAXLR1234')
    input_int = int.from_bytes(byte, 'little')
    for i, s in enumerate(''.join(input_list)):
        if not bool(input_int & (1 << i)):
            input_list[i] = ' '
    return ''.join(input_list)


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
    current_frames = 0
    while True:
        if ser.read() == REQ_NEXT:
            data = movie.read(2)
            print(f'{current_frames}: {bite_to_input(data)}')
            if data != b'':
                ser.write(data)
            else:
                movie.close()
            current_frames += 1


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
