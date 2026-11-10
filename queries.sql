-- Student Performance Analysis
-- Table: students (created by run_analysis.py from StudentsPerformance.csv)
-- Columns: gender, race, parent_education, lunch, test_prep,
--          math_score, reading_score, writing_score, avg_score

-- Q0: Sanity check - how many rows, and the overall average?
SELECT COUNT(*) AS total_students,
       ROUND(AVG(avg_score), 2) AS overall_avg
FROM students;

-- Q1: Do students who completed the test prep course score higher?
SELECT test_prep,
       COUNT(*)                      AS students,
       ROUND(AVG(math_score), 1)     AS avg_math,
       ROUND(AVG(reading_score), 1)  AS avg_reading,
       ROUND(AVG(writing_score), 1)  AS avg_writing,
       ROUND(AVG(avg_score), 1)      AS avg_overall
FROM students
GROUP BY test_prep
ORDER BY avg_overall DESC;

-- Q2: Does parental education affect scores?
SELECT parent_education,
       COUNT(*)                  AS students,
       ROUND(AVG(avg_score), 1)  AS avg_overall
FROM students
GROUP BY parent_education
ORDER BY avg_overall DESC;

-- Q3: Grade bands (CASE) - how many students fall in each band?
SELECT CASE
         WHEN avg_score >= 90 THEN 'A (90+)'
         WHEN avg_score >= 80 THEN 'B (80-89)'
         WHEN avg_score >= 70 THEN 'C (70-79)'
         WHEN avg_score >= 60 THEN 'D (60-69)'
         ELSE 'F (<60)'
       END AS grade_band,
       COUNT(*) AS students
FROM students
GROUP BY grade_band
ORDER BY grade_band;

-- Q4: Grade bands split by test prep (does prep shift students into higher bands?)
SELECT test_prep,
       SUM(CASE WHEN avg_score >= 80 THEN 1 ELSE 0 END) AS a_or_b,
       SUM(CASE WHEN avg_score < 60  THEN 1 ELSE 0 END) AS failing,
       COUNT(*)                                         AS students
FROM students
GROUP BY test_prep;

-- Q5: Top 10 students by overall average
SELECT id, gender, parent_education, test_prep,
       math_score, reading_score, writing_score, avg_score
FROM students
ORDER BY avg_score DESC, id
LIMIT 10;

-- Q6: Filtering (WHERE) - prep students who scored 90+ in every subject
SELECT id, gender, parent_education, math_score, reading_score, writing_score
FROM students
WHERE test_prep = 'completed'
  AND math_score >= 90 AND reading_score >= 90 AND writing_score >= 90
ORDER BY avg_score DESC, id;
