from datetime import date
from pydantic import BaseModel, ConfigDict


class MusicInfoSchema(BaseModel):
    music_id: int
    title: str
    artist: str
    category: str | None = None
    version: str | None = None
    release_date: date | None = None
    is_deleted: bool | None = None
    deleted_version: str | None = None

    model_config = ConfigDict(from_attributes=True)


class MusicDifficultySchema(BaseModel):
    music_id: int
    version: str
    diff0_const: float | None = None
    diff1_const: float | None = None
    diff2_const: float | None = None
    diff3_const: float | None = None
    diff4_const: float | None = None

    model_config = ConfigDict(from_attributes=True)


class ChartDataSchema(BaseModel):
    music_id: int
    difficulty: int
    creator: str | None = None
    bpm: float | None = None
    tap_count: int | None = None
    hold_count: int | None = None
    slide_count: int | None = None
    air_count: int | None = None
    flick_count: int | None = None
    total_count: int | None = None

    model_config = ConfigDict(from_attributes=True)
