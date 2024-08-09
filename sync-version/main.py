from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes.users import user_router
from database.db import initialize_database


app = FastAPI()
app.include_router(user_router)


@app.on_event("startup")
async def init_db():
    await initialize_database()


@app.get("/")
async def home():
    return RedirectResponse(url="/event/")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
