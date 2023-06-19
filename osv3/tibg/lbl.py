
gen_lbl = __import__('gen-lbl')

def main(name):
    return f'Lbl {gen_lbl.labels.index(name)}\n'