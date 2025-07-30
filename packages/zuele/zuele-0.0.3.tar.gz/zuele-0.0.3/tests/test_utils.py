# test/test_utils.py

import unittest
from zuele.utils import add

class TestAddFunction(unittest.TestCase):
    def test_add(self):
        result = add(3, 5)
        self.assertEqual(result, 8, "加法函数测试失败")

if __name__ == "__main__":
    unittest.main()