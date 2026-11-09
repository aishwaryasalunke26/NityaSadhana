
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db

from app.models import (
    User,
    JapaRecord,
    BookReading,
    HearingRecord,
    SevaRecord,
)

from app.routers.auth import get_current_user

from app.schemas.dashboard import (
    DashboardStats,
    DashboardDay,
)


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard Statistics"],
)


@router.get(
    "/me",
    response_model=DashboardStats,
)
def get_dashboard_statistics(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    # 1. Set default date range
    today = date.today()

    if end_date is None:
        end_date = today

    if start_date is None:
        start_date = end_date - timedelta(days=6)

    # 2. Validate date range
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date.",
        )

    total_days = (end_date - start_date).days + 1

    # 3. Initialize daily statistics
    daily_data = {}

    current_date = start_date

    while current_date <= end_date:

        daily_data[current_date] = {
            "activity_date": current_date,

            "japa_rounds": 0,

            "reading_sessions": 0,
            "reading_pages": 0,
            "reading_minutes": 0,

            "hearing_sessions": 0,
            "hearing_minutes": 0,

            "seva_activities": 0,
            "seva_minutes": 0,
        }

        current_date += timedelta(days=1)

    # 4. Get Japa records
    japa_records = (
        db.query(JapaRecord)
        .filter(
            JapaRecord.user_id == current_user.user_id,
            JapaRecord.record_date >= start_date,
            JapaRecord.record_date <= end_date,
        )
        .all()
    )

    for record in japa_records:
        daily_data[record.record_date]["japa_rounds"] += int(
            record.rounds_completed or 0
        )

    # 5. Get Book Reading records
    reading_records = (
        db.query(BookReading)
        .filter(
            BookReading.user_id == current_user.user_id,
            BookReading.reading_date >= start_date,
            BookReading.reading_date <= end_date,
        )
        .all()
    )

    for record in reading_records:
        day = daily_data[record.reading_date]

        day["reading_sessions"] += 1
        day["reading_pages"] += int(record.pages_read or 0)
        day["reading_minutes"] += int(record.reading_minutes or 0)

    # 6. Get Hearing records
    hearing_records = (
        db.query(HearingRecord)
        .filter(
            HearingRecord.user_id == current_user.user_id,
            HearingRecord.hearing_date >= start_date,
            HearingRecord.hearing_date <= end_date,
        )
        .all()
    )

    for record in hearing_records:
        day = daily_data[record.hearing_date]

        day["hearing_sessions"] += 1
        day["hearing_minutes"] += int(record.duration_minutes or 0)

    # 7. Get Seva records
    seva_records = (
        db.query(SevaRecord)
        .filter(
            SevaRecord.user_id == current_user.user_id,
            SevaRecord.seva_date >= start_date,
            SevaRecord.seva_date <= end_date,
        )
        .all()
    )

    for record in seva_records:
        day = daily_data[record.seva_date]

        day["seva_activities"] += 1
        day["seva_minutes"] += int(record.duration_minutes or 0)

    # 8. Prepare daily response
    daily_stats = []

    for day in daily_data.values():

        total_minutes = (
            day["reading_minutes"]
            + day["hearing_minutes"]
            + day["seva_minutes"]
        )

        daily_stats.append(
            DashboardDay(
                **day,
                total_activity_minutes=total_minutes,
            )
        )

    # 9. Calculate overall totals
    total_japa_rounds = sum(
        day.japa_rounds for day in daily_stats
    )

    total_reading_sessions = sum(
        day.reading_sessions for day in daily_stats
    )

    total_reading_pages = sum(
        day.reading_pages for day in daily_stats
    )

    total_reading_minutes = sum(
        day.reading_minutes for day in daily_stats
    )

    total_hearing_sessions = sum(
        day.hearing_sessions for day in daily_stats
    )

    total_hearing_minutes = sum(
        day.hearing_minutes for day in daily_stats
    )

    total_seva_activities = sum(
        day.seva_activities for day in daily_stats
    )

    total_seva_minutes = sum(
        day.seva_minutes for day in daily_stats
    )

    total_activity_minutes = (
        total_reading_minutes
        + total_hearing_minutes
        + total_seva_minutes
    )

    # 10. Return dashboard statistics
    return DashboardStats(
        start_date=start_date,
        end_date=end_date,
        total_days=total_days,

        total_japa_rounds=total_japa_rounds,

        total_reading_sessions=total_reading_sessions,
        total_reading_pages=total_reading_pages,
        total_reading_minutes=total_reading_minutes,

        total_hearing_sessions=total_hearing_sessions,
        total_hearing_minutes=total_hearing_minutes,

        total_seva_activities=total_seva_activities,
        total_seva_minutes=total_seva_minutes,

        total_activity_minutes=total_activity_minutes,

        daily_stats=daily_stats,
    )
