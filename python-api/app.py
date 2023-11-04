from datetime import datetime, timedelta
from typing import List

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

from utils.article import Article
from utils.db_connector import DBConnector

# Main backend app. Run with e.g. `uvicorn app:app --host 0.0.0.0 --port 7243` from
# within the `python-api` folder

# Loading env variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = FastAPI()

conn = DBConnector()
user_collection = conn.get_user_collection()

DEFAULT_USER = "test"
MAX_DOCUMENTS_TO_QUERY_FROM_DB = 500


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


# TODO implement using single rank and dedup
@app.post("/generate-digest")
async def generate_digest():
    yesterday_ts = datetime.now() - timedelta(days=1)
    articles = fetch_articles_since(DEFAULT_USER, yesterday_ts)


# TODO implement using separate rank and dedup
@app.post("/generate-digest-chained")
async def generate_digest_chained():
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


### Helpers
async def fetch_articles_since(username: str, timestamp: datetime) -> List[Article]:
    user_email = get_email_from_username(username)
    articles_collection = conn.get_incoming_data_collection()
    cursor = articles_collection.find(
        {"email_recipient": user_email, "received_at": {"$gt": timestamp}}
    )
    articles = []
    for document in await cursor.to_list(length=MAX_DOCUMENTS_TO_QUERY_FROM_DB):
        print(document)
        articles.append(
            Article(
                document["raw_content"],
                document["extracted_content"],
                "HEADLINE_PLACEHOLDER",  # TODO parse the headline from the article
                "CONTENT_PLACEHOLDER",  # TODO parse the content from the article
            )
        )
    return articles


def get_email_from_username(username: str) -> str:
    # TODO: Fix by actually getting the email
    return "demo@rituai.email"
