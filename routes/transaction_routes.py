from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from models import Transaction

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/add-transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        user_email = request.form['email']
        amount = float(request.form['amount'])
        category = request.form['category']
        type_ = request.form['type']
        description = request.form['description']

        transaction = Transaction(
            user_email=user_email,
            amount=amount,
            category=category,
            type=type_,
            description=description
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transaction.view_transactions'))

    return render_template('add_transaction.html')

@transaction_bp.route('/transactions')
def view_transactions():
    all_transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template('view_transactions.html', transactions=all_transactions)
