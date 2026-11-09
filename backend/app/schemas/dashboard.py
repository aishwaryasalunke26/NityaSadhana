
from datetime import date

from pydantic import BaseModel, ConfigDict


class DashboardDay(BaseModel):
    activity_date: date

    japa_rounds: int

    reading_sessions: int
    reading_pages: int
    reading_minutes: int

    hearing_sessions: int
    hearing_minutes: int

    seva_activities: int
    seva_minutes: int

    total_activity_minutes: int

    model_config = ConfigDict(from_attributes=True)


class DashboardStats(BaseModel):
    start_date: date
    end_date: date
    total_days: int

    total_japa_rounds: int

    total_reading_sessions: int
    total_reading_pages: int
    total_reading_minutes: int

    total_hearing_sessions: int
    total_hearing_minutes: int

    total_seva_activities: int
    total_seva_minutes: int

    total_activity_minutes: int

    daily_stats: list[DashboardDay]

    model_config = ConfigDict(from_attributes=True)
