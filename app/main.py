from fastapi import FastAPI
from app.routers import grades, students

app = FastAPI(title="Ecom tech API", description="API for Ecom tech application")

app.include_router(grades.router, prefix="/grades", tags=["grades"])
app.include_router(students.router, prefix="/students", tags=["students"])

@app.get("/health")
def health_check():
    return {"status": "ok"}