from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "papers.db"

# 初始化資料庫（如果不存在就建立）
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            year TEXT,
            tags TEXT
        )
        """)
        conn.commit()
        conn.close()

init_db()

# 取得所有論文
@app.route("/get_papers")
def get_papers():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM papers")
    papers = c.fetchall()
    conn.close()
    return jsonify([{"id": p[0], "title": p[1], "author": p[2], "year": p[3], "tags": p[4]} for p in papers])

# 新增論文
@app.route("/add_paper", methods=["POST"])
def add_paper():
    data = request.get_json()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO papers (title, author, year, tags) VALUES (?, ?, ?, ?)",
              (data["title"], data["author"], data["year"], data.get("tags","")))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# 刪除論文
@app.route("/delete_paper", methods=["POST"])
def delete_paper():
    data = request.get_json()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM papers WHERE id = ?", (data["id"],))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
