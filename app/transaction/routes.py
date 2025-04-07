from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.transaction.models import Transaction
from datetime import datetime

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/')
def index():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    income = sum(t.amount for t in transactions if t.type == 'income')
    expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = income - expense
    month_year = datetime.now().strftime("%B %Y")
    return render_template('index.html', transactions=transactions, income_total=income, expense_total=expense, balance=balance, month_year=month_year)

@transaction_bp.route('/add', methods=['POST'])
def add_transaction():
    amount = float(request.form['amount'])
    description = request.form['description']
    t_type = request.form['type']
    date = datetime.now().date()  # default date to today

    new_txn = Transaction(date=date, amount=amount, description=description, type=t_type)
    db.session.add(new_txn)
    db.session.commit()
    return redirect(url_for('transaction.index'))

@transaction_bp.route('/delete/<int:txn_id>', methods=['POST'])
def delete_transaction(txn_id):
    txn = Transaction.query.get(txn_id)
    db.session.delete(txn)
    db.session.commit()
    return redirect(url_for('transaction.index'))
