from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(20), default=datetime.now().strftime('%Y-%m-%d'))

@app.route('/')
def index():
    transactions = Transaction.query.all()
    income_total = sum(txn.amount for txn in transactions if txn.type == 'income')
    expense_total = sum(txn.amount for txn in transactions if txn.type == 'expense')
    return render_template('index.html',
                           transactions=transactions,
                           income_total=income_total,
                           expense_total=expense_total,
                           month_year=datetime.now().strftime('%B %Y'))

@app.route('/add', methods=['POST'])
def add():
    description = request.form['description']
    amount = float(request.form['amount'])
    txn_type = request.form['type']
    txn = Transaction(description=description, amount=amount, type=txn_type)
    db.session.add(txn)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    txn = Transaction.query.get_or_404(id)
    db.session.delete(txn)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    txn = Transaction.query.get_or_404(id)
    if request.method == 'POST':
        txn.description = request.form['description']
        txn.amount = float(request.form['amount'])
        txn.type = request.form['type']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', txn=txn)

# ✅ Export to CSV route
@app.route('/export')
def export():
    transactions = Transaction.query.all()

    # create in-memory text stream for CSV
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['ID', 'Date', 'Description', 'Amount', 'Type'])

    # Write data rows
    for txn in transactions:
        writer.writerow([txn.id, txn.date, txn.description, txn.amount, txn.type])

    # Prepare response
    output.seek(0)
    return Response(output.getvalue(),
                    mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=transactions.csv"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
