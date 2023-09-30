"""Main module to run the application."""
from contextlib import asynccontextmanager

import uvicorn
from db.database import bind_database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from routes import room
from routes import user


# https://fastapi.tiangolo.com/advanced/events/
@asynccontextmanager
async def lifespan(application: FastAPI):
    """Context manager to start and stop the application."""
    try:
        bind_database()
        yield
    finally:
        pass


# FastAPI instance
app = FastAPI(
    title="Stay Away",
    description="Stay Away - Card Game",
    version="Demo 1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.user_router)
app.include_router(room.room_router)
# app.include_router(player.player_router)
# app.include_router(game.game_router)
# app.include_router(card.card_router)


# Root router
@app.get("/", tags=["root"])
def redirect_to_docs():
    """Redirect to the docs -> only for this moment of development."""
    return RedirectResponse(url="/docs/")


# Run app
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
