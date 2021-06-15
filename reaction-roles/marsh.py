from flask_marshmallow import Marshmallow

from models import Message

ma = Marshmallow()


class MessageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Message

    id = ma.auto_field()
    guild_id = ma.auto_field()
    channel_id = ma.auto_field()
    message_id = ma.auto_field()
