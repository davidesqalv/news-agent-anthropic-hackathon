import json
import re
from datetime import datetime, timedelta
from typing import List, Optional

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from motor.motor_asyncio import AsyncIOMotorCollection

from services.article_merger.article_merger import ArticleMerger
from services.deduplication.deduplicator import Deduplicator
from services.profiles.user_profile import UserProfile
from services.rank_and_dedup.rank_and_dedup import RankAndDedup
from services.ranking.ranker import Ranker
from utils.article import Article
from utils.db_connector import DBConnector
from utils.metaculus_connector import MetaculusConnector

# Main backend app. Run with e.g. `uvicorn app:app --host 0.0.0.0 --port 8000` from
# within the `python-api` folder

# Loading env variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = FastAPI()

# CORS middleware stuff so that the frontend can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://rituai.com",
        "https://www.rituai.com",
    ],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = DBConnector()
user_collection = conn.get_user_collection()

DEFAULT_USER = "demo@rituai.email"
MAX_DOCUMENTS_TO_QUERY_FROM_DB = 500


async def update_user_fields(
    users: AsyncIOMotorCollection, username: str, update_fields: dict
):
    try:
        # Construct the update query
        update_query = {"$set": {}, "$push": {}}
        for key, value in update_fields.items():
            if isinstance(value, list):
                update_query["$push"][key] = {"$each": value}
            else:
                update_query["$set"][key] = value

        update_result = await users.update_one(
            {"username": username},
            update_query,
        )

        return update_result.modified_count > 0 or update_result.upserted_id is not None
    except Exception as e:
        print(f"error updating user {username}")
        print(e)
        return False


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


@app.post("/preferences")
async def add_preferences(preferences: List[str]):
    """Adds preferences for the logged in user to the DB"""
    await user_collection.update_one(
        {"username": DEFAULT_USER},
        {"$addToSet": {"preferences": {"$each": preferences}}},
    )


@app.delete("/preference")
async def delete_preference(preference: str):
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
    # await user_collection.update_one(
    #     {"username": DEFAULT_USER},
    #     {"$push": {"feeds": feed}},
    # )
    await update_user_fields(user_collection, DEFAULT_USER, {"feeds": [feed]})


@app.delete("/feed")
async def delete_feed(feed: str):
    """Removes a preference for the logged in user from the DB"""
    await user_collection.update_one(
        {"username": DEFAULT_USER}, {"$pull": {"feeds": feed}}
    )


def parse_articles(text):
    articles = []

    for match in re.finditer(r"(\d+)\.", text, re.DOTALL):
        number = match.group(1)
        title = ""
        summary = ""

        article = {"number": number, "title": title, "summary": summary}
        articles.append(article)

    return json.dumps(articles, indent=2)


@app.post("/generate-digest")
async def generate_digest():
    now = datetime.now()
    yesterday_ts = now - timedelta(days=1)
    user_email = get_email_from_username(DEFAULT_USER)
    articles = await fetch_articles_since(user_email, yesterday_ts)
    print("getting profile")
    profile = await fetch_user_profile(DEFAULT_USER)
    print("ranking and deduping")
    rank_and_dedup_service = RankAndDedup()
    output = rank_and_dedup_service.rank_and_deduplicate(
        list(map(lambda a: a.extracted_content, articles)), profile, 10
    )
    # For debugging
    print(output)
    digests_coll = conn.get_generated_digests_collection()
    await digests_coll.insert_one(
        {
            "username": DEFAULT_USER,
            "email": user_email,
            "generated_at": now,
            "digest": output,
        }
    )
    # return parse_articles(output)
    return output


# @app.get("/last-generated-digest")
# async def get_last_generated_digest():
#     digests_coll = conn.get_generated_digests_collection()
#     last_digest = await digests_coll.find_one(
#         {"username": DEFAULT_USER},
#         sort=[("generated_at", pymongo.DESCENDING)]
#     )
#     if last_digest:
#         return dumps(last_digest["digest"])
#     else:
#         return "No digest found"


