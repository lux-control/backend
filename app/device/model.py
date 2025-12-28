from app import mongo
from bson import ObjectId
from datetime import datetime
import uuid

class Device:
    def __init__(
            self,
            _id,
            min_lux,
            max_lux,
            certificate_string,
            created_at=None,
            channel_name=None
        ):
        self._id = _id or str(uuid.uuid4())
        self.min_lux = min_lux or 0
        self.max_lux = max_lux or 4000
        self.certificate_string = str(certificate_string)
        self.created_at = created_at or datetime.now()
        self.channel_name = str(channel_name) if channel_name else None
    
    def to_dict(self):
        return {
            "_id": self._id,
            "min_lux": self.min_lux,
            "max_lux": self.max_lux,
            "certificate_string": self.certificate_string,
            "created_at": self.created_at,
            "channel_name": self.channel_name
        }
    
    @staticmethod
    def from_mongo(data):
        return Device(
            _id = data.get("_id"),
            min_lux = data.get("min_lux"),
            max_lux = data.get("max_lux"),
            certificate_string=data.get("certificate_string"),
            created_at=data.get("created_at"),
            channel_name=data.get("channel_name")
        )
    
    def save(self, db):
        sensor = db.sensor.insert_one(self.to_dict())
        return self._id