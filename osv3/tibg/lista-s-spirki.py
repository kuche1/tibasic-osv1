def main(avtobus):
    match avtobus:
        case '88':
            return ['na-maikati-putkata', 'boli-me-kura', 'bai-hui']
    
    assert False, f'ne go znam toq avtobus `{avtobus}`'