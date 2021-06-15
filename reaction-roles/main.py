from flask import Flask
from flask_restful import Resource, Api

from models import db
from marsh import ma, MessageSchema

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
db.create_all()
db.init_app(app)
ma.init_app(app)

message_schema = MessageSchema()


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


api.add_resource(ReactionRoleMessage, 'message/')


if __name__ == '__main__':
    app.run(debug=True)