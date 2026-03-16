import csv
import io
from datetime import datetime
from fastapi import APIRouter, HTTPException, UploadFile, File
from psycopg2.extras import execute_values
from app.db import get_db_connection

router = APIRouter()


@router.post("/upload-grades", status_code=201)
def upload_grades(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Поддерживаются только файлы CSV.")

    # UploadFile.read() — асинхронный, используем file.file — синхронный BinaryIO.
    csv_text = file.file.read().decode("utf-8-sig")  # Учитываем возможную BOM в начале файла

    if not csv_text.strip():
        raise HTTPException(status_code=400, detail="Файл пустой.")

    reader = csv.reader(io.StringIO(csv_text), delimiter=';')
    rows = list(reader)

    header = [col.strip() for col in rows[0]]
    expected_header = ["Дата", "Номер группы", "ФИО", "Оценка"]
    if header != expected_header:
        raise HTTPException(
            status_code=400,
            detail=f"Неверный заголовок. Ожидается: {expected_header}, получено: {header}"
        )

    records = []

    for i, row in enumerate(rows[1:], start=2):
        if len(row) != 4:
            raise HTTPException(
                status_code=400,
                detail=f"Строка {i}: неверное количество столбцов (ожидается 4, получено {len(row)})"
            )

        date_str, group_number, full_name, grade_str = [col.strip() for col in row]

        if not full_name:
            raise HTTPException(status_code=400, detail=f"Строка {i}: пустое ФИО")

        try:
            grade = int(grade_str)
            if grade not in (2, 3, 4, 5):
                raise ValueError
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Строка {i}: оценка должна быть числом 2, 3, 4 или 5, получено '{grade_str}'"
            )

        try:
            grade_date = datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Строка {i}: неверная дата '{date_str}', ожидаемый формат ДД.ММ.ГГГГ"
            )

        records.append((full_name, group_number, grade_date, grade))

    if not records:
        raise HTTPException(status_code=400, detail="Нет валидных записей для загрузки.")

    students_count = len(set((r[0], r[1]) for r in records))

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            execute_values(cur, """
                INSERT INTO students (full_name, group_name)
                VALUES %s
                ON CONFLICT (full_name, group_name) DO NOTHING
            """, [(r[0], r[1]) for r in records])

            cur.execute("SELECT id, full_name, group_name FROM students")
            student_map = {
                (row[1], row[2]): row[0] for row in cur.fetchall()
            }

            execute_values(cur, """
                INSERT INTO grades (student_id, grade_date, grade)
                VALUES %s
            """, [(student_map[(r[0], r[1])], r[2], r[3]) for r in records])

            conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении данных: {str(e)}")

    finally:
        conn.close()

    return {
        "status": "ok",
        "records_loaded": len(records),
        "students": students_count,
    }