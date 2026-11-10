# Student Performance Analysis

Simple SQL project on the Kaggle "Students Performance in Exams" dataset (1,000 rows).
SQL skills used: filtering (`WHERE`, Q6), `AVG`, `COUNT`, `GROUP BY`, `CASE` for grade bands.

## Files
| File | Purpose |
|---|---|
| `StudentsPerformance.csv` | Raw data |
| `queries.sql` | All SQL queries (Q0–Q6) |
| `run_analysis.py` | Loads CSV into SQLite (`students.db`), runs the queries, writes `results.txt` |
| `results.txt` | Query output |

## Run it
```
python run_analysis.py
```
Needs only Python 3 (sqlite3 is built in). `avg_score` = mean of math, reading, writing.

## Findings
1. **Test prep helps.** Completed: **72.7** avg vs none: **65.0** (+7.7). The gap shows up in all three subjects. 107 of 358 prep students (30%) scored 80+ vs 91 of 642 (14%) without prep. Only 17% of prep students averaged below 60, against 35% without prep.
2. **Parental education matters.** Average score rises steadily from **63.1** (high school) to **73.6** (master's degree), a gap of about 10 points.
3. **Top 10.** Three students scored a perfect 100 (IDs 459, 917, 963). Eight of the top 10 are female, and seven completed the prep course.

Caveat: these are correlations, not proof of cause. For example, students who choose prep may differ in other ways. `id` is just the CSV row order.
