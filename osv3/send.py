#! /usr/bin/env python3

# ./compile osv1

import subprocess
import os
import sys
import shutil

COMMENT = '#'

BAD_WORDS = [
    'Str0', 'Str1', 'Str2', 'Str3', 'Str4', 'Str5', 'Str6', 'Str7', 'Str8', 'Str9',
    '→',
    # the rest are assumptions
    '₁', '₂', '►'
]

EXTENSION_OLD_PP = '.tib'
EXTENSION_PARSE_NEW_PP = '.tibc'

def term(cmds:list):
    subprocess.run(cmds, check=True)

def deal_with_program(input_file):

    # determine preprocessor based on extension

    use_new_preprocessor = None
    extension = None

    if input_file.endswith(EXTENSION_OLD_PP):
        use_new_preprocessor = False
        extension = EXTENSION_OLD_PP
    elif input_file.endswith(EXTENSION_PARSE_NEW_PP):
        use_new_preprocessor = True
        extension = EXTENSION_PARSE_NEW_PP
    else:
        assert False

    # some basic checks

    program_name = input_file[:-len(extension)]

    # assert input_file.upper() == input_file
    assert len(program_name) <= 8

    # preprocess c

    if use_new_preprocessor:
    
        # copy all `.h` files
        for path, folders, files in os.walk('.'): # TODO hardcoded path
            for file in files:
                if file.endswith('.h'):
                    path_to_file = os.path.join(path, file)
                    shutil.copyfile(path_to_file, f'/tmp/{file}')
            break

        not_preprocessed_file_c = f'/tmp/{program_name}.c'
        shutil.copyfile(input_file, not_preprocessed_file_c)

        preprocessed_file_c = f'/tmp/{program_name}_preprocessed.c'
        term(['gcc', '-E', '-o', preprocessed_file_c, not_preprocessed_file_c])
    
    else:

        preprocessed_file_c = input_file

    # preprocess python

    if use_new_preprocessor:

        # TODO remove `#`` only if at beginning of line

        with open(preprocessed_file_c, 'r') as f:
            data = f.read()

        data_new = []
        for line in data.splitlines():

            # if line starts with `#`, delete line
            if len(line) and line[0] == COMMENT:
                continue

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

        preprocessed_file = f'/tmp/{program_name}.tib'

        with open(preprocessed_file, 'w')as f:
            f.write('\n'.join(data))

    else:

        # old preprocessor
        # considers everything after `#` a comment

        with open(preprocessed_file_c, 'r') as f:
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

        preprocessed_file = f'/tmp/{program_name}.tib'

        with open(preprocessed_file, 'w')as f:
            f.write('\n'.join(data))

    # compile

    compiled_file = f'/tmp/{program_name}.8xp'

    assert preprocessed_file.endswith('.tib') # otherwise the compiler refuses to work
    term(['ti84cc', '-o', compiled_file, preprocessed_file])

    # send to calc

    term(['tilp', '--no-gui', compiled_file])

if __name__ == '__main__':
    for program in sys.argv[1:]:
        deal_with_program(program)
