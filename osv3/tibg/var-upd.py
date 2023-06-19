
import var

def main(name, value):
    assert name in var.variables
    var.variables[name] = value
