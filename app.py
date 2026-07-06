from flask import Flask, request, redirect, session, render_template
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret_key"

def get_db():
    return psycopg2.connect(
        host="db",
        database="appdb",
        user="appuser",
        password="apppass"
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(100) UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)

    default_email = "admin@test.com"
    default_password = generate_password_hash("admin123")

    cur.execute("""
        INSERT INTO users (email, password)
        VALUES (%s, %s)
        ON CONFLICT (email) DO NOTHING;
    """, (default_email, default_password))

    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    if "email" not in session:
        return redirect("/login")
    return render_template("home.html", email=session["email"])

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[0], password):
            session["email"] = email
            return redirect("/")

        error = "Email ou mot de passe incorrect"

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
