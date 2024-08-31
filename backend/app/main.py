from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import auth, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Service is starting.")

    yield

    print("Service is stopped.")


app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(req: Request, exc: HTTPException):
    content = {"detail": exc.detail}
    if exc.headers and "X-Error" in exc.headers:
        content["code"] = exc.headers["X-Error"]

    return JSONResponse(status_code=exc.status_code, content=content)


app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
