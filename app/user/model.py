from app import mongo
from bson import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(
        self,
        device_id,
        username,
        password,
        created_at=None,
        _id=None,
    ):
        self._id = str(_id) if _id else None
        self.device_id = str(device_id) if device_id else None
        self.username = username
        self.password = password
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            "_id": self._id,
            "device_id": self.device_id,
            "username": self.username,
            "password": self.password,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_mongo(data):
        return User(
            device_id=data.get("device_id"),
            username=data.get("username"),
            password=data.get("password"),
            created_at=data.get("created_at"),
            _id=data.get("_id"),
        )

    @staticmethod
    def get_by_id(db, user_id):
        user_data = db.users.find_one({"_id": ObjectId(user_id)})
        return User.from_mongo(user_data) if user_data else None

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)

    def save(self):
        if self.password and not self.password.startswith("pbkdf2:sha256:"):
            self.password = self.hash_password(self.password)

        user = mongo.db.users.insert_one(self.to_dict())
        self._id = str(user.inserted_id)
        return self._id