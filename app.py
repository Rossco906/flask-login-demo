import os
from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse, request
from models.tag import TagModel

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'Bob'
api = Api(app)


@app.route('/')
def index():
    return render_template('home.html')

class Tag(Resource):
    def get(self, name):
        tag = TagModel.find_by_tagName(name)
        if tag:
            return tag.json()
        else:
            return {"message":"item not found"}, 404
    
    def post(self, name):
        if TagModel.find_by_tagName(name):
            return {"Message": f"An tag with name {name} already exists"}, 404
        tag = TagModel(name)
        try: 
            tag.save_to_db()
        except:
            return {"message" : "An error occurred inserting the item"}, 500
        return tag.json()



api.add_resource(Tag, "/tag/<name>")
if __name__ =='__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)

