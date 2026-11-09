
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from app.models import (
    User,
    JapaRecord,
    BookReading,
    HearingRecord,
    SevaRecord,
    DailyReport,
)
from app.routers.auth import get_current_user
from app.schemas.summary import DailySadhanaSummary


router = APIRouter(
    prefix="/api/summary",
    tags=["Daily Sadhana Summary"],
)


@router.get(
    "/me",
    response_model=DailySadhanaSummary,
)
def get_daily_sadhana_summary(
    report_date: date = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    # 1. Get Japa record
    japa_record = (
        db.query(JapaRecord)
        .filter(
            JapaRecord.user_id == current_user.user_id,
            JapaRecord.record_date == report_date,
        )
        .first()
    )

    japa_rounds = (
        int(japa_record.rounds_completed or 0)
        if japa_record else 0
    )

    # 2. Get Book Reading records
    reading_records = (
        db.query(BookReading)
        .filter(
            BookReading.user_id == current_user.user_id,
            BookReading.reading_date == report_date,
        )
        .order_by(BookReading.reading_id.asc())
        .all()
    )

    reading_pages = sum(
        int(record.pages_read or 0)
        for record in reading_records
    )

    reading_minutes = sum(
        int(record.reading_minutes or 0)
        for record in reading_records
    )

    # 3. Get Hearing records
    hearing_records = (
        db.query(HearingRecord)
        .filter(
            HearingRecord.user_id == current_user.user_id,
            HearingRecord.hearing_date == report_date,
        )
        .order_by(HearingRecord.hearing_id.asc())
        .all()
    )

    hearing_minutes = sum(
        int(record.duration_minutes or 0)
        for record in hearing_records
    )

    # 4. Get Seva records
    seva_records = (
        db.query(SevaRecord)
        .filter(
            SevaRecord.user_id == current_user.user_id,
            SevaRecord.seva_date == report_date,
        )
        .order_by(SevaRecord.seva_id.asc())
        .all()
    )

    seva_minutes = sum(
        int(record.duration_minutes or 0)
        for record in seva_records
    )

    # 5. Get Daily Report
    daily_report = (
        db.query(DailyReport)
        .filter(
            DailyReport.user_id == current_user.user_id,
            DailyReport.report_date == report_date,
        )
        .first()
    )

    # 6. Calculate total activity minutes
    total_activity_minutes = (
        reading_minutes
        + hearing_minutes
        + seva_minutes
    )

    # 7. Return complete daily summary
    return DailySadhanaSummary(
        report_date=report_date,

        japa_rounds=japa_rounds,
        japa_record=japa_record,

        reading_sessions=len(reading_records),
        reading_pages=reading_pages,
        reading_minutes=reading_minutes,
        reading_records=reading_records,

        hearing_sessions=len(hearing_records),
        hearing_minutes=hearing_minutes,
        hearing_records=hearing_records,

        seva_activities=len(seva_records),
        seva_minutes=seva_minutes,
        seva_records=seva_records,

        report_submitted=daily_report is not None,
        daily_report=daily_report,

        total_activity_minutes=total_activity_minutes,
    )
