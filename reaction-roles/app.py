import os
import uuid

from flask import Flask
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

#from models import db
#from marsh import ma, MessageSchema

POSTGRES_URI = (
    f"postgresql://{os.environ.get('POSTGRES_USER', 'postgres')}:"
    f"{os.environ.get('POSTGRES_PASSWORD', 'postgres')}@"
    f"{os.environ.get('POSTGRES_HOST', 'localhost')}:"
    f"{os.environ.get('POSTGRES_PORT', '5432')}/"
    f"{os.environ.get('POSTGRES_DATABASE', 'reaction_roles')}"
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URI
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

## DATABASE MODELS ##


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


## MARSHMALLOW SCHEMAS ##


class MessageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Message

    id = ma.auto_field()
    guild_id = ma.auto_field()
    channel_id = ma.auto_field()
    message_id = ma.auto_field()


db.create_all()
message_schema = MessageSchema()

## API ENDPOINTS ##


class ReactionRoleMessage(Resource):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        try:
            data = message_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        db.session.add(data)
        db.session.commit()
        return message_schema.dump(data)


api.add_resource(ReactionRoleMessage, '/message/')


if __name__ == '__main__':
    app.run(debug=True)