from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class SongBase(BaseModel):
    name: str


class SongCreate(SongBase):
    url: HttpUrl
    pass


class Song(SongBase):
    id: int
    filename: str

    class Config:
        orm_mode = True
