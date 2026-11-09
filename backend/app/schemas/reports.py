
from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict, model_validator


class DailyReportCreate(BaseModel):
    report_date: date
    reflection: str = Field(min_length=1)
    gratitude: str = Field(min_length=1)
    challenges: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_fields(self):
        self.reflection = self.reflection.strip()
        self.gratitude = self.gratitude.strip()
        self.challenges = self.challenges.strip()

        if not self.reflection:
            raise ValueError("Reflection cannot be empty.")
        if not self.gratitude:
            raise ValueError("Gratitude cannot be empty.")
        if not self.challenges:
            raise ValueError("Challenges cannot be empty.")

        return self


class DailyReportUpdate(BaseModel):
    report_date: date | None = None
    reflection: str | None = Field(default=None, min_length=1)
    gratitude: str | None = Field(default=None, min_length=1)
    challenges: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_update(self):
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update.")

        for field in ("report_date", "reflection", "gratitude", "challenges"):
            if field in self.model_fields_set:
                value = getattr(self, field)

                if value is None:
                    raise ValueError(f"{field} cannot be empty.")

                if isinstance(value, str):
                    value = value.strip()
                    if not value:
                        raise ValueError(f"{field} cannot be empty.")
                    setattr(self, field, value)

        return self


class DailyReportResponse(BaseModel):
    report_id: int
    user_id: int
    report_date: date
    reflection: str
    gratitude: str
    challenges: str
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
