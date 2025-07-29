from typing import Iterable

class Writer:
    def __init__(self, file_obj):
        self._file_obj = file_obj

    def write_row(self, row: Iterable[str]):
        if row:
            chunk = ''.join(f'{Writer.escape(cell)}\n' for cell in row)
            self._file_obj.write(chunk)
        self._file_obj.write('\n')

    def write_rows(self, rows: Iterable[Iterable[str]]):
        for row in rows:
            self.write_row(row)

    @staticmethod
    def escape(s):
        if s == '':
            return '\\'
        return s.replace("\\", "\\\\").replace("\n", "\\n")  # i know
