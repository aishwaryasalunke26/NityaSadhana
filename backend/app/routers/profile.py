
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
from app.models import DevoteeProfile, User
from app.routers.auth import get_current_user

from app.schemas.profile import (
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse,
)


router = APIRouter(
    prefix="/api/profile",
    tags=["Devotee Profile"]
)


# 1. CREATE PROFILE
@router.post(
    "/",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED
)
def create_profile(
    data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    existing_profile = db.query(DevoteeProfile).filter(
        DevoteeProfile.user_id == current_user.user_id
    ).first()

    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profile already exists for this user."
        )

    profile = DevoteeProfile(
        user_id=current_user.user_id,
        full_name=data.full_name,
        initiated_name=data.initiated_name,
        phone=data.phone,
        city=data.city,
    )

    try:
        db.add(profile)
        db.commit()
        db.refresh(profile)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profile already exists for this user."
        )

    return profile


# 2. VIEW MY PROFILE
@router.get(
    "/me",
    response_model=ProfileResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    profile = db.query(DevoteeProfile).filter(
        DevoteeProfile.user_id == current_user.user_id
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please create your profile first."
        )

    return profile


# 3. UPDATE MY PROFILE
@router.put(
    "/me",
    response_model=ProfileResponse
)
def update_my_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    profile = db.query(DevoteeProfile).filter(
        DevoteeProfile.user_id == current_user.user_id
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please create your profile first."
        )

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(profile, field, value)

    try:
        db.commit()
        db.refresh(profile)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profile update failed due to a database conflict."
        )

    return profile
