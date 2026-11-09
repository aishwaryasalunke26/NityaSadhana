
from datetime import date

from pydantic import BaseModel, ConfigDict

from app.schemas.japa import JapaResponse
from app.schemas.reading import ReadingResponse
from app.schemas.hearing import HearingResponse
from app.schemas.seva import SevaResponse
from app.schemas.reports import DailyReportResponse


class DailySadhanaSummary(BaseModel):
    report_date: date

    # Japa
    japa_rounds: int
    japa_record: JapaResponse | None = None

    # Book Reading
    reading_sessions: int
    reading_pages: int
    reading_minutes: int
    reading_records: list[ReadingResponse]

    # Hearing
    hearing_sessions: int
    hearing_minutes: int
    hearing_records: list[HearingResponse]

    # Seva
    seva_activities: int
    seva_minutes: int
    seva_records: list[SevaResponse]

    # Daily Report
    report_submitted: bool
    daily_report: DailyReportResponse | None = None

    # Overall statistics
    total_activity_minutes: int

    model_config = ConfigDict(from_attributes=True)
