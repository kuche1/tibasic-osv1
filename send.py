#! /usr/bin/env python3

# ./compile osv1

import subprocess
import os
import sys

COMMENT = '#'

BAD_WORDS = [
    'Str0', 'Str1', 'Str2', 'Str3', 'Str4', 'Str5', 'Str6', 'Str7', 'Str8', 'Str9',
    '→',
    # the rest are assumptions
    '₁', '₂', '►'
]

def deal_with_program(input_file):

    tmp = '.tib'
    assert input_file.endswith(tmp)
    program_name = input_file[:-len(tmp)]

    # assert input_file.upper() == input_file

    assert len(program_name) <= 8

    with open(input_file, 'r') as f:
        data = f.read()

    data_new = []
    for line in data.splitlines():
        if COMMENT in line:
            line = line.split(COMMENT)
            line = line[0]

        while line.startswith(' ') or line.startswith('\t'):
            line = line[1:]

        while line.endswith(' ') or line.endswith('\t'):
            line = line[:-1]

        if line.count(' ') + line.count('\t') == len(line):
            continue

        for badword in BAD_WORDS:
            assert badword not in line, f'bad word found `{badword}`'

        data_new += [line]

    data = data_new

    preprocessed_file = f'/tmp/{input_file}.tib'

    with open(preprocessed_file, 'w')as f:
        f.write('\n'.join(data))

    # # delete all previous compiled files
    # for path, _, files in os.walk('.'):
    #     break
    # for file in files:
    #     if not file.endswith('.8xp'):
    #         continue
    #     p = os.path.join(path, file)
    #     os.remove(p)

    compiled_file = f'/tmp/{program_name}.8xp'

    subprocess.run(['ti84cc', '-o', compiled_file, preprocessed_file], check=True)

    # os.remove(preprocessed_file)

    subprocess.run(['tilp', '--no-gui', compiled_file], check=True)

if __name__ == '__main__':
    for program in sys.argv[1:]:
        deal_with_program(program)
