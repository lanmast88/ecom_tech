from fastapi import APIRouter, HTTPException
from app.db import get_db_connection

router = APIRouter()

@router.get("/students/more-than-3-twos")
def more_than_3_twos():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT full_name, COUNT(*) AS count_twos
                FROM grades
                JOIN students ON grades.student_id = students.id
                WHERE grade = 2
                GROUP BY full_name
                HAVING COUNT(*) > 3
            """)
            results = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")
    finally:
        conn.close()
    
    return [{"full_name": row[0], "count_twos": row[1]} for row in results]

@router.get("/students/less-than-5-twos")
def less_than_5_twos():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT full_name, COUNT(*) AS count_twos
                FROM grades
                JOIN students ON grades.student_id = students.id
                WHERE grade = 2
                GROUP BY full_name
                HAVING COUNT(*) < 5
            """)
            results = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении данных: {str(e)}")
    finally:
        conn.close()
    
    return [{"full_name": row[0], "count_twos": row[1]} for row in results]