def main(lbl, *args):
    args = list(args)

    ret = f'Menu({lbl}'

    while args:
        name = args.pop(0)

        assert len(args) > 0, f'missing an argument for label'
        label = args.pop(0)

        ret += f',{name},{label}'

    return ret + '\n'