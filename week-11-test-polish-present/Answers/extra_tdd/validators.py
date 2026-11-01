"""Extra practice 1: validate_booking, written after the tests (test-driven development)."""


def validate_booking(name, seats, available):
    """Return a dict of field -> error message. An empty dict means the booking is valid."""
    errors = {}

    name = (name or "").strip()
    if not 2 <= len(name) <= 40:
        errors["name"] = "Name must be 2 to 40 characters."

    seats = (seats or "").strip()
    if not seats.isdigit() or int(seats) < 1:         # "abc", "1.5", "-2", "" and "0" all fail here
        errors["seats"] = "Seats must be a whole number of at least 1."
    elif int(seats) > available:
        errors["seats"] = f"Only {available} seat{'s' if available != 1 else ''} left."

    return errors
