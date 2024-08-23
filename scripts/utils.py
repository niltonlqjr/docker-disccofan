@staticmethod
def lines_of(string, sep='\n'):
    return string.split(sep)

@staticmethod
def line_to_list(line, columns_types, header=True):
    spl = line.split()
    ncolum=len(columns_types)
    if len(spl) != ncolum:
        print(f'Line:{line} has {len(spl)} fields.\nExpected {len(columns_types)}')
        return []
    ret = [columns_types[i](spl[i]) for i in range(ncolum)]
    return ret