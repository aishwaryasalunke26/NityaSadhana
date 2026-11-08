
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
from app.models import User
from app.models.models import JapaRecord
from app.routers.auth import get_current_user

from app.schemas.japa import (
    JapaCreate,
    JapaUpdate,
    JapaResponse,
)


router = APIRouter(
    prefix="/api/japa",
    tags=["Japa Tracking"]
)


# 1. CREATE JAPA RECORD
@router.post(
    "/",
    response_model=JapaResponse,
    status_code=status.HTTP_201_CREATED
)
def create_japa_record(
    data: JapaCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    existing_record = db.query(JapaRecord).filter(
        JapaRecord.user_id == current_user.user_id,
        JapaRecord.record_date == data.record_date
    ).first()

    if existing_record:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Japa record already exists for this date."
        )

    record = JapaRecord(
        user_id=current_user.user_id,
        record_date=data.record_date,
        rounds_completed=data.rounds_completed,
        notes=data.notes
    )

    try:
        db.add(record)
        db.commit()
        db.refresh(record)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Japa record already exists for this date."
        )

    return record


# 2. VIEW MY JAPA HISTORY
@router.get(
    "/me",
    response_model=list[JapaResponse]
)
def get_my_japa_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    records = db.query(JapaRecord).filter(
        JapaRecord.user_id == current_user.user_id
    ).order_by(
        JapaRecord.record_date.desc()
    ).all()

    return records


# 3. VIEW ONE JAPA RECORD
@router.get(
    "/{japa_id}",
    response_model=JapaResponse
)
def get_japa_record(
    japa_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    record = db.query(JapaRecord).filter(
        JapaRecord.japa_id == japa_id,
        JapaRecord.user_id == current_user.user_id
    ).first()

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Japa record not found."
        )

    return record


# 4. UPDATE JAPA RECORD
@router.put(
    "/{japa_id}",
    response_model=JapaResponse
)
def update_japa_record(
    japa_id: int,
    data: JapaUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    record = db.query(JapaRecord).filter(
        JapaRecord.japa_id == japa_id,
        JapaRecord.user_id == current_user.user_id
    ).first()

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Japa record not found."
        )

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(record, field, value)

    try:
        db.commit()
        db.refresh(record)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A Japa record already exists for this date."
        )

    return record
