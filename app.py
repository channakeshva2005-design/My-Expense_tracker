from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database import get_connection

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# ---------------------------
# HOME - SERVE FRONTEND
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------------------
# GET ALL EXPENSES
# ---------------------------
@app.get("/expenses")
def get_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])

# ---------------------------
# ADD EXPENSE
# ---------------------------
@app.post("/expenses")
def add_expense():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (date, category, amount, description)
        VALUES (?, ?, ?, ?)
    """, (data["date"], data["category"], data["amount"], data["description"]))
    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added!"})

# ---------------------------
# DELETE EXPENSE
# ---------------------------
@app.delete("/expenses/<int:expense_id>")
def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Expense deleted!"})

# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
