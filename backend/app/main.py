import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, courses, exercises, submissions

app = FastAPI(
    title="CodeLab Revival API",
    description="Backend API for the CodeLab Revival coding education platform.",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────
# In production, replace "*" with the deployed frontend origin.
_allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(exercises.router)
app.include_router(submissions.router)


@app.get("/", tags=["health"])
def health():
    return {"status": "ok", "message": "CodeLab Revival API is running."}
