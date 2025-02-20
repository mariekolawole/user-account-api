from datetime import date
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()

db = [
    {"id": 1, "email": "susan.bill@abc.com", "name": "Susan Bill", "date_of_birth": date(1979,2,25) , "postcode": "N1 5SS"},
    {"id": 2, "email": "joe.dill@abc.com", "name": "Joe Dill", "date_of_birth": date(1979,2,25), "postcode": "N1 5SS"},
    {"id": 3, "email": "sing.holl@dcf.com", "name": "Sing Holl", "date_of_birth": date(1987,8,15), "postcode": "N1 4RD"},
    {"id": 4, "email": "mike.mile@gmail.com", "name": "Mike Mile", "date_of_birth": date(1979,2,25), "postcode": "N13 8UJ"},
    {"id": 5, "email": "moe,mill@gmail.com", "name": "Moe Mill", "date_of_birth": date(1970,2,23), "postcode": "SW17 9JU"},
    {"id": 6, "email": "matt.link@yahoo.com", "name": "Matt Link", "date_of_birth": date(1959,2,12), "postcode": "W1 5RT"},
    {"id": 7, "email": "lue.pole@toys.com", "name": "Lue Pole", "date_of_birth": date(1969,2,5), "postcode": "SE1 8UJ"},
    {"id": 8, "email": "len.looop@gril.com", "name": "Len Loop", "date_of_birth": date(1973,3,10), "postcode": "E17 8OP"},
    {"id": 9, "email": "lan.thed@gmail.com", "name": "Lan Thed", "date_of_birth": date(1979,12,29), "postcode": "N1 5SS"}
]

@app.get("/users", responses={200: {"model": List[dict], "description": "A list of user accounts"}})
async def list_users() -> List[dict]:
    """
    Retrieves a list of user accounts
    """

    return db


@app.get("/users/{userId}", responses={200: {"model": dict, "description": "A user account"}, 404: {"description": "User not found"}})
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