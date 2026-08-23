from  fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
app = FastAPI(title = "Study Group Tracker")

students: list[dict] = []


class StudentCreate(BaseModel):
    """What the client needs to send to us."""
    name: str = Field(min_length=2, max_length=60)
    email: EmailStr
    track: str = Field(default="backend")

class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    track: str


@app.post("/students", status_code=201, response_model=StudentResponse)
def create_student(payload: StudentCreate):
    student_dict = payload.model_dump()

    student_dict["id"] = len(students) + 1

    students.append(student_dict)

    return student_dict


@app.get("/students", response_model=list[StudentResponse])
def get_students(track: str | None = None, name: str | None=None):
    if track:
        return [students for students in students if students["track"]==track]
    if name:
        return [students for students in students if name.lower() in students["name"].lower()]    
    return students


@app.get("/students/{student_id}", response_model= StudentResponse)
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(status_code=404, detail="Student not found")

class StudentUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=60)
    email: EmailStr
    track: str


@app.put("/students/{student_id}",response_model=StudentResponse)
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

