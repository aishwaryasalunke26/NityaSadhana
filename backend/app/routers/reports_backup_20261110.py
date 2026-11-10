
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database import get_db
from app.models import User
from app.models.models import DailyReport
from app.routers.auth import get_current_user

from app.schemas.reports import (
    DailyReportCreate,
    DailyReportUpdate,
    DailyReportResponse
)


router = APIRouter(
    prefix="/api/reports",
    tags=["Daily Reports"]
)


# CREATE DAILY REPORT
@router.post(
    "/",
    response_model=DailyReportResponse,
    status_code=status.HTTP_201_CREATED
)
def create_daily_report(
    data: DailyReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = DailyReport(
        user_id=current_user.user_id,
        report_date=data.report_date,
        reflection=data.reflection,
        gratitude=data.gratitude,
        challenges=data.challenges
    )

    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A daily report already exists for this date."
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to create daily report."
        )


# GET ALL MY DAILY REPORTS
@router.get("/me", response_model=list[DailyReportResponse])
def get_my_daily_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return (
        db.query(DailyReport)
        .filter(DailyReport.user_id == current_user.user_id)
        .order_by(
            DailyReport.report_date.desc(),
            DailyReport.report_id.desc()
        )
        .all()
    )


# GET SINGLE DAILY REPORT
@router.get("/{report_id}", response_model=DailyReportResponse)
def get_daily_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = (
        db.query(DailyReport)
        .filter(
            DailyReport.report_id == report_id,
            DailyReport.user_id == current_user.user_id
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Daily report not found."
        )

    return record


# UPDATE DAILY REPORT
@router.put("/{report_id}", response_model=DailyReportResponse)
def update_daily_report(
    report_id: int,
    data: DailyReportUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = (
        db.query(DailyReport)
        .filter(
            DailyReport.report_id == report_id,
            DailyReport.user_id == current_user.user_id
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Daily report not found."
        )

    try:
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(record, key, value)

        db.commit()
        db.refresh(record)
        return record

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A report already exists for the updated date."
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to update daily report."
        )
