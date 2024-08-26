import motor.motor_asyncio
from info import AUTH_CHANNEL, DATABASE_URI

auth_channel = AUTH_CHANNEL

class JoinReqs:

    def __init__(self):
        global auth_channel
        if DATABASE_URI and auth_channel:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
            self.db = self.client["JoinReqs"]
            self.col = self.db[str(auth_channel)]
        else:
            self.client = None
            self.db = None
            self.col = None

    def isActive(self):
        return self.client is not None

    async def add_user(self, user_id, first_name, username, date):
        try:
            await self.col.insert_one({
                "_id": int(user_id),
                "user_id": int(user_id),
                "first_name": first_name,
                "username": username,
                "date": date
            })
        except Exception as e:
            logging.error("Error adding user: %s", str(e))

    async def get_user(self, user_id):
        return await self.col.find_one({"user_id": int(user_id)})

    async def get_all_users(self):
        return await self.col.find().to_list(None)

    async def delete_user(self, user_id):
        await self.col.delete_one({"user_id": int(user_id)})

    async def delete_all_users(self):
        await self.col.delete_many({})

    async def get_all_users_count(self):
        return await self.col.count_documents({})
