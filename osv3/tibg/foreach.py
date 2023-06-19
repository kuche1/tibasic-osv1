var_new = __import__('var-new').main
var_upd = __import__('var-upd').main
var_del = __import__('var-del').main
run = __import__('run').main

def main(var, list_, code):
    ret = ''

    var_new(var)
    for item in list_:
        var_upd(var, item)
        ret += run(code)
    var_del(var)

    print(f'for result {ret=}')

    return ret