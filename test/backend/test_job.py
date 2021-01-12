import unittest
import mist
import saliweb.test
import saliweb.backend


class JobTests(saliweb.test.TestCase):
    """Check custom Job class"""

    def test_run_ok(self):
        """Test successful run method"""
        j = self.make_test_job(mist.Job, 'RUNNING')
        with saliweb.test.working_directory(j.directory):
            with open('param.txt', 'w') as fh:
                fh.write('training\nno_filtering\n')
            with open('input.txt', 'w') as fh:
                fh.write('#\t#\t#\tExps\tA1\tA2\tB1\n')
                fh.write('#\t#\t#\tBaits\tA\tB\tC\n')
                fh.write('Prey\t#\tLength\tBaitSims\tA\tA\tB|C\n')
                fh.write('Protein1\t#\t188\t#\t12\t4\t12\n')
            cls = j._run_in_job_directory(j.run)
            self.assertIsInstance(cls, saliweb.backend.SGERunner)

    def test_run_not_ok(self):
        """Test run method with bad input file"""
        j = self.make_test_job(mist.Job, 'RUNNING')
        with saliweb.test.working_directory(j.directory):
            with open('param.txt', 'w') as fh:
                fh.write('training\nno_filtering\n')
            with open('input.txt', 'w') as fh:
                fh.write('#\t#\t#\tExps\tA1\tA2\tA1\n')
                fh.write('#\t#\t#\tBaits\tA\tB\tC\n')
                fh.write('Prey\t#\tLength\tBaitSims\tA\tA\tB|C\n')
                fh.write('Protein1\t#\t188\t#\t12\t4\t12\n')
            cls = j._run_in_job_directory(j.run)
            self.assertIsInstance(cls, saliweb.backend.DoNothingRunner)

    def test_postprocess_ok(self):
        """Test postprocess method of OK run"""
        j = self.make_test_job(mist.Job, 'RUNNING')
        with saliweb.test.working_directory(j.directory):
            with open('output.log', 'w') as fh:
                fh.write('test header\n')
            with open('output_metrics.out', 'w') as fh:
                fh.write(
                    'Bait\tPrey\tReproducibility\tAbundance\tSpecificity\n')
                fh.write('A\tB\ttestrep\ttestab\ttestsp\n')
            with open('output_mist.out', 'w') as fh:
                fh.write('Bait\tPrey\tMiST score\n')
                fh.write('A\tB\ttestmist\n')
            j.postprocess()
            with open('MistOutput.txt') as fh:
                contents = fh.read()
            self.assertEqual(contents, """# test header

#Bait\tPrey\tReproducibility\tAbundance\tSpecificity\tMiST
A\tB\ttestrep\ttestab\ttestsp\ttestmist
""")

    def test_postprocess_bad(self):
        """Test postprocess method of bad run"""
        j = self.make_test_job(mist.Job, 'RUNNING')
        with saliweb.test.working_directory(j.directory):
            j.postprocess()  # should do nothing


if __name__ == '__main__':
    unittest.main()
