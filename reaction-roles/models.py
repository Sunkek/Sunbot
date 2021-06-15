from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()


class Message(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guild_id = db.Column(db.BigInteger)
    channel_id = db.Column(db.BigInteger)
    message_id = db.Column(db.BigInteger)

    __table_args__ = (
        db.UniqueConstraint("guild_id", "channel_id", "message_id", name='message_url_uc'),
    )
    
    def __repr__(self):
        return f"<RR embed {self.guild_id}/{self.channel_id}/{self.message_id}>"

        