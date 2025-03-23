import random
from datetime import datetime
import json
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle

app = Flask(__name__)
app.secret_key = os.urandom(24)

# File to store bank data
BANK_DATA_FILE = 'bank_data.pkl'

class Account:
    def __init__(self, name, pin, initial_deposit):
        self.account_number = self.generate_account_number()
        self.name = name
        self.balance = initial_deposit
        self.pin = pin
        self.transactions = []
        self.add_transaction("Account opened", initial_deposit)

    def generate_account_number(self):
        return str(random.randint(10**9, 10**10-1))  # 10-digit account number

    def add_transaction(self, transaction_type, amount):
        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": transaction_type,
            "amount": amount,
            "balance": self.balance
        }
        self.transactions.append(transaction)

    def deposit(self, amount):
        self.balance += amount
        self.add_transaction("Deposit", amount)
        return self.balance

    def withdraw(self, amount, pin):
        if pin != self.pin:
            return "Invalid PIN"
        if amount > self.balance:
            return "Insufficient funds"
        self.balance -= amount
        self.add_transaction("Withdrawal", -amount)
        return self.balance

    def get_statement(self):
        return self.transactions


class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, name, pin, initial_deposit):
        if len(pin) != 4 or not pin.isdigit():
            return "PIN must be 4 digits"
        if initial_deposit < 0:
            return "Initial deposit must be positive"
        account = Account(name, pin, initial_deposit)
        self.accounts[account.account_number] = account
        self.save_data()  # Save after creating an account
        return account.account_number

    def transfer(self, from_acc, to_acc, amount, pin):
        if from_acc not in self.accounts or to_acc not in self.accounts:
            return "Invalid account number"
        if self.accounts[from_acc].pin != pin:
            return "Invalid PIN"
        if self.accounts[from_acc].balance < amount:
            return "Insufficient funds"
        
        self.accounts[from_acc].balance -= amount
        self.accounts[to_acc].balance += amount
        
        self.accounts[from_acc].add_transaction(f"Transfer to {to_acc}", -amount)
        self.accounts[to_acc].add_transaction(f"Transfer from {from_acc}", amount)
        
        self.save_data()  # Save after transfer
        return "Transfer successful"
    
    def save_data(self):
        """Save bank data to file using pickle"""
        with open(BANK_DATA_FILE, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load_data():
        """Load bank data from file, or create a new Bank if file doesn't exist"""
        if os.path.exists(BANK_DATA_FILE):
            try:
                with open(BANK_DATA_FILE, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading bank data: {e}")
                return Bank()
        else:
            return Bank()


# Initialize the bank by loading from file if it exists
bank = Bank.load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form['name']
        pin = request.form['pin']
        initial_deposit = float(request.form['initial_deposit'])
        
        result = bank.create_account(name, pin, initial_deposit)
        
        if isinstance(result, str) and (result.startswith("PIN") or result.startswith("Initial")):
            flash(result, 'error')
            return redirect(url_for('create_account'))
        
        flash(f'Account created successfully! Your account number is: {result}', 'success')
        return redirect(url_for('index'))
    
    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account_number = request.form['account_number']
        pin = request.form['pin']
        
        if account_number in bank.accounts and bank.accounts[account_number].pin == pin:
            session['account_number'] = account_number
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid account number or PIN', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('account_number', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'account_number' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    account = bank.accounts[session['account_number']]
    return render_template('dashboard.html', account=account)

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if 'account_number' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        amount = float(request.form['amount'])
        if amount <= 0:
            flash('Amount must be positive', 'error')
        else:
            account = bank.accounts[session['account_number']]
            new_balance = account.deposit(amount)
            bank.save_data()  # Save after deposit
            flash(f'Deposit successful! New balance: ${new_balance:.2f}', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if 'account_number' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        amount = float(request.form['amount'])
        pin = request.form['pin']
        
        if amount <= 0:
            flash('Amount must be positive', 'error')
        else:
            account = bank.accounts[session['account_number']]
            result = account.withdraw(amount, pin)
            
            if isinstance(result, float):
                bank.save_data()  # Save after successful withdrawal
                flash(f'Withdrawal successful! New balance: ${result:.2f}', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash(result, 'error')
    
    return render_template('withdraw.html')

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'account_number' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        to_account = request.form['to_account']
        amount = float(request.form['amount'])
        pin = request.form['pin']
        
        result = bank.transfer(session['account_number'], to_account, amount, pin)
        
        if result == "Transfer successful":
            flash('Transfer completed successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(result, 'error')
    
    return render_template('transfer.html')

@app.route('/statement')
def statement():
    if 'account_number' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    account = bank.accounts[session['account_number']]
    transactions = account.get_statement()
    
    return render_template('statement.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
