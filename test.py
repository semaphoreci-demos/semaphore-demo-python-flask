from semaphoreflask import app
import unittest

class TaskTest(unittest.TestCase):

    def test_homepage(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        response = tester.get('/task/all', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        
if __name__ == '__main__':
    unittest.main()