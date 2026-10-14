from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..models.schemas import Hospital
from ..services.db_service import db
from ..services.escrow_service import escrow_service

router = APIRouter(prefix="/api/hospitals", tags=["Hospitals & Escrow"])

@router.get("", response_model=List[Hospital])
def list_hospitals():
    return db.get_hospitals()

@router.get("/{hospital_id}", response_model=Hospital)
def get_hospital(hospital_id: str):
    hosp = db.get_hospital(hospital_id)
    if not hosp:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hosp

@router.get("/{hospital_id}/escrow-ledger")
def get_hospital_escrow_ledger(hospital_id: str):
    return escrow_service.generate_hospital_escrow_audit_trail(hospital_id)
