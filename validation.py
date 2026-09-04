def validate_username(username, users):
    """A username is valid if it's not empty and not already taken."""
    if not username or not username.strip():
        return False, "Username cannot be empty."
    if username in users:
        return False, "Username already exists. Choose another one."
    return True, ""


def validate_password(password):
    """Password must be at least 6 characters long."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    return True, ""


def validate_phone(phone):
    """Simple phone check: 11 digits, must start with '01'."""
    if len(phone) == 11 and phone.isdigit() and phone.startswith("01"):
        return True, ""
    return False, "Phone number must be 11 digits and start with '01'."


def validate_amount(amount_str):
    """Amount must be a number greater than zero.

    Returns (True, amount_as_float) on success,
    or (False, error_message) on failure.
    """
    try:
        amount = float(amount_str)
    except ValueError:
        return False, "Amount must be a number."
    if amount <= 0:
        return False, "Amount must be greater than 0."
    return True, amount


def validate_card_number(card_number):
    """Card number must be exactly 16 digits."""
    if len(card_number) == 16 and card_number.isdigit():
        return True, ""
    return False, "Card number must be 16 digits."


def validate_cvv(cvv):
    """CVV must be exactly 3 digits."""
    if len(cvv) == 3 and cvv.isdigit():
        return True, ""
    return False, "CVV must be 3 digits."


def validate_expiry(expiry):
    """Expiry date must look like MM/YY with a valid month."""
    parts = expiry.split("/")
    if len(parts) != 2:
        return False, "Expiry date must be in MM/YY format."

    month, year = parts
    if not (month.isdigit() and year.isdigit()):
        return False, "Expiry date must be in MM/YY format."
    if not (1 <= int(month) <= 12):
        return False, "Month must be between 01 and 12."
    if len(year) != 2:
        return False, "Year must be 2 digits (e.g. 27)."
    return True, ""
