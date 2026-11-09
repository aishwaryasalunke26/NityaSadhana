
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict, model_validator


HearingSource = Literal[
    "Srimad Bhagavatam Class",
    "Bhagavad Gita Class",
    "Lecture",
    "Kirtan",
    "Other",
]


class HearingCreate(BaseModel):
    hearing_date: date
    topic: str = Field(min_length=1, max_length=255)
    speaker_name: str | None = Field(default=None, max_length=150)
    source: HearingSource = "Lecture"
    duration_minutes: int = Field(default=0, ge=0)
    notes: str | None = None

    @model_validator(mode="after")
    def validate_topic(self):
        self.topic = self.topic.strip()
        if not self.topic:
            raise ValueError("Hearing topic cannot be empty.")
        if self.speaker_name is not None:
            self.speaker_name = self.speaker_name.strip() or None
        return self


class HearingUpdate(BaseModel):
    hearing_date: date | None = None
    topic: str | None = Field(default=None, min_length=1, max_length=255)
    speaker_name: str | None = Field(default=None, max_length=150)
    source: HearingSource | None = None
    duration_minutes: int | None = Field(default=None, ge=0)
    notes: str | None = None

    @model_validator(mode="after")
    def validate_update(self):
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update.")

        if "hearing_date" in self.model_fields_set and self.hearing_date is None:
            raise ValueError("Hearing date cannot be empty.")

        if "topic" in self.model_fields_set:
            if self.topic is None or not self.topic.strip():
                raise ValueError("Hearing topic cannot be empty.")
            self.topic = self.topic.strip()

        if "speaker_name" in self.model_fields_set:
            if self.speaker_name is not None:
                self.speaker_name = self.speaker_name.strip() or None

        if "source" in self.model_fields_set and self.source is None:
            raise ValueError("Hearing source cannot be empty.")

        if "duration_minutes" in self.model_fields_set:
            if self.duration_minutes is None:
                raise ValueError("Hearing duration cannot be empty.")

        return self


class HearingResponse(BaseModel):
    hearing_id: int
    user_id: int
    hearing_date: date
    topic: str
    speaker_name: str | None = None
    source: str | None = None
    duration_minutes: int | None = None
    notes: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class HearingSummary(BaseModel):
    total_sessions: int
    total_hearing_minutes: int
    total_hearing_hours: float
