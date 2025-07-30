from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Date,
    CheckConstraint,
    Numeric,
)


class ChunithmMusicDBBase(DeclarativeBase):
    __abstract__ = True


class ChunithmChartData(ChunithmMusicDBBase):
    __tablename__ = "chart_data"
    music_id = Column(Integer, primary_key=True)
    difficulty = Column(Integer, primary_key=True)
    creator = Column(String(50), nullable=True)
    bpm = Column(Float, nullable=True)
    tap_count = Column(Integer, nullable=True)
    hold_count = Column(Integer, nullable=True)
    slide_count = Column(Integer, nullable=True)
    air_count = Column(Integer, nullable=True)
    flick_count = Column(Integer, nullable=True)
    total_count = Column(Integer, nullable=True)


class ChunithmMusic(ChunithmMusicDBBase):
    __tablename__ = "music"
    music_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    category = Column(String(50), nullable=True)
    version = Column(String(10), nullable=True)
    release_date = Column(Date, nullable=True)
    is_deleted = Column(Integer, CheckConstraint("is_deleted IN (0, 1)"), default=0)
    deleted_version = Column(String(10), nullable=True)


class ChunithmMusicDifficulty(ChunithmMusicDBBase):
    __tablename__ = "music_difficulties"
    music_id = Column(Integer, primary_key=True)
    version = Column(String(10), primary_key=True)
    diff0_const = Column(Numeric(3, 1))
    diff1_const = Column(Numeric(3, 1))
    diff2_const = Column(Numeric(3, 1))
    diff3_const = Column(Numeric(3, 1))
    diff4_const = Column(Numeric(3, 1))