@app.post("/generate-digest-chained")
async def generate_digest_chained():
    now = datetime.now()
    yesterday_ts = now - timedelta(days=1)
    user_email = get_email_from_username(DEFAULT_USER)
    articles = await fetch_articles_since(user_email, yesterday_ts)
    articles_raw = list(map(lambda a: a.extracted_content, articles))
    profile = await fetch_user_profile(DEFAULT_USER)
    dedup_service = Deduplicator()
    dedup_result = dedup_service.deduplicate(articles_raw)
    unique_articles = dedup_result.get_unique_articles(articles_raw)
    articles_to_dedup = dedup_result.get_duplicated_articles(articles_raw)
    merger = ArticleMerger()
    deduped_articles = list(map(lambda d: merger.merge_articles(d), articles_to_dedup))
    rank_service = Ranker()
    ranked_articles = rank_service.rank_articles_get_ranked_articles(
        deduped_articles + unique_articles, profile
    )
    # for Debugging
    print(ranked_articles)
    digests_coll = conn.get_generated_digests_collection()
    digests_coll.insert_one(
        {
            "username": DEFAULT_USER,
            "email": user_email,
            "timestamp": now,
            "digest_dict": dict(zip(range(len(ranked_articles)), ranked_articles)),
        },
    )


@app.post("/upvote")
async def upvote_article(article_id: str):
    """Records an upvote by a user to an article"""
    # await user_collection.update_one(
    #     {"username": DEFAULT_USER}, {"$push": {"upvotes": article_id}}
    # )

    await update_user_fields(user_collection, DEFAULT_USER, {"upvotes": [article_id]})


@app.post("/downvote")
async def downvote_article(article_id: str):
    """Records an upvote by a user to an article"""
    # await user_collection.update_one(
    #     {"username": DEFAULT_USER}, {"$push": {"downvotes": article_id}}
    # )
    await update_user_fields(user_collection, DEFAULT_USER, {"downvotes": [article_id]})


# @app.post("/schedule")
# async def add_user_schedule(is_daily: bool, reminder_time: str, day: str):
#     """Adds a preference for the logged in user to the DB"""
#     # await user_collection.update_one(
#     #     {"username": DEFAULT_USER},
#     #     {
#     #         "schedule": {
#     #             "is_daily": is_daily,
#     #             "reminder_time": reminder_time,
#     #             "day": day,
#     #         }
#     #     },
#     # )
#     await update_user_fields(
#         user_collection,
#         DEFAULT_USER,
#         {
#             "schedule": {
#                 "is_daily": is_daily,
#                 "reminder_time": reminder_time,
#                 "day": day,
#             }
#         },
#     )


@app.post("/schedule")
async def add_user_schedule(request: Request):
    payload = await request.json()
    print(payload)
    """Adds a preference for the logged in user to the DB"""
    # await user_collection.update_one(
    #     {"username": DEFAULT_USER},
    #     {
    #         "schedule": {
    #             "is_daily": payload["is_daily"],
    #             "reminder_time": payload["reminder_time"],
    #             "day": payload["day"],
    #         }
    #     },
    # )

    await update_user_fields(
        user_collection,
        DEFAULT_USER,
        {
            "schedule": {
                "is_daily": payload["is_daily"],
                "reminder_time": payload["reminder_time"],
                "day": payload["day"],
            }
        },
    )


### Helpers
async def fetch_articles_since(user_email: str, timestamp: datetime) -> List[Article]:
    articles_collection = conn.get_incoming_data_collection()
    cursor = articles_collection.find(
        {"email_recipient": user_email, "received_at": {"$gt": timestamp}}
    )
    articles = []
    for document in await cursor.to_list(length=MAX_DOCUMENTS_TO_QUERY_FROM_DB):
        articles.append(
            Article(
                document["raw_content"],
                document["extracted_content"],
                "HEADLINE_PLACEHOLDER",  # TODO parse the headline from the article
                "CONTENT_PLACEHOLDER",  # TODO parse the content from the article
            )
        )
    return articles


async def fetch_user_profile(username: str) -> UserProfile:
    user_data = await user_collection.find_one(
        {"username": username}, {"_id": 0, "preferences": 1}
    )
    preferences = user_data.get("preferences")
    return UserProfile(preferences)


def get_email_from_username(username: str) -> str:
    # TODO: Fix by actually getting the email
    return DEFAULT_USER


# TODO remove
m = MetaculusConnector()
qs = m.get_questions_from_category("bio", limit=2)
print(qs[0].title)
print(qs[0].id)
print(qs[1].title)
print(qs[1].id)
