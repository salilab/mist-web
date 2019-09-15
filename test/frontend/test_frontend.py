import unittest
import saliweb.test

# Import the mist frontend with mocks
mist = saliweb.test.import_mocked_frontend("mist", __file__,
                                           '../../frontend')


class Tests(saliweb.test.TestCase):

    def test_index(self):
        """Test index page"""
        c = mist.app.test_client()
        rv = c.get('/')
        self.assertIn(b'MiST is a computational tool for scoring', rv.data)
        self.assertIn(b'S. Jaeger, P. Cimermancic, et al.', rv.data)

    def test_contact(self):
        """Test contact page"""
        c = mist.app.test_client()
        rv = c.get('/contact')
        self.assertIn(b'Please address inquiries to', rv.data)

    def test_help(self):
        """Test help page"""
        c = mist.app.test_client()
        rv = c.get('/help')
        self.assertIn(b'Upload input interaction table', rv.data)

    def test_queue(self):
        """Test queue page"""
        c = mist.app.test_client()
        rv = c.get('/job')
        self.assertIn(b'No pending or running jobs', rv.data)


if __name__ == '__main__':
    unittest.main()
