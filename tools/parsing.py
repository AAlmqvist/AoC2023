def read_by_line(filepath: str, parse_func=None):
    with open(filepath, "r") as f:
        # read lines and replace line break and clear line characters
        out = [x.replace('\n', '').replace('\r', '') for x in f.readlines()]
        # remove any empty lines
        out = [x for x in out if x != '']
        # if each line should be parsed into something else than a string
        if parse_func is not None:
            out = [parse_func(x) for x in out]
        return out

def read_with_delimeter(filepath: str, split_by, parse_func=None):
    with open(filepath, "r") as f:
        # read lines and replace line break and clear line characters
        out = [x.replace('\r', '') for x in f.read().split(split_by)]
        # remove any empty lines
        out = [x for x in out if x != '']
        # if each line should be parsed into something else than a string
        if parse_func is not None:
            out = [parse_func(x) for x in out]
        return out