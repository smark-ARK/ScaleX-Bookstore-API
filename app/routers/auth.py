from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.oauth2 import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    users,
)
from app.schemas import ResponseToken

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=ResponseToken)
def login(
    response: Response,
    user_cred: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(user_cred.username, user_cred.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
    access_token = create_access_token(
        data={"user_id": user.get("id"), "username": user.get("username")}
    )
    refresh_token = create_refresh_token(
        data={"user_id": user.get("id"), "username": user.get("username")}
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="none",
        secure=True,
        domain=None,
    )  # set HttpOnly cookie in response

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# Function to authenticate user
def authenticate_user(username: str, password: str):
    user = next((x for x in users if x["username"] == username), None)
    if not user:
        return False
    if not password == user["password"]:
        return False
    return user


@router.post("/refresh")
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="No refresh token found in cookies")

    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    new_access_token = create_access_token(data=payload)
    refresh_token = create_refresh_token(data={"user_id": payload})

    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return {"access_token": new_access_token, "token_type": "bearer"}
