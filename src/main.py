import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from models import db
from routes.room import room
from routes.user import user
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

app = FastAPI(middleware=middleware)


app = FastAPI(title="Demo", description="A simple demo", version="demo")


@app.get("/", tags=["root"])
def redirect_to_docs():
    return RedirectResponse(url="/docs/")


@app.on_event("startup")
async def configure_routes():
    # Connect and create db
    db.bind("sqlite", "example.sqlite", create_db=True)
    db.generate_mapping(create_tables=True)
    app.include_router(user)
    app.include_router(room)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
