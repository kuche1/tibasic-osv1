
labels = []

def main(name):
    assert name not in labels
    labels.append(name)
    return str(labels.index(name))