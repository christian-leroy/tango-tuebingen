import unittest
from cleanup import isOver
from ical_export import createLocation, createUid
from regular import nextDay
import datetime as dt



class TestIsOver(unittest.TestCase):
    def test_isOver(self):
        static_today = dt.date(2026, 7, 2)
        self.assertTrue(isOver("2026-07-01", static_today), "2026-07-01 is before 2026-07-02")
        self.assertFalse(isOver("2026-07-02", static_today), "2026-07-02 is NOT before 2026-07-02")

class TestCreateLocation(unittest.TestCase):
    def test_createLocation(self):
        test_milonga = {"venue": "Tanz-Atelier",
                        "street": "Provenceweg",
                        "house_number": "22",
                        "postal_code": "72072",
                        "city": "Tübingen"
                        }
        self.assertTrue(createLocation(test_milonga) == "Tanz-Atelier, Provenceweg 22, 72072 Tübingen")

class TestCreateUid(unittest.TestCase):
    def test_uid_has_no_spaces(self):
        test_milonga = {"title": "Eine Test-Milonga", "date": "2026-07-02"}
        self.assertTrue(createUid(test_milonga) == "2026-07-02-Eine-Test-Milonga@tangotuebingen.de")

    def test_uid_has_no_special_char(self):
        test_milonga = {"title": "!Eine Test-Milongä & Practica", "date": "2026-07-02"}
        self.assertTrue(createUid(test_milonga) == "2026-07-02-Eine-Test-Milong-Practica@tangotuebingen.de")

class TestCreateNext(unittest.TestCase):
    def testNextDay(self):
        self.assertTrue(nextDay(6,6) == 7) # Sunday to Sunday: 7 days
        self.assertTrue(nextDay(6,0) == 1) # Sunday to Monday: 1 day
        self.assertTrue(nextDay(6,5) == 6) # Sunday to Friday: 6 days 

        self.assertTrue(nextDay(0,0) == 7) # Monday to Monday: 7 days
        self.assertTrue(nextDay(0,1) == 1) # Monday to Tuesday: 1 day
        self.assertTrue(nextDay(1,0) == 6) # Monday to Sunday: 6 days

if __name__ == "__main__":
    unittest.main()
