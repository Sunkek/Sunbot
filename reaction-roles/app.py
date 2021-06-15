import os
import uuid

from flask import Flask, request
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
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

## DATABASE MODELS ##


class Message(db.Model):
    guild_id = db.Column(db.BigInteger)
    channel_id = db.Column(db.BigInteger)
    message_id = db.Column(db.BigInteger, primary_key=True)
    
    def __repr__(self):
        return f"<RR embed {self.guild_id}/{self.channel_id}/{self.message_id}>"


class ReactionRole(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    emote = db.Column(db.String)
    role_id = db.Column(db.BigInteger)
    message_id = db.Column(db.BigInteger, db.ForeignKey("message.message_id"))
    message = db.relationship("Message", backref="reaction_roles")

    __table_args__ = (
        db.UniqueConstraint("emote", "role_id", "message_id", name="raction_role_uc"),
    )
    
    def __repr__(self):
        return f"<RR {self.emote} {self.role_id}>"


## MARSHMALLOW SCHEMAS ##


class MessageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Message

    message_id = ma.auto_field()
    guild_id = ma.auto_field()
    channel_id = ma.auto_field()


class ReactionRoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ReactionRole

    id = ma.auto_field()
    emote = ma.auto_field()
    role_id = ma.auto_field()
    message_id = ma.auto_field()


db.create_all()
message_schema = MessageSchema()
reaction_role_schema = ReactionRoleSchema()

## API ENDPOINTS ##


class ReactionRoleMessage(Resource):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        try:
            data = message_schema.load(json_data, session=db.session)
        except ValidationError as err:
            return err.messages, 422
        message = Message()
        message.guild_id = data["guild_id"]
        message.channel_id = data["channel_id"]
        message.message_id = data["message_id"]
        print(message.message_id)
        db.session.add(message)
        db.session.commit()
        print(message.message_id)
        result = message_schema.dump(Message.query.get(message.message_id))
        return {"message": "Reaction roles message created", "data": result}


class ReactionRole(Resource):
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        try:
            data = reaction_role_schema.load(json_data, session=db.session)
        except ValidationError as err:
            return err.messages, 422
        reaction_role = ReactionRole()
        reaction_role.emote = data["emote"]
        reaction_role.role_id = data["role_id"]
        reaction_role.message_id = data["message_id"]
        print(reaction_role.id)
        db.session.add(reaction_role)
        db.session.commit()
        print(reaction_role.id)
        result = reaction_role_schema.dump(ReactionRole.query.get(reaction_role.id))
        return {"message": "Reaction role created", "data": result}


api.add_resource(ReactionRoleMessage, '/api/v1/message/')
api.add_resource(ReactionRole, '/api/v1/reaction_role/')


if __name__ == '__main__':
    app.run(debug=True)