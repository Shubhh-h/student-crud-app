from datetime import date
from typing import Annotated, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]


def _not_in_future(v: Optional[date]) -> Optional[date]:
    if v is not None and v > date.today():
        raise ValueError("date of birth cannot be in the future")
    return v


class StudentBase(BaseModel):
    name: Name
    date_of_birth: date
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=20)
    course: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=255)
    enrollment_date: Optional[date] = None

    @field_validator("date_of_birth")
    @classmethod
    def dob_check(cls, v):
        return _not_in_future(v)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[Name] = None
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=20)
    course: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=255)
    enrollment_date: Optional[date] = None

    @field_validator("date_of_birth")
    @classmethod
    def dob_check(cls, v):
        return _not_in_future(v)

    @model_validator(mode="after")
    def required_fields_not_null(self):
        # Sending {"name": null} would wipe a required column -> reject it
        for f in ("name", "date_of_birth", "email"):
            if f in self.model_fields_set and getattr(self, f) is None:
                raise ValueError(f"{f} cannot be null")
        return self


class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
