import os
import unittest
from io import StringIO

import nsv
from test_utils import SAMPLES_DATA, dump_sample, dumps_sample, SAMPLES_DIR


class TestDump(unittest.TestCase):
    def test_dump(self):
        for name in SAMPLES_DATA:
            with self.subTest(name=name):
                actual = dump_sample(name)
                file_path = os.path.join(SAMPLES_DIR, f'{name}.nsv')
                with open(file_path, 'r') as f:
                    expected = f.read()
                self.assertEqual(expected, actual)

    def test_dumps(self):
        for name in SAMPLES_DATA:
            with self.subTest(name=name):
                actual = dumps_sample(name)
                file_path = os.path.join(SAMPLES_DIR, f'{name}.nsv')
                with open(file_path, 'r') as f:
                    expected = f.read()
                self.assertEqual(expected, actual)

    def test_parity(self):
        for name, data in SAMPLES_DATA.items():
            with self.subTest(name=name):
                self.assertEqual(nsv.dumps(data), nsv.dump(data, StringIO()).getvalue())


if __name__ == '__main__':
    unittest.main()
