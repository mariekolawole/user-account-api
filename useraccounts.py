from datetime import date
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from schemas import User, load_users, save_users, UserCreate, UserUpdate

app = FastAPI()

db = load_users()

@app.get("/users", responses={200: {"model": List[User], "description": "A list of user accounts"}})
async def list_users() -> List[User]:
    """
    Retrieves a list of user accounts
    """
    return db

@app.post("/users", responses={201: {"model": User, "description": "User account created successfully"}})
async def create_user(user: UserCreate) -> User:
    """
    Create a new user account
    """
    new_user = User(id=len(db) + 1, **user.model_dump())
    db.append(new_user)
    save_users(db)
    return new_user


@app.get("/users/{userId}", responses={200: {"model": User, "description": "A user account"}, 404: {"description": "User not found"}})
async def get_user(user_id: int) -> User:
    """
    Retrieve a user account by ID
    """

    for user in db:
        if user.id == user_id:
          return user

    raise HTTPException(status_code=404, detail=f"No user with id={user_id}.")


@app.put("/users/{userId}", responses={200: {"model": User, "description": "User account updated  successfully"}, 404: {"description": "User not found"}})
def update_user(user_id: int, updated_user: UserUpdate) -> User:
    """
    Update an existing user account
    """

    for i, user in enumerate(db):
        if user.id == user_id:
            db[i] = User( id=user_id, **updated_user.model_dump())
            save_users(db)
            return db[i]

    raise HTTPException(status_code=404, detail=f"No user with id={user_id}.")


if __name__ == "__main__":
    uvicorn.run("useraccounts:app", reload=True)