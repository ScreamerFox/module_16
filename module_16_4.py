from fastapi import FastAPI, HTTPException

from pydantic import BaseModel, Field

app = FastAPI()

users = []

class User(BaseModel):
    id: int = Field(ge=1, le=100, examples=[45])
    username: str = Field(min_length=5, max_length=20, description="Enter username", examples=["UrbanUser"])
    age: int = Field(ge=18, le=120, description="Enter age", examples=[24])


@app.get("/users")
async def get_users():
    return users


@app.post("/user/{username}/{age}")
async def create_user(user: User):
    if users:
        user.id = users[-1].id + 1
    else:
        user.id = 1
    users.append(user)
    return {"user": user}


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user: User):
    for us in users:
        if us.id == user.id:
            us.username = user.username
            us.age = user.age
            return {"user": user}
    raise HTTPException(status_code=400, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user: User):
    for us in users:
        if us.id == user.id:
            users.remove(us)
            return {"message": f"The user {user.id} is delete", "user": us}
    raise HTTPException(status_code=400, detail="User was not found")
