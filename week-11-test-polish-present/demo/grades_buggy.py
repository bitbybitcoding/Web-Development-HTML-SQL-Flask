"""THE SAME MODULE WITH TWO BOUNDARY BUGS. Copy it over grades.py to watch the tests catch them, then fix it."""


def grade(score):
    """Return the grade for a score from 0 to 100.

    A: 75 and above    B: 65 to 74    C: 55 to 64    D: 45 to 54    F: below 45
    Raises ValueError for anything that is not a whole number from 0 to 100.
    """
    if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 100:
        raise ValueError("score must be a whole number from 0 to 100")
    if score >= 75:
        return "A"
    if score > 65:
        return "B"
    if score >= 55:
        return "C"
    if score > 45:
        return "D"
    return "F"


def average(scores):
    """Average of the scores that are not None (None means absent). Returns None if there are none."""
    present = [s for s in scores if s is not None]
    if not present:
        return None
    return round(sum(present) / len(present), 1)
