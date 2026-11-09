
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database import get_db
from app.models import User
from app.models.models import SevaRecord
from app.routers.auth import get_current_user
from app.schemas.seva import SevaCreate, SevaUpdate, SevaResponse


router = APIRouter(
    prefix="/api/seva",
    tags=["Seva Records"]
)


# CREATE SEVA RECORD
@router.post(
    "/",
    response_model=SevaResponse,
    status_code=status.HTTP_201_CREATED
)
def create_seva_record(
    data: SevaCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = SevaRecord(
        user_id=current_user.user_id,
        seva_date=data.seva_date,
        seva_type=data.seva_type,
        description=data.description,
        duration_minutes=data.duration_minutes
    )

    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to create seva record."
        )


# GET ALL MY SEVA RECORDS
@router.get("/me", response_model=list[SevaResponse])
def get_my_seva_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return (
        db.query(SevaRecord)
        .filter(SevaRecord.user_id == current_user.user_id)
        .order_by(
            SevaRecord.seva_date.desc(),
            SevaRecord.seva_id.desc()
        )
        .all()
    )


# GET SINGLE SEVA RECORD
@router.get("/{seva_id}", response_model=SevaResponse)
def get_seva_record(
    seva_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = (
        db.query(SevaRecord)
        .filter(
            SevaRecord.seva_id == seva_id,
            SevaRecord.user_id == current_user.user_id
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Seva record not found."
        )

    return record


# UPDATE SEVA RECORD
@router.put("/{seva_id}", response_model=SevaResponse)
def update_seva_record(
    seva_id: int,
    data: SevaUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = (
        db.query(SevaRecord)
        .filter(
            SevaRecord.seva_id == seva_id,
            SevaRecord.user_id == current_user.user_id
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Seva record not found."
        )

    try:
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(record, key, value)

        db.commit()
        db.refresh(record)
        return record

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to update seva record."
        )


# DELETE SEVA RECORD
@router.delete("/{seva_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_seva_record(
    seva_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = (
        db.query(SevaRecord)
        .filter(
            SevaRecord.seva_id == seva_id,
            SevaRecord.user_id == current_user.user_id
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Seva record not found."
        )

    try:
        db.delete(record)
        db.commit()
        return None

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to delete seva record."
        )
