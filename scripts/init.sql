CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    group_name VARCHAR(4) NOT NULL,
    UNIQUE (full_name, group_name)
);

CREATE TABLE IF NOT EXISTS grades (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    grade_date DATE NOT NULL,
    grade SMALLINT NOT NULL CHECK (grade IN (2, 3, 4, 5))
);

CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id);
CREATE INDEX IF NOT EXISTS idx_grades_grade ON grades(grade);