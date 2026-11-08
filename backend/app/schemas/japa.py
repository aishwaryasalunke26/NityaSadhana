
from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict, model_validator


class JapaCreate(BaseModel):
    record_date: date
    rounds_completed: int = Field(default=0, ge=0)
    notes: str | None = None


class JapaUpdate(BaseModel):
    record_date: date | None = None
    rounds_completed: int | None = Field(default=None, ge=0)
    notes: str | None = None

    @model_validator(mode="after")
    def validate_update(self):
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update.")

        if "record_date" in self.model_fields_set:
            if self.record_date is None:
                raise ValueError("Record date cannot be empty.")

        if "rounds_completed" in self.model_fields_set:
            if self.rounds_completed is None:
                raise ValueError("Rounds completed cannot be empty.")

        return self


class JapaResponse(BaseModel):
    japa_id: int
    user_id: int
    record_date: date
    rounds_completed: int
    notes: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
