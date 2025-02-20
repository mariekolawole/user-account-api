from contextlib import asynccontextmanager
from datetime import date
from typing import List, Any, Coroutine, Sequence

import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from schema import User, load_users, save_users, UserCreate, UserUpdate

# Database Setup
# Defines the SQLite database file location
engine = create_engine("sqlite:///./database.db",
                       connect_args={"check_same_thread": False}, #sqlite specific, allows multiple threads to access the database file
                       echo=True #logging for sql queries
                       )


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine) # creates the database tables before requests are processed
    yield


app = FastAPI(
    title="User Account API",
    lifespan=lifespan,
    description="API for managing user accounts with standard CRUD operations and JWT authentication. Endpoints (except for token generation) require a valid JWT provided via the Bearer scheme.",
    version="1.0.0")


@app.get("/users", responses={200: {"model": List[User], "description": "A list of user accounts"}})
async def list_users() -> Sequence[User]:
    """
    Retrieves a list of user accounts
    """
    with Session(engine) as session:
        query = select(User)
        return session.exec(query).all()


@app.post("/users", responses={201: {"model": User, "description": "User account created successfully"}})
async def create_user(user: UserCreate) -> User:
    """
    Create a new user account
    """
    with Session(engine) as session: # wraps in db transaction
        new_user = User.model_validate(user)
        session.add(new_user)
        session.commit()
        session.refresh(new_user) # updates the object with the database generated id
        return new_user


@app.get("/users/{userId}", responses={200: {"model": User, "description": "A user account"}, 404: {"description": "User not found"}})
async def get_user(user_id: int) -> User:
    """
    Retrieve a user account by ID
    """
    users = select(User, User.id == user_id)
    with Session(engine) as session:
        user = session.exec(users).first()
        return user[0] if user else HTTPException(status_code=404, detail=f"No user with id={user_id}.")


#
# @app.put("/users/{userId}", responses={200: {"model": User, "description": "User account updated  successfully"}, 404: {"description": "User not found"}})
# async def update_user(user_id: int, updated_user: UserUpdate) -> User:
#     """
#     Update an existing user account
#     """
#
#     for i, user in enumerate(db):
#         if user.id == user_id:
#             db[i] = User( id=user_id, **updated_user.model_dump())
#             save_users(db)
#             return db[i]
#
#     raise HTTPException(status_code=404, detail=f"No user with id={user_id}.")
#
#
# @app.delete("/users/{userId}", status_code=204, responses={204: {"description": "User account deleted successfully"}, 404: {"description": "User not found"}})
# def delete_user(user_id: int):
#     """
#     Delete a user account
#     """
#
#     for i, user in enumerate(db):
#         if user.id == user_id:
#             db.pop(i)
#             save_users(db)
#             return
#
#     raise HTTPException(status_code=404, detail=f"No user with id={user_id}.")

if __name__ == "__main__":
    uvicorn.run("useraccounts:app", reload=True)