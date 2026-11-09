
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from app.models import User
from app.models.models import BookReading
from app.routers.auth import get_current_user
from app.schemas.reading import (
    ReadingCreate,
    ReadingUpdate,
    ReadingResponse,
)


router = APIRouter(
    prefix="/api/reading",
    tags=["Book Reading"],
)


@router.post(
    "/",
    response_model=ReadingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_reading_record(
    data: ReadingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = BookReading(
        user_id=current_user.user_id,
        reading_date=data.reading_date,
        book_title=data.book_title.strip(),
        pages_read=data.pages_read,
        reading_minutes=data.reading_minutes,
        notes=data.notes,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@router.get(
    "/me",
    response_model=list[ReadingResponse],
)
def get_my_reading_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    records = (
        db.query(BookReading)
        .filter(BookReading.user_id == current_user.user_id)
        .order_by(
            BookReading.reading_date.desc(),
            BookReading.reading_id.desc(),
        )
        .all()
    )

    return records


@router.get(
    "/{reading_id}",
    response_model=ReadingResponse,
)
def get_reading_record(
    reading_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(BookReading)
        .filter(
            BookReading.reading_id == reading_id,
            BookReading.user_id == current_user.user_id,
        )
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book reading record not found.",
        )

    return record


@router.put(
    "/{reading_id}",
    response_model=ReadingResponse,
)
def update_reading_record(
    reading_id: int,
    data: ReadingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(BookReading)
        .filter(
            BookReading.reading_id == reading_id,
            BookReading.user_id == current_user.user_id,
        )
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book reading record not found.",
        )

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)

    return record
