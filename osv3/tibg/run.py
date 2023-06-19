

import sys

var = __import__('var')
var_new = __import__('var-new').main

ITEM_SEPARATORS = \
    (WHITESPACE := ' \t\n') + \
    (STRING := "'") + \
    (LIST_BEGIN := '[') + \
    (LIST_END := ']') + \
    (NESTED_STR_BEGIN := '{') + \
    (NESTED_STR_END := '}')

def execute_command(list_):
    command = list_[0]
    args = list_[1:]

    print(list_)

    try:
        module = __import__(f'{command}')
    except ModuleNotFoundError:
        assert False, f'command not found `{command}`'
    else:
        return module.main(*args)

def pop_item(code):
    command = ''
    while code:
        char = code[0]        

        if char in ITEM_SEPARATORS:

            if len(command) == 0:
                
                if char in WHITESPACE:
                    return pop_item(code[1:])

                elif char == LIST_BEGIN:
                    code = code[1:]
                    list_ = []
                    while True:
                        item, code = pop_item(code)
                        if item == LIST_END:
                            break
                        if type(item) == list:
                            item = execute_command(item)
                        list_.append(item)
                    return list_, code

                elif char == NESTED_STR_BEGIN:
                    # TODO this fucking sucks
                    code = code[1:]

                    code_tmp_offset = 0
                    while True:
                        code_tmp = code[code_tmp_offset:]

                        end = code_tmp.index(NESTED_STR_END)
                        code_tmp_offset += end + 1

                        code_tmp = code[:code_tmp_offset]

                        if code_tmp.count(NESTED_STR_BEGIN) == code_tmp.count(NESTED_STR_END) - 1:
                            break

                    return code[:code_tmp_offset-1], code[code_tmp_offset+1:]

                elif char == LIST_END: # this might turn out to be a very bad idea
                    return LIST_END, code[1:]

                elif char == STRING:
                    code = code[1:]
                    end = code.index(STRING)
                    return code[:end], code[end+1:]

                assert False, 'bad syntax'

            return command, code

        command += char
        code = code[1:]

    return None, code


def main(code):

    if 'ret-val' not in var.variables:
        var_new('ret-val')

    while code:

        list_, code = pop_item(code)
        if list_ == None:
            break
        assert type(list_) == list, f'{type(list_)=} ; {list_=}'

        execute_command(list_)

    return var.main('ret-val')