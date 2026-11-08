from sqlalchemy import (
    Column,
    String,
    Text,
    Date,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint,
    Index,
    text,
    func,
    FetchedValue,
)
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, ENUM

from database import Base


# 1. USERS TABLE
class User(Base):
    __tablename__ = "users"

    user_id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

    role = Column(
        ENUM("devotee", "admin"),
        server_default=text("'devotee'")
    )

    account_status = Column(
        ENUM("active", "inactive"),
        server_default=text("'active'")
    )

    created_at = Column(
        TIMESTAMP,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue()
    )


# 2. DEVOTEE PROFILES TABLE
class DevoteeProfile(Base):
    __tablename__ = "devotee_profiles"

    profile_id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)

    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.user_id", name="fk_profile_user", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    full_name = Column(String(150), nullable=False)
    initiated_name = Column(String(150), nullable=True)
    phone = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)

    created_at = Column(
        TIMESTAMP,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue()
    )


# 3. JAPA RECORDS TABLE
class JapaRecord(Base):
    __tablename__ = "japa_records"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "record_date",
            name="unique_user_japa_date"
        ),
    )

    japa_id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)

    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.user_id", name="fk_japa_user", ondelete="CASCADE"),
        nullable=False
    )

    record_date = Column(Date, nullable=False)

    rounds_completed = Column(
        INTEGER(unsigned=True),
        nullable=False,
        server_default=text("0")
    )

    notes = Column(Text, nullable=True)

    created_at = Column(
        TIMESTAMP,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP")
    )


# 4. BOOK READING TABLE
class BookReading(Base):
    __tablename__ = "book_reading"

    __table_args__ = (
        Index("fk_reading_user", "user_id"),
    )

    reading_id = Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.user_id", name="fk_reading_user", ondelete="CASCADE"),
        nullable=False
    )

    reading_date = Column(Date, nullable=False)
    book_title = Column(String(255), nullable=False)

    pages_read = Column(
        INTEGER(unsigned=True),
        nullable=True,
        server_default=text("0")
    )

    reading_minutes = Column(
        INTEGER(unsigned=True),
        nullable=True,
        server_default=text("0")
    )

    notes = Column(Text, nullable=True)

    created_at = Column(
        TIMESTAMP,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP")
    )


# 5. HEARING RECORDS TABLE
class HearingRecord(Base):
    __tablename__ = "hearing_records"

    __table_args__ = (
        Index("fk_hearing_user", "user_id"),
    )

    hearing_id = Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.user_id", name="fk_hearing_user", ondelete="CASCADE"),
        nullable=False
    )

    hearing_date = Column(Date, nullable=False)
    topic = Column(String(255), nullable=False)
    speaker_name = Column(String(150), nullable=True)

    source = Column(
        ENUM(
            "Srimad Bhagavatam Class",
            "Bhagavad Gita Class",
            "Lecture",
            "Kirtan",
            "Other"
        ),
        nullable=True,
        server_default=text("'Lecture'")
    )

    duration_minutes = Column(
        INTEGER(unsigned=True),
        nullable=True,
        server_default=text("0")
    )

    notes = Column(Text, nullable=True)

    created_at = Column(
        TIMESTAMP,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP")
    )


# 6. SEVA RECORDS TABLE
class SevaRecord(Base):
    __tablename__ = "seva_records"

    __table_args__ = (
        Index("fk_seva_user", "user_id"),
    )

    seva_id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)

    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.user_id", name="fk_seva_user", ondelete="CASCADE"),
        nullable=False
    )

    seva_date = Column(Date, nullable=False)
    seva_type = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)

    duration_minutes = Column(
        INTEGER(unsigned=True),
        nullable=True,
        server_default=text("0")
    )

    created_at = Column(
        TIMESTAMP,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP")
    )


# 7. DAILY REPORTS TABLE
class DailyReport(Base):
    __tablename__ = "daily_reports"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "report_date",
            name="unique_user_report_date"
        ),
    )

    report_id = Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.user_id", name="fk_report_user", ondelete="CASCADE"),
        nullable=False
    )

    report_date = Column(Date, nullable=False)
    reflection = Column(Text, nullable=True)
    gratitude = Column(Text, nullable=True)
    challenges = Column(Text, nullable=True)

    created_at = Column(
        TIMESTAMP,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue()
    )