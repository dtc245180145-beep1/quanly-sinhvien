CREATE DATABASE IF NOT EXISTS student_management
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE student_management;

CREATE TABLE IF NOT EXISTS classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_code VARCHAR(30) NOT NULL UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150),
    class_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_student_class
        FOREIGN KEY (class_id) REFERENCES classes(id)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    score DECIMAL(4,2) NOT NULL,
    CONSTRAINT chk_score CHECK (score >= 0 AND score <= 10),
    CONSTRAINT fk_grade_student
        FOREIGN KEY (student_id) REFERENCES students(id)
        ON DELETE CASCADE
);

INSERT IGNORE INTO classes (class_name, description)
VALUES
    ('CNTT-K20A', 'Lớp Công nghệ thông tin'),
    ('CNTT-K20B', 'Lớp Công nghệ thông tin B');

INSERT IGNORE INTO students (student_code, full_name, email, class_id)
VALUES
    ('SV001', 'Nguyen Van An', 'an@example.com', 1),
    ('SV002', 'Tran Thi Binh', 'binh@example.com', 2);

INSERT INTO grades (student_id, subject_name, score)
SELECT s.id, 'Co so du lieu', 8.50
FROM students s
WHERE s.student_code = 'SV001'
AND NOT EXISTS (
    SELECT 1 FROM grades g
    WHERE g.student_id = s.id
    AND g.subject_name = 'Co so du lieu'
);
