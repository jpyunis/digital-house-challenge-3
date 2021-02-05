from sqlalchemy.orm import Session

from . import models, schemas
from .music_recognition import save_track, compute_features


def get_song(db: Session, song_id: int):
    return db.query(models.Song).filter(models.Song.id == song_id).first()


def get_song_by_name(db: Session, name: str):
    return db.query(models.Song).filter(models.Song.name == name).first()


def get_songs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Song).offset(skip).limit(limit).all()


def create_song(db: Session, song: schemas.SongCreate):
    filename = save_track(song.url)

    #compute_features(filename)

    db_song = models.Song(name=song.name, url=song.url, filename=filename)
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

