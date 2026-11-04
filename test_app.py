import unittest
from app import app


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_hello(self):
        response = self.client.get('/hello?name=TEST')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, TEST!', response.data)

    def test_hello_sin_nombre(self):
        response = self.client.get('/hello')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, None!', response.data)


if __name__ == '__main__':
    unittest.main()