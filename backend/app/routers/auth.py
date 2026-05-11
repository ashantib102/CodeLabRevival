"""
Authentication router — POST /auth/login
Returns a JWT access token.
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, status
from jose import jwt

from app.data import get_user_by_email, verify_password, USERS, pwd_context
from app.models import LoginRequest, RegisterRequest, ForgotPasswordRequest, ResetPasswordRequest, TokenResponse, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "changeme-use-env-var-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8 hours


def _create_token(user_id: int, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    user = get_user_by_email(body.email)
    if not user or not verify_password(body.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    token = _create_token(user["id"], user["role"])
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserPublic(
            id=str(user["id"]),
            name=user["name"],
            email=user["email"],
            role=user["role"],
        ),
    )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest):
    if body.role not in ("student", "instructor"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be 'student' or 'instructor'.",
        )
    if get_user_by_email(body.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with that email already exists.",
        )
    new_id = max(u["id"] for u in USERS) + 1
    new_user: dict = {
        "id": new_id,
        "name": body.name.strip(),
        "email": body.email.strip().lower(),
        "hashed_password": pwd_context.hash(body.password),
        "role": body.role,
    }
    # Students are enrolled in the main course by default so they can access the lab
    if body.role == "student":
        new_user["enrolled_courses"] = ["59094"]
    # Instructors start with no section key; an admin can assign one later
    if body.role == "instructor":
        new_user["instructor_key"] = ""
    USERS.append(new_user)
    token = _create_token(new_id, body.role)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserPublic(
            id=str(new_id),
            name=new_user["name"],
            email=new_user["email"],
            role=new_user["role"],
        ),
    )


@router.post("/forgot-password")
def forgot_password(body: ForgotPasswordRequest):
    user = get_user_by_email(body.email.strip().lower())
    # Always return success to prevent email enumeration
    if user:
        # Generate a reset token
        reset_token = _create_reset_token(user["id"])
        # Send email
        _send_reset_email(user["email"], reset_token)
    return {"message": "If an account with that email exists, a password reset link has been sent."}


@router.post("/reset-password")
def reset_password(body: ResetPasswordRequest):
    try:
        payload = jwt.decode(body.token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "reset":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token type")
        user_id = int(payload["sub"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    user["hashed_password"] = pwd_context.hash(body.password)
    return {"message": "Password reset successfully"}


def _create_reset_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=1)  # 1 hour expiry
    payload = {"sub": str(user_id), "type": "reset", "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _send_reset_email(email: str, reset_token: str):
    # For demo purposes, we'll just print the email content
    # In production, you'd configure SMTP properly
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    if not smtp_user or not smtp_pass:
        print(f"Password reset for {email}: {reset_token}")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = email
        msg['Subject'] = "Password Reset - CodeLab"

        body = f"""
        You requested a password reset for your CodeLab account.

        Click the link below to reset your password:
        http://localhost:3000/reset-password?token={reset_token}

        If you didn't request this, please ignore this email.

        This link will expire in 1 hour.
        """

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        text = msg.as_string()
        server.sendmail(smtp_user, email, text)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")
        # In production, you'd want to handle this better
