from auth import register, login, change_password
from operations import (
    show_balance, link_card, remove_card, deposit, withdraw,
    transfer, show_transactions, search_transactions
)

users = {}


def welcome_menu():
    print("\n===== InstaPay =====")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    return input("Choose: ").strip()


def main_menu():
    print("\n===== Main Menu =====")
    print("1. View Balance")
    print("2. Link Card")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Transfer")
    print("6. Transaction History (last 5)")
    print("7. Search Transactions")
    print("8. Change Password")
    print("9. Remove Card")
    print("10. Logout")
    return input("Choose: ").strip()


def run_session(username):
    """Runs the logged-in menu loop for a single user session."""
    user = users[username]

    while True:
        choice = main_menu()

        if choice == "1":
            show_balance(user)
        elif choice == "2":
            link_card(user)
        elif choice == "3":
            deposit(user)
        elif choice == "4":
            withdraw(user)
        elif choice == "5":
            transfer(users, username, user)
        elif choice == "6":
            show_transactions(user, limit=5)
        elif choice == "7":
            search_transactions(user)
        elif choice == "8":
            change_password(users, username)
        elif choice == "9":
            remove_card(user)
        elif choice == "10":
            print("\nLogged out successfully.")
            break
        else:
            print("\nInvalid choice. Please try again.")


def main():
    print("Welcome to InstaPay Simulation!")

    while True:
        choice = welcome_menu()

        if choice == "1":
            register(users)
        elif choice == "2":
            username = login(users)
            if username is not None:
                run_session(username)
        elif choice == "3":
            print("\nThank you for using InstaPay. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
