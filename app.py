from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from Banking_System import Banking_System

app = Flask(__name__)
app.secret_key = 'g#rD8fN1@T2k!x9L'  # Needed to use sessions

# 💾 MySQL config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Monu10111%40@localhost/bankdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 📦 Database Models
class User(db.Model):
    __tablename__ = 'users'  # 🔥 explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Transaction(db.Model):
    __tablename__ = 'transactions'  # 👈 add this line
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(10))
    amount = db.Column(db.Float)
    balance_before = db.Column(db.Float)
    balance_after = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# 🧪 Initial route
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    balance = session.pop("last_balance", None)
    action = session.pop("last_action", None)

    return render_template("index.html", balance=balance, action=action)

# 🔁 Processing credit/debit
@app.route("/process", methods=["POST"])
def process():
    if "user_id" not in session:
        return redirect(url_for("login"))

    amount = float(request.form.get("amount"))
    action = request.form.get("action")
    user = User.query.get(session["user_id"])

    # Get last balance
    last_txn = Transaction.query.filter_by(user_id=user.id).order_by(Transaction.id.desc()).first()
    current_balance = last_txn.balance_after if last_txn else 0
    bank = Banking_System(current_balance)

    try:
        if action == "credit":
            updated_balance = bank.credit(amount)
        elif action == "debit":
            updated_balance = bank.debit(amount)
        else:
            return "Invalid action", 400
    except ValueError as e:
        return str(e), 400

    txn = Transaction(
        user_id=user.id,
        action=action,
        amount=amount,
        balance_before=current_balance,
        balance_after=updated_balance
    )
    db.session.add(txn)
    db.session.commit()

    # Save data in session for GET display
    session["last_balance"] = updated_balance
    session["last_action"] = action

    return redirect(url_for("home"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
