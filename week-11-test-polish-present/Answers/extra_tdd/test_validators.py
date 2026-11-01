"""Run from this folder:  python3 -m unittest test_validators -v"""
import unittest

from validators import validate_booking


class TestName(unittest.TestCase):
    def test_name_length_boundaries(self):
        for name, ok in [("A", False), ("Al", True), ("A" * 40, True), ("A" * 41, False)]:
            with self.subTest(name=name):
                self.assertEqual("name" in validate_booking(name, "1", 5), not ok)

    def test_spaces_are_trimmed_before_checking(self):
        self.assertIn("name", validate_booking("   ", "1", 5))
        self.assertIn("name", validate_booking(" A ", "1", 5))
        self.assertNotIn("name", validate_booking(" Al ", "1", 5))

    def test_missing_name(self):
        self.assertIn("name", validate_booking(None, "1", 5))
        self.assertIn("name", validate_booking("", "1", 5))


class TestSeats(unittest.TestCase):
    def test_boundaries(self):
        self.assertIn("seats", validate_booking("Mei", "0", 5))          # one below the minimum
        self.assertNotIn("seats", validate_booking("Mei", "1", 5))       # the minimum
        self.assertNotIn("seats", validate_booking("Mei", "5", 5))       # exactly what is available
        self.assertIn("seats", validate_booking("Mei", "6", 5))          # one too many

    def test_not_a_whole_number(self):
        for bad in ("abc", "1.5", "-2", "", " ", "1 OR 1=1", None):
            with self.subTest(seats=bad):
                self.assertIn("seats", validate_booking("Mei", bad, 5))

    def test_message_mentions_how_many_are_left(self):
        self.assertEqual(validate_booking("Mei", "6", 5)["seats"], "Only 5 seats left.")
        self.assertEqual(validate_booking("Mei", "2", 1)["seats"], "Only 1 seat left.")

    def test_nothing_available(self):
        self.assertIn("seats", validate_booking("Mei", "1", 0))


class TestWholeBooking(unittest.TestCase):
    def test_valid_booking_has_no_errors(self):
        self.assertEqual(validate_booking("Mei Lin", "2", 5), {})

    def test_all_errors_are_reported_together(self):
        self.assertEqual(set(validate_booking("", "abc", 5)), {"name", "seats"})

    def test_order_of_checks_does_not_change_the_result(self):
        """Because each field is checked independently, re-ordering the code cannot change the answer."""
        self.assertEqual(validate_booking("M", "99", 5).keys(), {"name": 1, "seats": 1}.keys())


if __name__ == "__main__":
    unittest.main()
