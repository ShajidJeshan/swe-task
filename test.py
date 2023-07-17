import unittest
from main import app


class TestDataAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_add_data(self):
        data = "1649941817 Voltage 1.34\n1649941818 Voltage 1.35\n1649941817 Current 12.0\n1649941818 Current 14.0"
        response = self.app.post('/data', headers={'Content-Type': 'text/plain'}, data=data)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_add_malformed_data(self):
        data = "1649941817 Voltage 1.34\n1649941818 1.35 Voltage"
        response = self.app.post('/data', headers={'Content-Type': 'text/plain'}, data=data)
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])

    def test_get_data(self):
        response = self.app.get('/data?from=2022-04-14&to=2022-04-15')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['data'], list)
        self.assertIsInstance(data['avg_power_per_day'], list)


if __name__ == '__main__':
    unittest.main()
