from contextlib import asynccontextmanager
from datetime import date
from typing import List, Any, Coroutine, Sequence, Annotated

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from schemas import User, load_users, save_users, UserCreate, UserUpdate

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

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI(
    title="User Account API",
    lifespan=lifespan,
    description="API for managing user accounts with standard CRUD operations and JWT authentication. Endpoints (except for token generation) require a valid JWT provided via the Bearer scheme.",
    version="1.0.0")


@app.get("/users", responses={200: {"model": List[User], "description": "A list of user accounts"}})
async def list_users(session: Annotated[Session, Depends(get_session)]) -> Sequence[User]:
    """
    Retrieves a list of user accounts
    """
    query = select(User)
    return session.exec(query).all()


@app.post("/users", responses={201: {"model": User, "description": "User account created successfully"}})
async def create_user(session: Annotated[Session, Depends(get_session)], user: UserCreate) -> User:
    """
    Create a new user account
    """
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user) # updates the object with the database generated id
    return new_user


@app.get("/users/{userId}", responses={200: {"model": User, "description": "A user account"}, 404: {"description": "User not found"}})
async def get_user(session: Annotated[Session, Depends(get_session)], user_id: int) -> User:
    """
    Retrieve a user account by ID
    """
    users = select(User, User.id == user_id)
    user = session.exec(users).first()
    return user[0] if user else HTTPException(status_code=404, detail=f"No user with id={user_id}.")



@app.put("/users/{userId}", responses={200: {"model": User, "description": "User account updated  successfully"}, 404: {"description": "User not found"}})
async def update_user(session: Annotated[Session, Depends(get_session)], user_id: int, updated_user: UserUpdate) -> User:
    """
    Update an existing user account
    """
    user = session.get(User, user_id)
    if user:
        user.sqlmodel_update(updated_user)
        session.commit()
        session.refresh(user)
        return User.model_validate(user)
    else:
        raise HTTPException(status_code=404, detail=f"No user with id={user_id}.")


@app.delete("/users/{userId}", status_code=204, responses={204: {"description": "User account deleted successfully"}, 404: {"description": "User not found"}})
def delete_user(session: Annotated[Session, Depends(get_session)], user_id: int):
    """
    Delete a user account
    """
    user = session.get(User, user_id)
    if user:
         session.delete(user)
         session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No user with id={user_id}.")

if __name__ == "__main__":
    uvicorn.run("useraccounts:app", reload=True)