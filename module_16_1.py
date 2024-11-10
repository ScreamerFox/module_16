from fastapi import FastAPI

app = FastAPI()


@app.get("/user/admin")
async def admin() -> dict:
    return {"message": "Вы вошли как администратор"}

@app.get("/user/{user_id}")
async def users(user_id: int) -> dict:
    return {"message": f"Вы  вошли как пользователь №{user_id}"}

@app.get("/user/")
async def user_info(name: str, age: int) -> dict:
    return {"message": f"Информация о пользователе. Имя: {name}, Возраст: {age}"}

@app.get("/")
async def homepage() -> dict:
    return {"message": "Главная страница"}
