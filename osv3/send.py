#! /usr/bin/env python3

# ./compile osv1

import subprocess
import os
import sys
import shutil

COMMENT = '#'

DIRECTIVE_BEGIN = '${'
DIRECTIVE_END = '}'

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

        with open(preprocessed_file_c, 'r') as f:
            data = f.read()

        # remove gcc autogen comments
        data_new = []
        for line in data.splitlines():
            if line.startswith(COMMENT):
                continue
            data_new += [line]
        data = '\n'.join(data_new)


        # deal with directives
        data_new = []

        while DIRECTIVE_BEGIN in data:

            start = data.index(DIRECTIVE_BEGIN)

            data_head = data[:start]
            data = data[start+len(DIRECTIVE_BEGIN) : ]

            directives = 1
            next_start = None
            next_end = None
            offset = 0
            while directives:
                next_start = data[offset:].find(DIRECTIVE_BEGIN)
                next_end = data[offset:].find(DIRECTIVE_END)

                assert next_end != -1 # syntax error

                if next_start == -1:
                    next_start = float('inf')

                if (next_end < next_start):
                    directives -= 1
                    if directives == 0:
                        break
                    offset += next_end + len(DIRECTIVE_END)
                elif (next_start < next_end):
                    directives += 1
                    offset += next_start + len(DIRECTIVE_BEGIN)
                else:
                    assert False

            end = offset + next_end

            cmd = data[ : end]

            data_tail = data[end+len(DIRECTIVE_END) : ]

            cmd = cmd.split(' ')
            arg = cmd[1:]
            cmd = cmd[0]
        
            data_mid = None # set this var in the `match`

            match cmd:

                case 'add':
                    a, b = arg
                    a = int(a)
                    b = int(b)
                    res = a + b
                    data_mid = res

                case 'for':
                    var = arg[0]
                    start = int(arg[1])
                    end = int(arg[2])
                    code = ' '.join(arg[3:])

                    data_mid = ''
                    for x in range(start, end):
                        data_mid += code.replace(var, str(x))

                case other:
                    assert False, f'invalid directive `{cmd}`'
                
            data = data_head + str(data_mid) + data_tail


        # get rid of whitespace
        # filter words
        data_new = []
        for line in data.splitlines():

            while line.startswith(' ') or line.startswith('\t'):
                line = line[1:]

            while line.endswith(' ') or line.endswith('\t'):
                line = line[:-1]

            if line.count(' ') + line.count('\t') == len(line):
                continue

            for badword in BAD_WORDS:
                assert badword not in line, f'bad word found `{badword}`'

            data_new += [line]

        data = '\n'.join(data_new)

        preprocessed_file = f'/tmp/{program_name}.tib'

        with open(preprocessed_file, 'w')as f:
            f.write(data)

    else:

        # old preprocessor
        # considers everything after `#` a comment

        comment = '#'

        with open(preprocessed_file_c, 'r') as f:
            data = f.read()

        data_new = []
        for line in data.splitlines():
            if comment in line:
                line = line.split(comment)
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
