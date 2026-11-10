from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database import get_db
from app.models.models import DailyReport
from app.routers.auth import get_current_user
from app.schemas.reports import DailyReportSave, DailyReportResponse


router = APIRouter(
    prefix="/api/reports",
    tags=["Daily Reports"]
)


def get_user_report(db: Session, user_id: int, report_date: date):
    return db.query(DailyReport).filter(
        DailyReport.user_id == user_id,
        DailyReport.report_date == report_date
    ).first()


def check_edit_permission(record: DailyReport):
    if record.status != "Submitted":
        return

    if record.submitted_at is None:
        raise HTTPException(
            status_code=403,
            detail="This submitted report cannot be edited."
        )

    submitted = record.submitted_at

    if submitted.tzinfo is None:
        submitted = submitted.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) - submitted >= timedelta(hours=24):
        raise HTTPException(
            status_code=403,
            detail="The 24-hour editing period has ended."
        )


@router.get("/today", response_model=DailyReportResponse)
def get_today_report(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    record = get_user_report(
        db,
        current_user.user_id,
        date.today()
    )

    if not record:
        raise HTTPException(status_code=404, detail="Today's report not found.")

    return record


@router.get("/previous", response_model=DailyReportResponse)
def get_previous_report(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    previous_date = date.today() - timedelta(days=1)

    record = get_user_report(
        db,
        current_user.user_id,
        previous_date
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="No previous day's report found."
        )

    return record


@router.get("/me", response_model=list[DailyReportResponse])
def get_my_daily_reports(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(DailyReport).filter(
        DailyReport.user_id == current_user.user_id
    ).order_by(
        DailyReport.report_date.desc(),
        DailyReport.report_id.desc()
    ).all()


@router.post(
    "/save",
    response_model=DailyReportResponse,
    status_code=status.HTTP_200_OK
)
def save_daily_report(
    data: DailyReportSave,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    record = get_user_report(
        db,
        current_user.user_id,
        data.report_date
    )

    if record:
        check_edit_permission(record)

        record.report_data = data.report_data

        if record.status != "Submitted":
            record.status = "Draft"
    else:
        record = DailyReport(
            user_id=current_user.user_id,
            report_date=data.report_date,
            report_data=data.report_data,
            status="Draft"
        )
        db.add(record)

    try:
        db.commit()
        db.refresh(record)
        return record

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A report already exists for this date."
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to save daily report."
        )


@router.post(
    "/submit",
    response_model=DailyReportResponse
)
def submit_daily_report(
    data: DailyReportSave,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    record = get_user_report(
        db,
        current_user.user_id,
        data.report_date
    )

    if record:
        check_edit_permission(record)
        record.report_data = data.report_data
    else:
        record = DailyReport(
            user_id=current_user.user_id,
            report_date=data.report_date,
            report_data=data.report_data
        )
        db.add(record)

    record.status = "Submitted"
    record.submitted_at = datetime.now(timezone.utc).replace(tzinfo=None)

    try:
        db.commit()
        db.refresh(record)
        return record

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A report already exists for this date."
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to submit daily report."
        )


@router.get("/{report_id}", response_model=DailyReportResponse)
def get_daily_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    record = db.query(DailyReport).filter(
        DailyReport.report_id == report_id,
        DailyReport.user_id == current_user.user_id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Report not found.")

    return record