from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Music Genre recognition",
              description="This is a very fancy project, with auto docs for the API and everything",
              version="1.0.0",)


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.post("/song/", response_model=schemas.Song)
def post_song(song: schemas.SongCreate, db: Session = Depends(get_db)):
    db_song = crud.get_song_by_name(db, name=song.name)
    if not db_song:
        db_song = crud.create_song(db=db, song=song)
    return db_song


@app.get("/songs/", response_model=List[schemas.Song])
def read_songs_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_songs(db, skip=skip, limit=limit)
    return users


@app.get("/song/{song_name}", response_model=schemas.Song)
def read_song(song_name: str, db: Session = Depends(get_db)):
    db_song = crud.get_song_by_name(db, name=song_name)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return db_song


@app.get("/song/{song_name}/play", response_class=HTMLResponse)
def play_song(request: Request, song_name: str, db: Session = Depends(get_db)):
    db_song = crud.get_song_by_name(db, name=song_name)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")

    filepath = '/songs/' + db_song.filename

    return templates.TemplateResponse("song.html", {"request": request,
                                                    "song": db_song.name,
                                                    "filepath":  filepath})