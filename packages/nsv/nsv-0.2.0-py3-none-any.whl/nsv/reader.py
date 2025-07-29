class Reader:
    def __init__(self, file_obj):
        self._file_obj = file_obj

    def __iter__(self):
        return self

    def __next__(self):
        acc = []
        for line in self._file_obj:
            if line == '\n':
                return acc
            if line[-1] == '\n':  # so as not to chop if missing newline at EOF
                line = line[:-1]
            acc.append(Reader.unescape(line))  # bruh
        # at the end of the file
        if acc:
            return acc
        else:  # an empty row would self-report in the cycle body
            raise StopIteration

    @staticmethod
    def unescape(s):
        if s == '\\':
            return ''
        return s.replace("\\n", "\n").replace("\\\\", "\\")  # i know
