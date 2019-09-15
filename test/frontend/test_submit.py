import unittest
import saliweb.test
import os
import re

# Import the mist frontend with mocks
mist = saliweb.test.import_mocked_frontend("mist", __file__,
                                           '../../frontend')


class Tests(saliweb.test.TestCase):
    """Check submit page"""

    def test_submit_page(self):
        """Test submit page"""
        incoming = saliweb.test.TempDir()
        mist.app.config['DIRECTORIES_INCOMING'] = incoming.tmpdir
        c = mist.app.test_client()
        rv = c.post('/job')
        self.assertEqual(rv.status_code, 400)  # no input table
        self.assertIn(b'Please upload input table', rv.data)

        t = saliweb.test.TempDir()
        inf = os.path.join(t.tmpdir, 'inf.txt')
        with open(inf, 'w') as fh:
            fh.write("test")

        rv = c.post('/job', data={'input_file':open(inf, 'rb'),
                                  'running_mode': 'garbage'})
        self.assertEqual(rv.status_code, 400)  # bad running mode
        self.assertIn(b"Invalid value 'garbage' for running mode; should "
                      b"be one of 'training', 'trained'.".replace(b"'",
                                                                  b"&#39;"),
                      rv.data)

        rv = c.post('/job', data={'input_file':open(inf, 'rb'),
                                  'running_mode': 'training',
                                  'filtering_mode': 'garbage'})
        self.assertEqual(rv.status_code, 400)  # bad filtering mode
        self.assertIn(b"Invalid value 'garbage' for filtering mode; should "
                      b"be one of 'filtering', "
                      b"'no_filtering'.".replace(b"'", b"&#39;"), rv.data)

        # Successful submission (no email)
        rv = c.post('/job', data={'input_file':open(inf, 'rb'),
                                  'running_mode': 'training',
                                  'filtering_mode': 'filtering'})
        self.assertEqual(rv.status_code, 200)
        r = re.compile(b'Your job .*has been submitted.*Results will be '
                       b'found at', re.MULTILINE | re.DOTALL)
        self.assertRegexpMatches(rv.data, r)

        # Successful submission (with email)
        rv = c.post('/job', data={'input_file':open(inf, 'rb'),
                                  'running_mode': 'training',
                                  'filtering_mode': 'filtering',
                                  'email': 'test@test.com'})
        self.assertEqual(rv.status_code, 200)
        r = re.compile(b'Your job .*has been submitted.*Results will be '
                       b'found at.*You will be notified at',
                       re.MULTILINE | re.DOTALL)
        self.assertRegexpMatches(rv.data, r)


if __name__ == '__main__':
    unittest.main()
