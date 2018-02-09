#!/usr/bin/env python2.7
from database_setup import Contacts
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_restful import Api, Resource
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import date

app = Flask(__name__)
api = Api(app)
admin = Admin(app)

engine = create_engine('postgresql:///farmerfire')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

admin.add_view(ModelView(contacts,session))

class LetterData(Resource):
    def get(self, id):
        return {"hello": "world"}

api.add_resource(LetterData,'/JSON/letterdata/<int:id>')

class Name(Resource):
    def get(self, fname, *kwargs):
        pass

api.add_resource(Name, '/JSON/name/<string:name>')



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/letters/<int:id>', methods=['GET'])
def letter(id):
    today = (str(date.today().strftime('%m/%d/%Y')))

    return render_template('letter_template.html', date=today)



if __name__ == '__main__':
    app.debug= True
    app.run(host='0.0.0.0', port=5000)
