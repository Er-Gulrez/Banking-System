from flask import Flask, request, render_template
import Banking_System
app = Flask(__name__)

bank = Banking_System.Banking_System()

@app.route("/")
def home():
    return render_template("index.html", balance = None)

@app.route("/process", methods=["Post"])
def credit():
    amount = int(request.form.get("amount"))
    action = request.form.get("action")
    
    if action == "credit":
        bank.credit(amount)
    
    elif action == "debit":
        bank.debit(amount)

    return render_template("index.html", balance = bank.balance, action = action)

if __name__ == "__main__":
    app.run(debug = True)