from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes.users import user_router
# from routes.terminals import terminal_router
# from routes.equipment import equipment_router
from database.db import conn


app = FastAPI()
app.include_router(user_router, prefix="/user")
# app.include_router(terminal_router, prefix="/terminal")
# app.include_router(equipment_router, prefix="/equipment")


@app.on_event("startup")
def on_startup():
    conn()


@app.get("/")
async def home():
    return RedirectResponse(url="/user")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
