import sqlite3

conn = sqlite3.connect("papers.db")
c = conn.cursor()

# 清空所有資料，但保留欄位
c.execute("DELETE FROM papers")
conn.commit()
conn.close()

print("資料表已清空！")
