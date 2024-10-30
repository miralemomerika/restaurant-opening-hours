from dateutil.parser import parse

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.deps import get_db
from crud.restaurant import crud_restaurant
from schemas.restaurant import (
    RestaurantNameRead,
)

router = APIRouter()


@router.get(
    "/{opening_hours}",
)
def get_album_by_id(*, db: Session = Depends(get_db), opening_hours: str) -> Any:
    """
    Get restaurant per opening hours.
    """
    try:
        parsed_datetime = parse(opening_hours)
    except ValueError:
        # Raise an HTTPException if parsing fails
        raise HTTPException(status_code=400, detail="Invalid opening_hours datetime format")

    restaurants = crud_restaurant.get_by_opening_hours(db=db, opening_hours=parsed_datetime)
    if not restaurants:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurants not found",
        )
    return {
        'description': "Restaurants retrieved successfully",
        'data': [
            RestaurantNameRead.model_validate(restaurant).model_dump()
            for restaurant in restaurants
        ],
    }
