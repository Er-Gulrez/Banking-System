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

# User model - for login
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    # One-to-one relationship with profile
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade="all, delete")

# UserProfile model - for additional details
class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(150), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)

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
    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    balance = session.pop("last_balance", None)
    action = session.pop("last_action", None)

    return render_template("transaction.html", balance=balance, action=action)

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

    return redirect(url_for("dashboard"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"]
        dob = datetime.strptime(request.form["dob"], "%Y-%m-%d")
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        username_error = email_error = None

        # Check for existing username
        if User.query.filter_by(username=username).first():
            username_error = "Username is already taken"

        # Check for existing email
        if UserProfile.query.filter_by(email=email).first():
            email_error = "Email is already registered"

        # If either error exists, return form with messages
        if username_error or email_error:
            return render_template(
                "register.html",
                username_error=username_error,
                email_error=email_error,
                form_data=request.form
            )

        # Otherwise, create new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.flush()

        new_profile = UserProfile(
            user_id=new_user.id,
            full_name=full_name,
            dob=dob,
            email=email
        )
        db.session.add(new_profile)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
