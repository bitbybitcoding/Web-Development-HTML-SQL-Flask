"""Run:  python3 -m unittest test_grades -v      (from the demo folder)"""
import unittest

from grades import average, grade


class TestGrade(unittest.TestCase):
    def test_typical_scores(self):
        self.assertEqual(grade(90), "A")
        self.assertEqual(grade(70), "B")
        self.assertEqual(grade(60), "C")
        self.assertEqual(grade(50), "D")
        self.assertEqual(grade(20), "F")

    def test_boundaries(self):
        """Bugs hide on the boundaries: test the number on each side of every change."""
        for score, expected in [(100, "A"), (75, "A"), (74, "B"), (65, "B"), (64, "C"),
                                (55, "C"), (54, "D"), (45, "D"), (44, "F"), (0, "F")]:
            with self.subTest(score=score):
                self.assertEqual(grade(score), expected)

    def test_invalid_scores_are_rejected(self):
        for bad in (-1, 101, 55.5, "80", None, True):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    grade(bad)


class TestAverage(unittest.TestCase):
    def test_ignores_absent_scores(self):
        self.assertEqual(average([80, None, 60]), 70.0)

    def test_rounds_to_one_decimal_place(self):
        self.assertEqual(average([1, 2, 2]), 1.7)

    def test_nobody_present_is_none_not_an_error(self):
        self.assertIsNone(average([]))
        self.assertIsNone(average([None, None]))


if __name__ == "__main__":
    unittest.main()
