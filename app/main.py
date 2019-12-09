from fastapi import Depends, FastAPI, Header, HTTPException
from starlette.middleware.cors import CORSMiddleware

from .routers import items, users

app = FastAPI(
    title="FastAPI Authentication Boilerplate",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.include_router(users.router)
app.include_router(
    items.router,
    prefix="/v1/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@app.get("/")
async def root():
    return "This is the root"

