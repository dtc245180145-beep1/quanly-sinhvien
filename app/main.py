
import os
import logging

import pymysql
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-only-change-this")
logging.basicConfig(level=logging.INFO)


def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "student_app"),
        password=os.getenv("DB_PASSWORD", "change_this_password"),
        database=os.getenv("DB_NAME", "student_management"),
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
        charset="utf8mb4"
    )


@app.route("/")
def index():
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.id, s.student_code, s.full_name, s.email,
                       s.class_id, c.class_name
                FROM students s
                LEFT JOIN classes c ON s.class_id = c.id
                ORDER BY s.id DESC
            """)
            students = cursor.fetchall()

            cursor.execute("SELECT id, class_name FROM classes ORDER BY class_name")
            classes = cursor.fetchall()

        return render_template(
            "index.html",
            students=students,
            classes=classes,
            editing=None
        )
    except Exception:
        app.logger.exception("Không thể tải danh sách sinh viên")
        return "Không thể kết nối hoặc truy vấn cơ sở dữ liệu.", 503
    finally:
        if connection:
            connection.close()


@app.route("/students/add", methods=["POST"])
def add_student():
    student_code = request.form.get("student_code", "").strip()
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    class_id = request.form.get("class_id", "").strip()

    if not student_code or not full_name:
        flash("Mã sinh viên và họ tên là bắt buộc.")
        return redirect(url_for("index"))

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO students (student_code, full_name, email, class_id)
                VALUES (%s, %s, %s, %s)
            """, (
                student_code,
                full_name,
                email or None,
                int(class_id) if class_id else None
            ))
        connection.commit()
        flash("Thêm sinh viên thành công.")
    except pymysql.err.IntegrityError:
        if connection:
            connection.rollback()
        flash("Mã sinh viên đã tồn tại hoặc dữ liệu không hợp lệ.")
    except Exception:
        if connection:
            connection.rollback()
        app.logger.exception("Lỗi khi thêm sinh viên")
        flash("Không thể thêm sinh viên.")
    finally:
        if connection:
            connection.close()

    return redirect(url_for("index"))


@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
def edit_student(student_id):
    connection = None
    try:
        connection = get_db_connection()

        if request.method == "POST":
            student_code = request.form.get("student_code", "").strip()
            full_name = request.form.get("full_name", "").strip()
            email = request.form.get("email", "").strip()
            class_id = request.form.get("class_id", "").strip()

            if not student_code or not full_name:
                flash("Mã sinh viên và họ tên là bắt buộc.")
                return redirect(url_for("edit_student", student_id=student_id))

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE students
                    SET student_code=%s, full_name=%s, email=%s, class_id=%s
                    WHERE id=%s
                """, (
                    student_code,
                    full_name,
                    email or None,
                    int(class_id) if class_id else None,
                    student_id
                ))
            connection.commit()
            flash("Cập nhật sinh viên thành công.")
            return redirect(url_for("index"))

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students WHERE id=%s", (student_id,))
            editing = cursor.fetchone()

            cursor.execute("SELECT id, class_name FROM classes ORDER BY class_name")
            classes = cursor.fetchall()

            cursor.execute("""
                SELECT s.id, s.student_code, s.full_name, s.email,
                       s.class_id, c.class_name
                FROM students s
                LEFT JOIN classes c ON s.class_id = c.id
                ORDER BY s.id DESC
            """)
            students = cursor.fetchall()

        if not editing:
            return "Không tìm thấy sinh viên.", 404

        return render_template(
            "index.html",
            students=students,
            classes=classes,
            editing=editing
        )
    except pymysql.err.IntegrityError:
        if connection:
            connection.rollback()
        flash("Mã sinh viên đã tồn tại hoặc dữ liệu không hợp lệ.")
        return redirect(url_for("edit_student", student_id=student_id))
    except Exception:
        if connection:
            connection.rollback()
        app.logger.exception("Lỗi khi sửa sinh viên")
        return "Không thể xử lý yêu cầu.", 500
    finally:
        if connection:
            connection.close()


@app.route("/students/<int:student_id>/delete", methods=["POST"])
def delete_student(student_id):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
        connection.commit()
        flash("Đã xóa sinh viên.")
    except pymysql.err.IntegrityError:
        if connection:
            connection.rollback()
        flash("Không thể xóa sinh viên vì vẫn còn dữ liệu điểm liên quan.")
    except Exception:
        if connection:
            connection.rollback()
        app.logger.exception("Lỗi khi xóa sinh viên")
        flash("Không thể xóa sinh viên.")
    finally:
        if connection:
            connection.close()

    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

