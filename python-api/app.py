from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import find_dotenv, load_dotenv
from os import environ as env


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Loading env variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Set up a connection to your MongoDB database using Motor
client = AsyncIOMotorClient(env.get("MONGO_CLIENT"))
user_collection = client["user-profiles"]


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

    # preferences = [
    #     "Artificial Intelligence",
    #     "UK Politics",
    #     "Russia-Ukraine War",
    # ]  # TODO: Look up the user's preferences in the DB

    projection = {"_id": 0, "preferences": 1}

    user_data = await user_collection.find_one({"username": "test"}, projection)

    preferences = user_data.get("preferences")

    # for testing purposes
    print(f"preferences: {preferences}")

    return preferences
