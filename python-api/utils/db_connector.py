import os

from motor.motor_asyncio import AsyncIOMotorClient


class DBConnector:
    DB_NAME_USER_PROFILES = "user-profiles"
    DB_NAME_INCOMING_DATA = "incoming-data"
    DB_NAME_GENERATED_DIGESTS = "generated-digests"

    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(os.environ.get("MONGO_CLIENT"))
        self.db = self.client["news-agent-database"]

    def get_user_collection(self):
        return self.db[DBConnector.DB_NAME_USER_PROFILES]

    def get_incoming_data_collection(self):
        return self.db[DBConnector.DB_NAME_INCOMING_DATA]

    def get_generated_digests_collection(self):
        return self.db[DBConnector.DB_NAME_GENERATED_DIGESTS]
