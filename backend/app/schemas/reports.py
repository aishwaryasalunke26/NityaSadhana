from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DailyReportSave(BaseModel):
    report_date: date
    report_data: dict[str, Any] = Field(default_factory=dict)


class DailyReportResponse(BaseModel):
    report_id: int
    user_id: int
    report_date: date

    reflection: str | None = None
    gratitude: str | None = None
    challenges: str | None = None

    report_data: dict[str, Any] | None = None
    status: str
    submitted_at: datetime | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)