import unittest
import os
from io import StringIO

import nsv
from test_utils import SAMPLES_DIR, SAMPLES_DATA, load_sample, loads_sample


class TestLoad(unittest.TestCase):
    def test_load(self):
        for name, expected in SAMPLES_DATA.items():
            with self.subTest(sample_name=name):
                actual = load_sample(name)
                self.assertEqual(expected, actual)

    def test_loads(self):
        for name, expected in SAMPLES_DATA.items():
            with self.subTest(sample_name=name):
                actual = loads_sample(name)
                self.assertEqual(expected, actual)

    def test_parity(self):
        for name in SAMPLES_DATA:
            with self.subTest(sample_name=name):
                file_path = os.path.join(SAMPLES_DIR, f'{name}.nsv')
                with open(file_path, 'r') as f:
                    s = f.read()
                    self.assertEqual(nsv.loads(s), nsv.load(StringIO(s)))


if __name__ == '__main__':
    unittest.main()
