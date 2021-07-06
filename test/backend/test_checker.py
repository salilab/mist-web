import unittest
import mist
import saliweb.test
import saliweb.backend
import tempfile
import os


def make_input_file(tmpdir, contents, mode='w'):
    fname = os.path.join(tmpdir, 'input.txt')
    with open(fname, mode) as fh:
        fh.write(contents)
    return fname


class Tests(saliweb.test.TestCase):
    """Check InputFileCheck class"""

    def test_bad_length(self):
        """Test file with bad line lengths"""
        with tempfile.TemporaryDirectory() as d:
            fname = make_input_file(d, """#\t#\t#\tExps\tA1\tA2\tB1
#\t#\t#\tBaits\tA\tB\tC
Prey\t#\tLength\tBaitSims\tA\tA\tB|C
Protein1\t#\t188\t#\t12\t4
""")
            check, msg = mist.InputFileCheck().fileCheck(fname)
            self.assertFalse(check)
            self.assertEqual(msg, '\n\tLine 4 disagrees with #Exp (7)!\n')

    def test_binary_file(self):
        """Test binary file (invalid UTF-8)"""
        with tempfile.TemporaryDirectory() as d:
            fname = make_input_file(d, b"test\xee\x9dfile", mode='wb')
            check, msg = mist.InputFileCheck().fileCheck(fname)
            self.assertTrue(check)

    def test_bad_value(self):
        """Test file with bad values"""
        with tempfile.TemporaryDirectory() as d:
            fname = make_input_file(d, """#\t#\t#\tExps\tA1\tA2\tB1
#\t#\t#\tBaits\tA\tB\tC
Prey\t#\tLength\tBaitSims\tA\tA\tB|C
Protein1\t#\t188\t#\tFOO\tBAR\t27
""")
            check, msg = mist.InputFileCheck().fileCheck(fname)
            self.assertFalse(check)
            self.assertEqual(
                msg, '\n\tElement in line 4, row 5 is not a value!\n'
                     '\tElement in line 4, row 6 is not a value!\n')

    def test_repeated_experiment(self):
        """Test file with repeated experiment"""
        with tempfile.TemporaryDirectory() as d:
            fname = make_input_file(d, """#\t#\t#\tExps\tA1\tA2\tA1
#\t#\t#\tBaits\tA\tB\tC
Prey\t#\tLength\tBaitSims\tA\tA\tB|C
Protein1\t#\t188\t#\t12\t4\t27
""")
            check, msg = mist.InputFileCheck().fileCheck(fname)
            self.assertFalse(check)
            self.assertEqual(msg, '\n\tExperiment A1 repeated!\n')

    def test_repeated_prey(self):
        """Test file with repeated prey"""
        with tempfile.TemporaryDirectory() as d:
            fname = make_input_file(d, """#\t#\t#\tExps\tA1\tA2\tB1
#\t#\t#\tBaits\tA\tB\tC
Prey\t#\tLength\tBaitSims\tA\tA\tB|C
Protein1\t#\t188\t#\t12\t4\t27
Protein1\t#\t188\t#\t12\t4\t27
Protein2\t#\t188\t#\t12\t4\t27
""")
            check, msg = mist.InputFileCheck().fileCheck(fname)
            self.assertFalse(check)
            self.assertEqual(msg, '\n\tPrey Protein1 repeated!\n')


if __name__ == '__main__':
    unittest.main()
