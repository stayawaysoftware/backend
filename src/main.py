import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from models import db
from routes.user import user

app = FastAPI(title="Demo", description="A simple demo", version="demo")


@app.get("/", tags=["root"])
def redirect_to_docs():
    return RedirectResponse(url="/docs/")


@app.on_event("startup")
async def configure_routes():
    # Connect and create db
    db.bind("sqlite", "db.sqlite", create_db=True)
    db.generate_mapping(create_tables=True)
    app.include_router(user)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
