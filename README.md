# InstaPay Simulation System

A comprehensive CLI-based payment application in Python simulating digital wallet and instant transfer features (inspired by InstaPay). It includes user authentication, card linking, deposit/withdrawal operations, peer-to-peer transfers with fees and daily limits, transaction histories, and transaction searching.

---

## 📋 Table of Contents
- [Features](#features)
- [Project Architecture](#project-architecture)
- [Modules Overview](#modules-overview)
- [Getting Started](#getting-started)
- [Usage & Menu Flow](#usage--menu-flow)
- [Key Business Logic & Validations](#key-business-logic--validations)

---

## ✨ Features

- **User Authentication**:
  - Secure registration with full name, unique username, 11-digit Egyptian phone number, and password validation.
  - Login authentication with a maximum of **3 failed attempts**.
  - Password change functionality for active user sessions.
- **Card Management**:
  - Link Visa cards with validation for card number (16 digits), expiry date (`MM/YY`), and CVV (3 digits).
  - Unlink/remove linked cards.
  - **PCI-DSS Compliance Principle**: CVV is validated during input but **never stored or displayed** in the system.
- **Financial Operations**:
  - View real-time account balance.
  - Deposit funds into account.
  - Withdraw funds (with insufficient balance protection).
  - Transfer money via **Username** or **Phone Number**.
  - **1% Transfer Fee** automatically calculated and applied.
  - **10,000 EGP Daily Transfer Limit** (auto-resets daily).
- **Transaction Tracking**:
  - Detailed transaction history (view all or limit to last 5 transactions).
  - Incremental, unique transaction IDs per user.
  - Keyword search through transaction history.

---

## 🏗 Project Architecture

```
.
├── main.py          # Entry point and menu navigation loops
├── auth.py          # Registration, login, and password management
├── operations.py    # Core financial transactions & card operations
└── validation.py    # Input validation logic (cards, passwords, phone, amounts)
```

---

## 🧩 Modules Overview

### 1. `main.py`
Contains the application loop and interactive menu system:
- `welcome_menu()`: Entry menu for Register, Login, or Exit.
- `main_menu()`: Navigation options for authenticated users.
- `run_session()`: Manages user action dispatching during a logged-in session.
- `main()`: Primary loop directing the application flow.

### 2. `auth.py`
Handles user account lifecycles:
- `register(users)`: Collects and validates new user information and creates user state dictionaries.
- `login(users)`: Authenticates credentials with a 3-try lockout rule.
- `change_password(users, username)`: Enables active users to safely update their password.

### 3. `operations.py`
Implements core business logic and financial transactions:
- `show_balance(user)`: Displays current account balance in EGP.
- `link_card(user)` & `remove_card(user)`: Adds or removes bank cards from user profile.
- `deposit(user)` & `withdraw(user)`: Modifies user account balance and logs transactions.
- `transfer(users, username, user)`: Handles peer-to-peer money transfer, validates daily limits, applies a 1% fee, and creates dual transaction records (sender & receiver).
- `show_transactions(user, limit)`: Displays recent transactions formatted with signs (`+` / `-`) and detail tags.
- `search_transactions(user)`: Filters transactions based on user-entered keywords.

### 4. `validation.py`
Helper functions for input sanitization and verification:
- `validate_username()`: Ensures non-empty and non-duplicate usernames.
- `validate_password()`: Enforces minimum length of 6 characters.
- `validate_phone()`: Ensures an 11-digit number starting with `01`.
- `validate_amount()`: Ensures positive numeric inputs.
- `validate_card_number()`, `validate_cvv()`, `validate_expiry()`: Validates standard payment card format.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher (No external dependencies required; uses pure standard Python libraries).

### Running the Application

Execute the main file from your terminal:

```bash
python main.py
```

---

## 🎮 Usage & Menu Flow

### Welcome Screen
```text
===== InstaPay =====
1. Register
2. Login
3. Exit
```

### Main Application Menu
```text
===== Main Menu =====
1. View Balance
2. Link Card
3. Deposit
4. Withdraw
5. Transfer
6. Transaction History (last 5)
7. Search Transactions
8. Change Password
9. Remove Card
10. Logout
```

---

## ⚙️ Key Business Logic & Validations

| Feature | Logic / Rule |
| :--- | :--- |
| **Transfer Fee Rate** | `1%` (`0.01`) calculated on transfer amount. Total deduction = `Amount + Fee`. |
| **Daily Transfer Limit** | Maximum transfer out limit of `10,000.00 EGP` per day. Resets automatically based on `date.today()`. |
| **Phone Number** | Must be exactly 11 numeric digits starting with `01` (e.g., `01012345678`). |
| **Card Number** | Exactly 16 numeric digits. |
| **Card Expiry** | `MM/YY` format with valid month (`01`-`12`). |
| **CVV** | 3 numeric digits. **Never stored** in user objects for security. |
