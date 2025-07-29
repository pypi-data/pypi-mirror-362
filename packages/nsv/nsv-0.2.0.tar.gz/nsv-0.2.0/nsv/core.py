from .reader import Reader
from .writer import Writer

def load(file_obj) -> list[list[str]]:
    """Load NSV data from a file-like object."""
    return list(Reader(file_obj))

def loads(s) -> list[list[str]]:
    """Load NSV data from a string."""
    data = []
    acc = []
    if not s:
        return []
    for i, line in enumerate(s.split('\n')[:-1]):
        if line:
            acc.append(Reader.unescape(line))
        else:
            data.append(acc)
            acc = []
    return data

def dump(data, file_obj):
    """Write elements to an NSV file."""
    Writer(file_obj).write_rows(data)
    return file_obj

def dumps(data):
    """Write elements to an NSV string."""
    lines = []
    for i, row in enumerate(data):
        for cell in row:
            lines.append(Writer.escape(cell))
        lines.append('')
    return '\n'.join(lines) + '\n' if lines else ''
