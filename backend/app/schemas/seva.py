
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict, model_validator


class SevaCreate(BaseModel):
    seva_date: date
    seva_type: str = Field(min_length=1, max_length=100)
    description: str | None = None
    duration_minutes: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def validate_seva_type(self):
        self.seva_type = self.seva_type.strip()
        if not self.seva_type:
            raise ValueError("Seva type cannot be empty.")
        return self


class SevaUpdate(BaseModel):
    seva_date: date | None = None
    seva_type: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    duration_minutes: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_update(self):
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update.")

        if "seva_date" in self.model_fields_set and self.seva_date is None:
            raise ValueError("Seva date cannot be empty.")

        if "seva_type" in self.model_fields_set:
            if self.seva_type is None or not self.seva_type.strip():
                raise ValueError("Seva type cannot be empty.")
            self.seva_type = self.seva_type.strip()

        if "duration_minutes" in self.model_fields_set:
            if self.duration_minutes is None:
                raise ValueError("Duration cannot be empty.")

        return self


class SevaResponse(BaseModel):
    seva_id: int
    user_id: int
    seva_date: date
    seva_type: str
    description: str | None = None
    duration_minutes: int | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
