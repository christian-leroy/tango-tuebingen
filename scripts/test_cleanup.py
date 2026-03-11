import unittest
from cleanup import isOver
import datetime as dt


class TestIsOver(unittest.TestCase):
    def test_isOver(self):
        static_today = dt.date(2026, 7, 2)
        self.assertTrue(isOver("2026-07-01", static_today), "2026-07-01 is before 2026-07-02")
        self.assertFalse(isOver("2026-07-02", static_today), "2026-07-02 is NOT before 2026-07-02")

if __name__ == "__main__":
    unittest.main()
