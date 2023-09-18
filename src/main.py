from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from db import db
import uvicorn

app = FastAPI(
    title = "Muestra",
    description = "Una simple muestra",
    version = "demo"
)

@app.get('/', tags=['root'])
def redirect_to_docs():
    return RedirectResponse(url="/docs/")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host = "0.0.0.0",
        reload = True,
        port = 8000
    )