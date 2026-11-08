
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


class ProfileCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    initiated_name: str | None = Field(default=None, max_length=150)
    phone: str | None = Field(default=None, max_length=20)
    city: str | None = Field(default=None, max_length=100)

    @field_validator("*", mode="before")
    @classmethod
    def clean_strings(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                return None
        return value

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):
        if not value:
            raise ValueError("Full name is required.")
        return value


class ProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=150)
    initiated_name: str | None = Field(default=None, max_length=150)
    phone: str | None = Field(default=None, max_length=20)
    city: str | None = Field(default=None, max_length=100)

    @field_validator("*", mode="before")
    @classmethod
    def clean_strings(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                return None
        return value

    @model_validator(mode="after")
    def validate_update(self):
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update.")

        if "full_name" in self.model_fields_set:
            if not self.full_name:
                raise ValueError("Full name cannot be empty.")

        return self


class ProfileResponse(BaseModel):
    profile_id: int
    user_id: int
    full_name: str
    initiated_name: str | None = None
    phone: str | None = None
    city: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
