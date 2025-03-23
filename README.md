# Flask Banking System

A simple yet functional web-based banking application built with Flask that simulates core banking operations including account creation, money transfers, deposits, and withdrawals.

![Banking System Demo](https://github.com/lodwickmasete/wick-banking-system/raw/main/screenshots/Screenshot_20250323_221526_Chrome.jpg)

![Banking System Demo](https://github.com/lodwickmasete/wick-banking-system/raw/main/screenshots/Screenshot_20250323_221602_Chrome.jpg)
## Features

- **Account Management**
  - Create accounts with a 4-digit PIN
  - Secure login system
  - View account dashboard with current balance

- **Transaction Capabilities**
  - Deposit funds
  - Withdraw funds (with PIN verification)
  - Transfer money between accounts
  - View transaction history and statements

- **Security**
  - PIN verification for sensitive operations
  - Session management
  - Proper error handling

- **Data Persistence**
  - All bank data is saved using Python's pickle module
  - Automatic data saving after critical operations

## Technologies Used

- Python 3.x
- Flask web framework
- Bootstrap 5 for responsive UI
- Pickle for data persistence

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/lodwickmasete/wick-banking-system.git
   cd wick-backing-system
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install flask
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000/`

## Usage Guide

### Creating a New Account
1. Click on "Create Account" from the homepage
2. Enter your full name
3. Create a 4-digit PIN (must be exactly 4 digits)
4. Enter an initial deposit amount
5. Your account number will be generated automatically

### Logging In
1. Click on "Login" from the homepage
2. Enter your account number and PIN
3. Upon successful login, you'll be redirected to your dashboard

### Making Transactions
From the dashboard, you can:

- **Deposit**: Add money to your account
- **Withdraw**: Remove money (requires PIN verification)
- **Transfer**: Send money to another account (requires recipient account number and PIN verification)
- **View Statement**: See all your transaction history

## Project Structure

```
wick-banking-system/
├── app.py                  # Main application file
├── bank_data.pkl           # Persisted bank data
├── templates/              # HTML templates
│   ├── base.html           # Base template with common elements
│   ├── index.html          # Homepage
│   ├── create_account.html # Account creation form
│   ├── login.html          # Login form
│   ├── dashboard.html      # User dashboard
│   ├── deposit.html        # Deposit form
│   ├── withdraw.html       # Withdrawal form
│   ├── transfer.html       # Transfer form
│   └── statement.html      # Transaction history
└── README.md               # This file
```

## Security Notes

This application is designed for educational purposes and demonstrates basic banking operations. In a production environment, you would want to implement:

- HTTPS for secure communication
- More robust authentication mechanisms
- Database encryption
- Input validation and sanitization
- Protection against CSRF and other web vulnerabilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask documentation
- Bootstrap for the responsive UI components
