
import var

def main(name):
    assert name not in var.variables, f'variable already exists `{name}`'
    var.variables[name] = None
