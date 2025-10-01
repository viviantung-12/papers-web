from flask import Flask, render_template, request, jsonify
import sqlite3, os

app = Flask(__name__)
DB_PATH = os.path.join(os.getcwd(), "papers.db")

# 初始化資料庫
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            link TEXT,
            abstract TEXT,
            tags TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 首頁
@app.route("/")
def index():
    return render_template("index.html")

# 取得所有論文
@app.route("/api/papers")
def api_get_papers():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, author, year, link, abstract, tags FROM papers ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    papers = [
        {"id": r[0], "title": r[1], "author": r[2], "year": r[3],
         "link": r[4], "abstract": r[5], "tags": r[6]}
        for r in rows
    ]
    return jsonify(papers)

# 新增論文
@app.route("/api/add", methods=["POST"])
def api_add():
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO papers (title, author, year, link, abstract, tags) VALUES (?, ?, ?, ?, ?, ?)",
        (data["title"], data["author"], data.get("year"),
         data.get("link"), data.get("abstract"), data.get("tags"))
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# 刪除單筆論文
@app.route("/api/delete/<int:paper_id>", methods=["DELETE"])
def api_delete(paper_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM papers WHERE id = ?", (paper_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))