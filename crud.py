from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# -----------------------------
# Pydantic Model
# -----------------------------

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    city: str


# -----------------------------
# Temporary Database
# -----------------------------

patients = {
    1: {
        "name": "Shubham",
        "age": 23,
        "gender": "male",
        "city": "Noida"
    },
    2: {
        "name": "Varun",
        "age": 25,
        "gender": "male",
        "city": "Delhi"
    }
}


# =============================
# CREATE
# =============================

@app.post("/patients")
def create_patient(patient: Patient):

    new_id = max(patients.keys(), default=0) + 1

    patients[new_id] = patient.model_dump()

    return {
        "message": "Patient created successfully",
        "patient_id": new_id,
        "data": patients[new_id]
    }


# =============================
# READ ALL
# =============================

@app.get("/patients")
def get_all_patients():

    return patients


# =============================
# READ ONE
# =============================

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):

    if patient_id not in patients:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patients[patient_id]


# =============================
# UPDATE
# =============================

@app.put("/patients/{patient_id}")
def update_patient(
    patient_id: int,
    patient: Patient
):

    if patient_id not in patients:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    patients[patient_id] = patient.model_dump()

    return {
        "message": "Patient updated successfully",
        "data": patients[patient_id]
    }


# =============================
# DELETE
# =============================

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):

    if patient_id not in patients:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    deleted_patient = patients.pop(patient_id)

    return {
        "message": "Patient deleted successfully",
        "data": deleted_patient
    }