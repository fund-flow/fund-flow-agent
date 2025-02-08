import unittest
from market_data import *

class TestGetRecommendation(unittest.TestCase):
    def test_get_market_data(self):

        market_data = get_market_data()
        print(market_data)

        self.assertIsInstance(market_data, dict)


if __name__ == "__main__":
    unittest.main()



# python -m unittest ./tests/test_market_data.py