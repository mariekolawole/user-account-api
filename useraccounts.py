from datetime import date
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from schemas import User, load_users, save_users
app = FastAPI()

db = load_users()

@app.get("/users", responses={200: {"model": List[User], "description": "A list of user accounts"}})
async def list_users() -> List[User]:
    """
    Retrieves a list of user accounts
    """
    return db

@app.get("/users/{userId}")
async def get_user(user_id: int):
    """
    Retrieve a user account by ID
    """
    result = None

    for user in db:
        if user["id"] == user_id:
           result=user

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail=f"No user with id={user_id}.")


if __name__ == "__main__":
    uvicorn.run("useraccounts:app", reload=True)