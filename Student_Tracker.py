from  fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
app = FastAPI(title = "Study Group Tracker")

students: list[dict] = []


class StudentCreate(BaseModel):
    """What the client needs to send to us."""
    name: str = Field(min_length=2, max_length=60)
    email: EmailStr
    track: str = Field(default="backend")


@app.post("/Students", status_code=201)
def create_student(payload: StudentCreate):
    student_dict = payload.model_dump()

    student_dict["id"] = len(students) + 1

    students.append(student_dict)

    return student_dict


@app.get("/Students")
def get_students():
    return Students


@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(status_code=404, detail="Student not found")

class StudentUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=60)
    email: EmailStr
    track: str

@app.put("/students/{student_id}")
def update_student(student_id: int, payload: StudentUpdate):
    for student in students:
        if student["id"] == student_id:
            student.update(payload.model_dump())
            return student

    raise HTTPException(status_code=404, detail="Student not found")
    
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return {"message": "Student deleted successfully"}

    raise HTTPException(status_code=404, detail="Student not found")

