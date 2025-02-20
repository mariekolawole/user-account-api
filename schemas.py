import json
import pprint
from datetime import date

from pydantic import BaseModel, Field, StrictStr, StrictInt
from typing_extensions import ClassVar, List


class UserBase(BaseModel):
    """
    User Base Model
    """
    email: StrictStr = Field(description="The user's email address")
    name: StrictStr = Field(description="The user's name")
    date_of_birth: date = Field(description="The user's date of birth")
    postcode: StrictStr = Field(description="The user's postcode")

    __properties: ClassVar[List[str]] = ["id", "email", "name", "date_of_birth", "postcode"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
        }

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.model_dump())

    def to_json(self) -> str:
        """Returns the JSON representation of the model"""
        return json.dumps(self.to_dict())


class User(UserBase):
    """
    User
    """
    id: StrictInt = Field(description="Unique identifier for the user")


class UserCreate(UserBase):
    """
    UserCreate
    """
    pass

class UserUpdate(UserBase):
    """
    UserUpdate
    """
    pass


def load_users() -> List[User]:
    """Load a list of User objects from a JSON file"""
    try:
        with open("users.json") as f:
            return [User.model_validate(obj) for obj in json.load(f)]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users: List[User]):
    with open("users.json", 'w') as f:
        json.dump([user.model_dump() for user in users], f, indent=4)
