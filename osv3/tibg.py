#! /usr/bin/env python3

import sys

def compile_file(file):
    with open(file, 'r') as f:
        source_code = f.read()

    sys.path.insert(0, 'tibg')
    run = __import__('run').main
    ret = run(source_code)
    del sys.path[0]

    return ret

if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = sys.argv[2]

    resulting_code = compile_file(in_file)

    with open(out_file, 'w') as f:
        f.write(resulting_code)
