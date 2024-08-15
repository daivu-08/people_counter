import sqlite3

conn = sqlite3.connect('people_count.db')
c = conn.cursor()

c.execute("SELECT * FROM individuals ORDER BY last_seen DESC")
rows = c.fetchall()

print("All entries:")
for row in rows:
    print(f"ID: {row[0]}, First seen: {row[1]}, Last seen: {row[2]}")

conn.close()