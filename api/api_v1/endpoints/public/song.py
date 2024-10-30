from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_db
from crud.crud_content_type import crud_content_type
from crud.crud_history_log import crud_history_log
from crud.crud_public_song import crud_public_song
from database_app.models import PublicSong
from schemas.common import SuccessResponse
from schemas.public.song import (
    PublicSongCreate,
    PublicSongReadHistoryLog,
)

router = APIRouter()


@router.post(
    "/",
    response_model=SuccessResponse,
)
def public_song_create(
    *,
    db: Session = Depends(get_db),
    song_in: PublicSongCreate,
) -> Any:
    """
    Create new public song.
    """
    content_type = crud_content_type.get_for_model(db=db, model=PublicSong)
    created = crud_public_song.create(db=db, obj_in=song_in)
    crud_history_log.public_create_event(
        db=db,
        content_type=content_type,
        obj_new=PublicSongReadHistoryLog.model_validate(created),
        user=None,
        object_id=created.id,
    )
    return SuccessResponse(
        description="Public song created successfully",
    )
