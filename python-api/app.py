from typing import Annotated

from dotenv import find_dotenv, load_dotenv
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from utils.db_connector import DBConnector

# Main backend app. Run with e.g. `uvicorn app:app --host 0.0.0.0 --port 7243` from
# within the `python-api` folder

# Loading env variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

conn = DBConnector()
user_collection = conn.get_user_collection()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # TODO implement OAuth2
    # TODO replace mytoken with the actual token
    return {"access_token": "mytoken", "token_type": "bearer"}


@app.get("/preferences")
async def get_preferences(token: Annotated[str, Depends(oauth2_scheme)]):
    # TODO: verify the token

    projection = {"_id": 0, "preferences": 1}

    user_data = await user_collection.find_one({"username": "test"}, projection)

    preferences = user_data.get("preferences")

    # for testing purposes
    print(f"preferences: {preferences}")

    return preferences


@app.post("/preference")
async def add_preference(
    token: Annotated[str, Depends(oauth2_scheme)], preference: str
):
    """Adds a preference for the logged in user to the DB"""
    await user_collection.update_one(
        {"username": "test"}, {"$push": {"$.preferences": preference}}
    )


@app.delete("/preference")
async def add_preference(
    token: Annotated[str, Depends(oauth2_scheme)], preference: str
):
    """Removes a preference for the logged in user from the DB"""
    await user_collection.update_one(
        {"username": "test"}, {"$pull": {"$.preferences": preference}}
    )
