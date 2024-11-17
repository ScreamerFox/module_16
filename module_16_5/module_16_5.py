from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from pydantic import BaseModel, Field

app = FastAPI()

templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int = Field(ge=1, le=100, examples=[45])
    username: str = Field(min_length=5, max_length=20, description="Enter username", examples=["UrbanUser"])
    age: int = Field(ge=18, le=120, description="Enter age", examples=[24])


@app.get("/", response_class=HTMLResponse)
async def read_users(request: Request):
    # Передаем данные в шаблон
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_users(request: Request, user_id: int):
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})


@app.post("/user/{username}/{age}")
async def create_user(user: User):
    user.id = len(users) + 1
    users.append(user)
    return {"message": f"User {user.id} is registered", "user": user}


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user: User):
    for us in users:
        if us.id == user.id:
            us.username = user.username
            us.age = user.age
            return f"The user {user.id} is updated"
    raise HTTPException(status_code=400, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user: User):
    for us in users:
        if us.id == user.id:
            users.remove(us)
            return f"User {user.id} deleted"
    raise HTTPException(status_code=400, detail="User was not found")

users.append(User(id=1, username="UrbanUser", age=24))
users.append(User(id=2, username="UrbanTest", age=22))
users.append(User(id=3, username="Capybara", age=60))