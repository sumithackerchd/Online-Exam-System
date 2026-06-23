import os
import sqlite3

from flask import Flask, render_template, request, redirect, session

print("Current Folder:", os.getcwd())

app = Flask(__name__)

app.secret_key = "exam_secret_key"


# Home Page

@app.route("/")
def home():
    return render_template("index.html")


# Admin Login

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["admin"] = True

            return redirect("/")

    return render_template("admin_login.html")


# Logout

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/admin")


# Add Question

@app.route("/add_question", methods=["GET", "POST"])
def add_question():

    if "admin" not in session:
        return redirect("/admin")

    if request.method == "POST":

        question = request.form["question"]
        option1 = request.form["option1"]
        option2 = request.form["option2"]
        option3 = request.form["option3"]
        option4 = request.form["option4"]
        answer = request.form["answer"]

        conn = sqlite3.connect("exam.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO questions
            (question, option1, option2, option3, option4, answer)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (question, option1, option2, option3, option4, answer)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_question.html")


# Start Exam

@app.route("/exam")
def exam():

    conn = sqlite3.connect("exam.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions")

    questions = cursor.fetchall()

    conn.close()

    return render_template(
        "exam.html",
        questions=questions
    )


# Result

@app.route("/result", methods=["POST"])
def result():

    conn = sqlite3.connect("exam.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions")

    questions = cursor.fetchall()

    conn.close()

    score = 0
    total = len(questions)

    for q in questions:

        selected_answer = request.form.get(f"q{q[0]}")

        if selected_answer == q[6]:
            score += 1

    return render_template(
        "result.html",
        score=score,
        total=total
    )


# View Questions

@app.route("/questions")
def questions():

    if "admin" not in session:
        return redirect("/admin")

    conn = sqlite3.connect("exam.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions")

    all_questions = cursor.fetchall()

    conn.close()

    return render_template(
        "view_questions.html",
        questions=all_questions
    )


# Delete Question

@app.route("/delete/<int:id>")
def delete_question(id):

    if "admin" not in session:
        return redirect("/admin")

    conn = sqlite3.connect("exam.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM questions WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/questions")


if __name__ == "__main__":
    app.run(debug=True, port=5004)