from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = 'trades.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                horario TEXT,
                par TEXT,
                direcao TEXT,
                valor REAL,
                payout INTEGER,
                resultado TEXT,
                lucro REAL,
                observacoes TEXT
            )
        """)

@app.route('/')
def index():
    with sqlite3.connect(DB) as conn:
        trades = conn.execute("SELECT * FROM trades").fetchall()
        total_lucro = conn.execute("SELECT SUM(lucro) FROM trades").fetchone()[0] or 0.0
    return render_template("index.html", trades=trades, total_lucro=total_lucro)

@app.route('/adicionar', methods=["POST"])
def adicionar():
    dados = (
        request.form["data"],
        request.form["horario"],
        request.form["par"],
        request.form["direcao"],
        float(request.form["valor"]),
        int(request.form["payout"]),
        request.form["resultado"],
        float(request.form["lucro"]),
        request.form["observacoes"]
    )
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO trades (data, horario, par, direcao, valor, payout, resultado, lucro, observacoes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", dados)
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)
