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

DEFAULT_USER = "test"


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/preferences")
async def get_preferences():
    # TODO: In the real world, use OAuth2, build login endpoint with JWT or
    # something, verify token, account management etc
    projection = {"_id": 0, "preferences": 1}
    user_data = await user_collection.find_one({"username": DEFAULT_USER}, projection)
    preferences = user_data.get("preferences")

    # for testing purposes
    print(f"preferences: {preferences}")
    return preferences


@app.post("/preference")
async def add_preference(preference: str):
    """Adds a preference for the logged in user to the DB"""
    await user_collection.update_one(
        {"username": DEFAULT_USER},
        {"$push": {"preferences": preference}},
    )


@app.delete("/preference")
async def add_preference(preference: str):
    """Removes a preference for the logged in user from the DB"""
    await user_collection.update_one(
        {"username": DEFAULT_USER}, {"$pull": {"preferences": preference}}
    )


@app.get("/feeds")
async def get_feeds():
    # TODO: In the real world, use OAuth2, build login endpoint with JWT or
    # something, verify token, account management etc
    projection = {"_id": 0, "feeds": 1}
    user_data = await user_collection.find_one({"username": DEFAULT_USER}, projection)
    feeds = user_data.get("feeds")

    # for testing purposes
    print(f"feeds: {feeds}")
    return feeds


@app.post("/feed")
async def add_feed(feed: str):
    """Adds a preference for the logged in user to the DB"""
    await user_collection.update_one(
        {"username": DEFAULT_USER},
        {"$push": {"feeds": feed}},
    )


@app.delete("/feed")
async def add_feed(feed: str):
    """Removes a preference for the logged in user from the DB"""
    await user_collection.update_one(
        {"username": DEFAULT_USER}, {"$pull": {"feeds": feed}}
    )


# TODO implement
@app.post("/generate-digest")
async def generate_digest():
    pass


@app.post("/upvote")
async def upvote_article(article_id: str):
    """Records an upvote by a user to an article"""
    await user_collection.update_one(
        {"username": DEFAULT_USER}, {"$push": {"upvotes": article_id}}
    )


@app.post("/downvote")
async def downvote_article(article_id: str):
    """Records an upvote by a user to an article"""
    await user_collection.update_one(
        {"username": DEFAULT_USER}, {"$push": {"downvotes": article_id}}
    )
