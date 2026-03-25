import unittest
from cleanup import isOver
from export_to_ical import createLocation, createUid
from generate_events import daysUntilWeekday
import datetime as dt


class TestCleanup(unittest.TestCase):
    """Class for testing cleanup.py"""
    def test_isOver(self):
        static_today = dt.date(2026, 7, 2)
        self.assertEqual(isOver("2026-07-01", static_today), True, "2026-07-01 is before 2026-07-02")
        self.assertEqual(isOver("2026-07-02", static_today), False, "2026-07-02 is NOT before 2026-07-02")


class TestExportToIcal(unittest.TestCase):
    """Class for testing export_to_ical.py"""
    def test_createLocation(self):
        test_milonga = {"venue": "Tanz-Atelier",
                        "street": "Provenceweg",
                        "house_number": "22",
                        "postal_code": "72072",
                        "city": "Tübingen"
                        }
        self.assertEqual(createLocation(test_milonga), "Tanz-Atelier, Provenceweg 22, 72072 Tübingen")

    def test_uid_has_no_spaces(self):
        test_milonga = {"title": "Eine Test-Milonga", "date": "2026-07-02"}
        self.assertEqual(createUid(test_milonga), "2026-07-02-Eine-Test-Milonga@tangotuebingen.de")

    def test_uid_has_no_special_char(self):
        test_milonga = {"title": "!Eine Test-Milongä & Practica", "date": "2026-07-02"}
        self.assertEqual(createUid(test_milonga), "2026-07-02-Eine-Test-Milong-Practica@tangotuebingen.de")


class TestGenerateEvents(unittest.TestCase):
    """Class for testing generate_events.py"""
    def testNextDay(self):
        self.assertEqual(daysUntilWeekday(6,6), 7) # Sunday to Sunday: 7 days
        self.assertEqual(daysUntilWeekday(6,0), 1) # Sunday to Monday: 1 day
        self.assertEqual(daysUntilWeekday(6,5), 6) # Sunday to Friday: 6 days

        self.assertEqual(daysUntilWeekday(0,0), 7) # Monday to Monday: 7 days
        self.assertEqual(daysUntilWeekday(0,1), 1) # Monday to Tuesday: 1 day
        self.assertEqual(daysUntilWeekday(1,0), 6) # Monday to Sunday: 6 days


if __name__ == "__main__":
    unittest.main()