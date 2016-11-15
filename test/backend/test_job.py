import unittest
import mist
import saliweb.test
import saliweb.backend
import os

class JobTests(saliweb.test.TestCase):
    """Check custom Job class"""

    def test_run_ok(self):
        """Test successful run method"""
        j = self.make_test_job(mist.Job, 'RUNNING')
        d = saliweb.test.RunInDir(j.directory)
        with open('param.txt', 'w') as fh:
            fh.write('csv\ntest@test.com\ntraining\nno_filtering\n')
        with open('input.txt', 'w') as fh:
            fh.write('SAV_STRAV;;2378;;3782;3990;2294;842;2739;1533;2938;1806;1686\n')
        cls = j._run_in_job_directory(j.run)
        self.assert_(isinstance(cls, saliweb.backend.SGERunner),
                     "SGERunner not returned")

if __name__ == '__main__':
    unittest.main()
