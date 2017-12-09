from optparse import OptionParser


parser = OptionParser()
parser.add_option("-f", "--file", dest="filepath",
                  help="tas movie dump file", metavar="FILE")


def open_file(filepath):
    return open(filepath, 'rb')


def bite_to_input(byte):
    input_list = list('BYsSudlrAXLR1234')
    input_int = int.from_bytes(byte, 'little')
    for i, s in enumerate(''.join(input_list)):
        if not bool(input_int & (1 << i)):
            input_list[i] = ' '
    return ''.join(input_list)


def play(movie):
    current_frames = 0
    while True:
        data = movie.read(2)
        print(f'{current_frames}: {bite_to_input(data)}')
        current_frames += 1
        if data == b'':
            movie.close()


def main():
    (options, args) = parser.parse_args()
    movie = open_file(options.filepath)

    play(movie)


if __name__ == '__main__':
    main()
