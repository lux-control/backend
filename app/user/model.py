from app import mongo
from bson import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User:
    def __init__(
        self,
        device_id,
        email,
        username,
        password,
        created_at=None,
        _id=None,
    ):
        self._id = _id
        self.device_id = str(device_id) if device_id else None
        self.email = email
        self.username = username
        self.password = password
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        doc = {
            "device_id": self.device_id,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "created_at": self.created_at,
        }

        if self._id:
            doc["_id"] = ObjectId(self._id) if isinstance(self._id, str) else self._id

        return doc

    @staticmethod
    def from_mongo(data):
        return User(
            device_id=data.get("device_id"),
            email=data.get("email"),
            username=data.get("username"),
            password=data.get("password"),
            created_at=data.get("created_at"),
            _id=data.get("_id"),
        )

    @staticmethod
    def get_by_id(db, user_id):
        if not user_id:
            return None
        try:
            oid = user_id if isinstance(user_id, ObjectId) else ObjectId(str(user_id))
        except Exception:
            return None

        user_data = db.users.find_one({"_id": oid})
        return User.from_mongo(user_data) if user_data else None
    
    @staticmethod
    def get_by_email(db, email):
        user_data = db.users.find_one({"email": email})
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
        self._id = user.inserted_id
        return str(self._id)