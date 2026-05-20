from sqlalchemy.orm import Session
from backend.models.patient import Patient


def create_patient(
    db: Session,
    name: str,
    discharge_summary: str,
    risk_level: str
):
    patient = Patient(
        name=name,
        discharge_summary=discharge_summary,
        risk_level=risk_level
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


def get_patients(db: Session):
    return db.query(Patient).order_by(Patient.id.desc()).all()


def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()
