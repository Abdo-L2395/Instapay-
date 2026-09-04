from validation import validate_username, validate_password, validate_phone

MAX_LOGIN_ATTEMPTS = 3


def find_user(users, username):
    """Return the user dict for a username, or None if not found."""
    return users.get(username)


def register(users):
    """Ask the user for registration details and add them to `users`."""
    print("\n===== Register =====")
    name = input("Full name: ").strip()

    while True:
        username = input("Choose a username: ").strip()
        ok, message = validate_username(username, users)
        if ok:
            break
        print(message)

    while True:
        phone = input("Phone number: ").strip()
        ok, message = validate_phone(phone)
        if ok:
            break
        print(message)

    while True:
        password = input("Choose a password (min 6 characters): ").strip()
        ok, message = validate_password(password)
        if ok:
            break
        print(message)

    users[username] = {
        "name": name,
        "phone": phone,
        "password": password,
        "balance": 0.0,
        "cards": [],
        "transactions": [],
        "daily_transfer_date": None,   # Bonus: supports the daily transfer limit
        "daily_transfer_total": 0.0
    }

    print(f"\nRegistration successful! Welcome, {name}.")
    return username


def login(users):
    """Ask for username/password. Returns the username on success, None on failure."""
    print("\n===== Login =====")
    attempts = 0

    while attempts < MAX_LOGIN_ATTEMPTS:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        user = find_user(users, username)
        if user is not None and user["password"] == password:
            print(f"\nLogin successful!\nWelcome {user['name']}")
            return username

        attempts += 1
        remaining = MAX_LOGIN_ATTEMPTS - attempts
        print("Invalid username or password.")
        if remaining > 0:
            print(f"Attempts remaining: {remaining}")

    print("\nToo many failed attempts. Returning to main menu.")
    return None


def change_password(users, username):
    """Bonus feature: let a logged-in user change their password."""
    user = users[username]
    current = input("Enter current password: ").strip()
    if current != user["password"]:
        print("Incorrect current password.")
        return

    new_password = input("Enter new password (min 6 characters): ").strip()
    ok, message = validate_password(new_password)
    if not ok:
        print(message)
        return

    user["password"] = new_password
    print("Password updated successfully!")
