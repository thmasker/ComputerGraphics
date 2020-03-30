import sys, getopt, os.path
from typing import List

import utils


def usage():
    print('Simple Lathe')
    print('------------------------------------')
    print('Usage: lathe <options> <.obj file>*')
    print('<options>:')
    print('\t-s, --steps=')
    print('\t-a, --angle=')
    print('\t-r, --rotation=[x, y, z]. Default z')
    print('------------------------------------')


def main(argv: List[str]):
    steps = 0
    angle = 0
    rotation = 'z'
    try:
        opts, args = getopt.getopt(argv, "s:a:r:", ['help', 'steps=', 'angle=', 'rotation='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--help':
            usage()
            sys.exit()
        elif opt in ('-s', '--steps'):
            try:
                steps = int(arg)
            except ValueError:
                print("Steps '" + arg +  "' is not a valid number (int)")
                sys.exit(2)
        elif opt in ('-a', '--angle'):
            try:
                angle = float(arg)
            except ValueError:
                print("Angle '" + arg + "' is not a valid number (int or float)")
                sys.exit(2)
        elif opt in ('-r', '--rotation'):
            if arg in ('x', 'X', ' x', ' X'):
                rotation = 'x'
            elif arg in ('y', 'Y', ' y', ' Y'):
                rotation = 'y'

    angle_per_step = angle / steps

    for file in args:
        try:
            f = open(file)
        except FileNotFoundError as fne:
            print(fne.strerror + ": '" + file + "'")
            sys.exit(2)

        lines = f.readlines()
        f.close()

        vertices = []
        ls = []
        info = []
        for line in lines:
            if line[0] == 'v':
                vertices.append(utils.toVertex(line))
            elif line[0] == 'l':
                ls.append(utils.toFace(line))
            else:
                info.append(line)

        n_vertices = len(vertices)
        n_ls = len(ls)

        faces = []
        for s in range(steps):
            for i in range(n_vertices * s, n_vertices * (s + 1)):
                vertices.append(utils.rotate(vertices[i], -angle_per_step, rotation))

            for i in range(n_ls * s, n_ls * (s + 1)):
                ls.append([ls[i][0] + n_vertices, ls[i][1] + n_vertices])
                faces.append([ls[i][0] + n_vertices, ls[i][1], ls[i][0]])
                faces.append([ls[i][0] + n_vertices, ls[i][1] + n_vertices, ls[i][1]])

        new_file = os.path.splitext(file)
        with open(new_file[0] + '_lathe' + new_file[1], 'w') as f:
            f.write(''.join(info))
            f.write(''.join(utils.toString(vertices, 'v')))
            f.write(''.join(utils.toString(faces, 'f')))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    else:
        main(sys.argv[1:])