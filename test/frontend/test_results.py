import unittest
import saliweb.test
import re

# Import the mist frontend with mocks
mist = saliweb.test.import_mocked_frontend("mist", __file__,
                                           '../../frontend')


class Tests(saliweb.test.TestCase):
    """Check results page"""

    def test_results_file(self):
        """Test download of results files"""
        with saliweb.test.make_frontend_job('testjob') as j:
            j.make_file('MistOutput.txt')
            c = mist.app.test_client()
            rv = c.get('/job/testjob/MistOutput.txt?passwd=%s' % j.passwd)
            self.assertEqual(rv.status_code, 200)

    def test_ok_job(self):
        """Test display of OK job"""
        with saliweb.test.make_frontend_job('testjob2') as j:
            j.make_file('MistOutput.txt')
            c = mist.app.test_client()
            for endpoint in ('job', 'results.cgi'):
                rv = c.get('/%s/testjob2?passwd=%s' % (endpoint, j.passwd))
                r = re.compile(b'Job.*testjob.*has completed.*Download.*'
                               b'MistOutput\\.txt.*MiST output',
                               re.MULTILINE | re.DOTALL)
                self.assertRegex(rv.data, r)

    def test_failed_job(self):
        """Test display of failed job"""
        with saliweb.test.make_frontend_job('testjob3') as j:
            c = mist.app.test_client()
            rv = c.get('/job/testjob3?passwd=%s' % j.passwd)
            r = re.compile(
                b'Your MiST job.*testjob.*failed to produce any ranking.*'
                b'please see the.*#errors.*help page.*For more information, '
                b'you can.*framework\\.log.*download the MiST file-check log.*'
                b'contact us', re.MULTILINE | re.DOTALL)
            self.assertRegex(rv.data, r)


if __name__ == '__main__':
    unittest.main()
