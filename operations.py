
from datetime import date
from validation import validate_amount, validate_card_number, validate_cvv, validate_expiry

TRANSFER_FEE_RATE = 0.01      # Bonus: 1% fee on every transfer
DAILY_TRANSFER_LIMIT = 10000  # Bonus: max EGP a user can transfer out per day


def find_user_by_phone(users, phone):
    """Bonus helper: look up a username by phone number."""
    for username, data in users.items():
        if data["phone"] == phone:
            return username
    return None


def _next_transaction_id(user):
    """Bonus: simple incrementing transaction ID, unique per user."""
    return len(user["transactions"]) + 1


def _record_transaction(user, tx_type, amount, detail=""):
    transaction = {
        "id": _next_transaction_id(user),
        "type": tx_type,
        "amount": amount,
        "detail": detail
    }
    user["transactions"].append(transaction)


def show_balance(user):
    print(f"\nCurrent Balance: {user['balance']:.2f} EGP")


def link_card(user):
    print("\n===== Link Visa Card =====")

    while True:
        card_number = input("Card number (16 digits): ").strip()
        ok, message = validate_card_number(card_number)
        if ok:
            break
        print(message)

    holder_name = input("Card holder name: ").strip()

    while True:
        expiry = input("Expiry date (MM/YY): ").strip()
        ok, message = validate_expiry(expiry)
        if ok:
            break
        print(message)

    while True:
        cvv = input("CVV (3 digits): ").strip()
        ok, message = validate_cvv(cvv)
        if ok:
            break
        print(message)

    # Card is stored, but the CVV is deliberately never saved or displayed.
    user["cards"].append({
    "number": card_number,
    "holder_name": holder_name,
    "expiry": expiry
     })
    print("\nCard linked successfully!")


def remove_card(user):
    """Bonus feature: unlink the currently linked card."""
    if user["cards"] is None:
        print("No card is linked.")
        return
    for i, card in enumerate(user["cards"], 1):
     print(i, card["number"])
    card_index = int(input("Select a card to remove: "))
    if 1 <= card_index <= len(user["cards"]):
     user["cards"].pop(card_index - 1)
     print("Card removed successfully.")
    else:
     print("Invalid card selection.")


def deposit(user):
    print("\n===== Deposit =====")
    amount_str = input("Enter amount: ").strip()
    ok, result = validate_amount(amount_str)
    if not ok:
        print(f"\nInvalid amount.\n{result}")
        return

    amount = result
    user["balance"] += amount
    _record_transaction(user, "Deposit", amount)
    print(f"\nDeposit successful!\nNew Balance: {user['balance']:.2f} EGP")


def withdraw(user):
    print("\n===== Withdraw =====")
    amount_str = input("Enter amount: ").strip()
    ok, result = validate_amount(amount_str)
    if not ok:
        print(f"\nInvalid amount.\n{result}")
        return

    amount = result
    if amount > user["balance"]:
        print("\nInsufficient balance. You cannot withdraw more than you have.")
        return

    user["balance"] -= amount
    _record_transaction(user, "Withdraw", amount)
    print(f"\nWithdrawal successful!\nRemaining Balance: {user['balance']:.2f} EGP")


def _get_daily_transferred(user):
    """Bonus: returns how much the user has transferred out today (resets on a new day)."""
    today = date.today().isoformat()
    if user.get("daily_transfer_date") != today:
        user["daily_transfer_date"] = today
        user["daily_transfer_total"] = 0.0
    return user["daily_transfer_total"]


def transfer(users, username, user):
    print("\n===== Transfer =====")
    recipient_input = input("Recipient (username or phone number): ").strip()

    # Bonus: allow finding the recipient by phone number as well as username.
    if recipient_input in users:
        recipient_username = recipient_input
    else:
        recipient_username = find_user_by_phone(users, recipient_input)

    if recipient_username is None:
        print("\nRecipient not found.")
        return

    if recipient_username == username:
        print("\nYou cannot transfer money to yourself.")
        return

    recipient = users[recipient_username]

    amount_str = input("Amount: ").strip()
    ok, result = validate_amount(amount_str)
    if not ok:
        print(f"\nInvalid amount.\n{result}")
        return

    amount = result
    fee = round(amount * TRANSFER_FEE_RATE, 2)
    total_deduction = amount + fee

    if total_deduction > user["balance"]:
        print(f"\nInsufficient balance. This transfer needs {total_deduction:.2f} EGP (including a {fee:.2f} EGP fee).")
        return

    # Bonus: enforce a daily transfer limit.
    already_transferred = _get_daily_transferred(user)
    if already_transferred + amount > DAILY_TRANSFER_LIMIT:
        remaining = DAILY_TRANSFER_LIMIT - already_transferred
        print(f"\nDaily transfer limit exceeded. You can still transfer up to {remaining:.2f} EGP today.")
        return

    confirm = input(
        f"\nConfirm transfer of {amount:.2f} EGP to {recipient_username} "
        f"(+ {fee:.2f} EGP fee, total {total_deduction:.2f} EGP)? (yes/no): "
    ).strip().lower()
    if confirm != "yes":
        print("Transfer cancelled.")
        return

    user["balance"] -= total_deduction
    recipient["balance"] += amount
    user["daily_transfer_total"] = already_transferred + amount

    _record_transaction(user, "Transfer", amount, detail=f"to {recipient_username}, fee {fee:.2f} EGP")
    _record_transaction(recipient, "Transfer In", amount, detail=f"from {username}")

    print(f"\nTransfer successful!\nYour new balance: {user['balance']:.2f} EGP")


def show_transactions(user, limit=None):
    """Prints transaction history. Pass limit=5 to show only the last 5 (bonus)."""
    print("\n===== Transaction History =====\n")
    transactions = user["transactions"]

    if not transactions:
        print("No transactions yet.")
        return

    if limit is not None:
        transactions = transactions[-limit:]

    for tx in transactions:
        sign = "+" if tx["type"] in ("Deposit", "Transfer In") else "-"
        detail = f" ({tx['detail']})" if tx["detail"] else ""
        print(f"{tx['id']}. {tx['type']:<12} {sign}{tx['amount']:.2f} EGP{detail}")


def search_transactions(user):
    """Bonus feature: search transaction history by type keyword."""
    keyword = input("Search by transaction type (e.g. Deposit, Withdraw, Transfer): ").strip().lower()
    matches = [tx for tx in user["transactions"] if keyword in tx["type"].lower()]

    print(f"\n===== Search Results for '{keyword}' =====\n")
    if not matches:
        print("No matching transactions found.")
        return

    for tx in matches:
        detail = f" ({tx['detail']})" if tx["detail"] else ""
        print(f"{tx['id']}. {tx['type']:<12} {tx['amount']:.2f} EGP{detail}")
