
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from app.models import User, HearingRecord
from app.routers.auth import get_current_user
from app.schemas.hearing import (
    HearingCreate,
    HearingUpdate,
    HearingResponse,
    HearingSummary,
)


router = APIRouter(
    prefix="/api/hearing",
    tags=["Hearing Records"],
)


@router.post(
    "/",
    response_model=HearingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_hearing_record(
    data: HearingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = HearingRecord(
        user_id=current_user.user_id,
        hearing_date=data.hearing_date,
        topic=data.topic,
        speaker_name=data.speaker_name,
        source=data.source,
        duration_minutes=data.duration_minutes,
        notes=data.notes,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@router.get(
    "/me",
    response_model=list[HearingResponse],
)
def get_my_hearing_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    records = (
        db.query(HearingRecord)
        .filter(HearingRecord.user_id == current_user.user_id)
        .order_by(
            HearingRecord.hearing_date.desc(),
            HearingRecord.hearing_id.desc(),
        )
        .all()
    )

    return records


@router.get(
    "/summary/me",
    response_model=HearingSummary,
)
def get_my_hearing_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = (
        db.query(
            func.count(HearingRecord.hearing_id),
            func.coalesce(func.sum(HearingRecord.duration_minutes), 0),
        )
        .filter(HearingRecord.user_id == current_user.user_id)
        .first()
    )

    total_sessions = int(result[0] or 0)
    total_minutes = int(result[1] or 0)

    return HearingSummary(
        total_sessions=total_sessions,
        total_hearing_minutes=total_minutes,
        total_hearing_hours=round(total_minutes / 60, 2),
    )


@router.get(
    "/{hearing_id}",
    response_model=HearingResponse,
)
def get_hearing_record(
    hearing_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(HearingRecord)
        .filter(
            HearingRecord.hearing_id == hearing_id,
            HearingRecord.user_id == current_user.user_id,
        )
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hearing record not found.",
        )

    return record


@router.put(
    "/{hearing_id}",
    response_model=HearingResponse,
)
def update_hearing_record(
    hearing_id: int,
    data: HearingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(HearingRecord)
        .filter(
            HearingRecord.hearing_id == hearing_id,
            HearingRecord.user_id == current_user.user_id,
        )
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hearing record not found.",
        )

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)

    return record
