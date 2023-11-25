def read_by_line(filepath: str, format_func=None):
    with open(filepath, "r") as f:
        out = [x.replace('\n', '').replace('\r', '') for x in f.readlines()]
        if format_func is not None:
            out = [format_func(x) for x in out]
        return out