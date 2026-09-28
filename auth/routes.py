from fastapi import APIRouter, HTTPException, Response, status

from auth.jwt import create_access_token
from auth.password import verify_password
from auth.service import create_user, get_user_by_email
from auth.dependencies import get_current_user
from schemas.auth import UserCreate, UserLogin, UserResponse
from fastapi import Depends


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/me")
def get_me(
    current_user: dict = Depends(get_current_user)
):
    return {
        "id": str(current_user["_id"]),
        "email": current_user["email"]
    }


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(user: UserCreate):

    try:
        created_user = create_user(
            user.email,
            user.password
        )

        return created_user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login")
def login(
    user: UserLogin,
    response: Response
):
    db_user = get_user_by_email(user.email)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    password_valid = verify_password(
        user.password,
        db_user["password_hash"]
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token({
        "sub": str(db_user["_id"])
    })

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,                    # Set this to true in production
        samesite="lax",
        max_age=60 * 60
    )

    return {
        "message": "Login successful"
    }


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )

    return {"message": "Logout successful"}