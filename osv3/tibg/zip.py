
var_upd = __import__('var-upd').main

def main(list1, list2):
    ret = []
    for item1, item2 in zip(list1, list2, strict=True):
        ret.append([item1,item2])
    var_upd('ret-val', ret)
