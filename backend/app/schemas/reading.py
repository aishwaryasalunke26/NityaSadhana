
from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict, model_validator


class ReadingCreate(BaseModel):
    reading_date: date
    book_title: str = Field(min_length=1, max_length=255)
    pages_read: int = Field(default=0, ge=0)
    reading_minutes: int = Field(default=0, ge=0)
    notes: str | None = None

    @model_validator(mode="after")
    def validate_book_title(self):
        self.book_title = self.book_title.strip()
        if not self.book_title:
            raise ValueError("Book title cannot be empty.")
        return self


class ReadingUpdate(BaseModel):
    reading_date: date | None = None
    book_title: str | None = Field(default=None, min_length=1, max_length=255)
    pages_read: int | None = Field(default=None, ge=0)
    reading_minutes: int | None = Field(default=None, ge=0)
    notes: str | None = None

    @model_validator(mode="after")
    def validate_update(self):
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update.")

        if "reading_date" in self.model_fields_set and self.reading_date is None:
            raise ValueError("Reading date cannot be empty.")

        if "book_title" in self.model_fields_set:
            if self.book_title is None or not self.book_title.strip():
                raise ValueError("Book title cannot be empty.")
            self.book_title = self.book_title.strip()

        if "pages_read" in self.model_fields_set and self.pages_read is None:
            raise ValueError("Pages read cannot be empty.")

        if "reading_minutes" in self.model_fields_set and self.reading_minutes is None:
            raise ValueError("Reading minutes cannot be empty.")

        return self


class ReadingResponse(BaseModel):
    reading_id: int
    user_id: int
    reading_date: date
    book_title: str
    pages_read: int | None = None
    reading_minutes: int | None = None
    notes: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
