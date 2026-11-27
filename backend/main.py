import sqlite3
from fastapi import FastAPI

app = FastAPI(title="CKD AI Backend")

def init_db():
    conn = sqlite3.connect("ckd_patients.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            blood_pressure REAL,
            glucose REAL,
            urea REAL,
            creatinine REAL,
            hemoglobin REAL,
            albumin REAL,
            sodium REAL,
            potassium REAL,
            wbc REAL,
            rbc REAL
        )
    """)

    conn.commit()
    conn.close()


init_db()
@app.get("/")
def home():
    return {
        "message": "CKD AI Backend is running!"
    }

from pydantic import BaseModel


class PatientData(BaseModel):
    name: str
    age: int
    gender: str
    blood_pressure: float
    glucose: float
    urea: float
    creatinine: float
    hemoglobin: float
    albumin: float
    sodium: float
    potassium: float
    wbc: float
    rbc: float





def init_db():
    conn = sqlite3.connect("ckd_patients.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            blood_pressure REAL,
            glucose REAL,
            urea REAL,
            creatinine REAL,
            hemoglobin REAL,
            albumin REAL,
            sodium REAL,
            potassium REAL,
            wbc REAL,
            rbc REAL
        )
    """)

    conn.commit()
    conn.close()


init_db()

@app.post("/patient")
def receive_patient(patient: PatientData):
    conn = sqlite3.connect("ckd_patients.db")

    cursor = conn.execute("""
        INSERT INTO patients (
            name, age, gender, blood_pressure, glucose,
            urea, creatinine, hemoglobin, albumin, sodium,
            potassium, wbc, rbc
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        patient.name,
        patient.age,
        patient.gender,
        patient.blood_pressure,
        patient.glucose,
        patient.urea,
        patient.creatinine,
        patient.hemoglobin,
        patient.albumin,
        patient.sodium,
        patient.potassium,
        patient.wbc,
        patient.rbc
    ))

    patient_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "message": "Patient data saved successfully!",
        "patient_id": patient_id
    }