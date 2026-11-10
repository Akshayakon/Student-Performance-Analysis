"""Load the CSV into SQLite, then run every query in queries.sql and print results."""
import csv
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
CSV_FILE = HERE / "StudentsPerformance.csv"
DB_FILE = HERE / "students.db"
SQL_FILE = HERE / "queries.sql"
OUT_FILE = HERE / "results.txt"


def load_data(conn):
    conn.execute("DROP TABLE IF EXISTS students")
    conn.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            gender TEXT, race TEXT, parent_education TEXT,
            lunch TEXT, test_prep TEXT,
            math_score INTEGER, reading_score INTEGER, writing_score INTEGER,
            avg_score REAL
        )""")
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            m, r, w = (int(row[k]) for k in ("math score", "reading score", "writing score"))
            conn.execute(
                "INSERT INTO students (gender, race, parent_education, lunch, test_prep,"
                " math_score, reading_score, writing_score, avg_score)"
                " VALUES (?,?,?,?,?,?,?,?,?)",
                (row["gender"], row["race/ethnicity"], row["parental level of education"],
                 row["lunch"], row["test preparation course"], m, r, w, round((m + r + w) / 3, 2)),
            )
    conn.commit()


def split_queries(text):
    """Split queries.sql into (title, sql) pairs using the '-- Qn:' comment lines."""
    blocks, title, lines = [], None, []
    for line in text.splitlines():
        if line.startswith("-- Q"):
            if title and lines:
                blocks.append((title, "\n".join(lines)))
            title, lines = line[3:].strip(), []
        elif title and not line.startswith("--"):
            lines.append(line)
    if title and lines:
        blocks.append((title, "\n".join(lines)))
    return blocks


def format_table(cols, rows):
    data = [cols] + [[str(v) for v in r] for r in rows]
    widths = [max(len(r[i]) for r in data) for i in range(len(cols))]
    fmt = lambda r: "  ".join(v.ljust(w) for v, w in zip(r, widths))
    return "\n".join([fmt(data[0]), "  ".join("-" * w for w in widths)] + [fmt(r) for r in data[1:]])


def main():
    conn = sqlite3.connect(DB_FILE)
    load_data(conn)
    out = []
    for title, sql in split_queries(SQL_FILE.read_text(encoding="utf-8")):
        cur = conn.execute(sql)
        cols = [d[0] for d in cur.description]
        out.append(f"{title}\n{format_table(cols, cur.fetchall())}\n")
    text = "\n".join(out)
    print(text)
    OUT_FILE.write_text(text, encoding="utf-8")
    conn.close()


if __name__ == "__main__":
    main()
