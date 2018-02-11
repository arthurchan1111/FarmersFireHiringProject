#!/usr/bin/env python2.7
from database_setup import Base, Contacts, Address, Policy, PolicyType, Letter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import date
import json

app = Flask(__name__)
admin = Admin(app)

engine = create_engine('postgresql:///farmerfire')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

admin.add_view(ModelView(Contacts,session))
admin.add_view(ModelView(Address,session))
admin.add_view(ModelView(Policy,session))
admin.add_view(ModelView(PolicyType,session))
admin.add_view(ModelView(Letter,session))

session.rollback()



@app.route('/', methods=['GET'])
def index():
    letter_categories = session.query(Letter.policy_type).distinct().all()
    print letter_categories[0].policy_type
    return render_template('index.html', letter_categories= letter_categories)

@app.route('/letters/<int:id>', methods=['GET'])
def letter(id):
    today = (str(date.today().strftime('%m/%d/%Y')))
    letter = session.query(Letter).filter(Letter.id == id).one()
    return render_template('letter_template.html', date=today, letter=letter)

@app.route('/JSON/policy/<int:policy>')
def getPolicy(policy):
    try:
        policy = session.query(Policy).filter(Policy.number == policy).first()

        if policy:
            contact = session.query(Contacts).filter(Contacts.id == policy.contact_id).first()
            address = session.query(Address).filter(Address.policy_id == policy.id).first()
            policy_type = session.query(PolicyType).filter(PolicyType.policy_id == policy.id).first()
            return jsonify(Policy=[contact.serialize,address.serialize,policy.serialize,policy_type.serialize])

        return json.dumps({"error": "No match found"})

    except:
        return json.dumps({"error": "No match found"})

@app.route('/JSON/contacts/<string:name>')
def getContacts(name):
    full_name = name.split("_")
    try:
        contacts = session.query(Contacts).filter(Contacts.first_name == full_name[0]).filter(Contacts.last_name == full_name[1]).limit(100).all()
        if len(contacts) > 0:
            for x in range(len(contacts)):
                address = session.query(Address).filter(Address.contact_id == contacts[x].id).limit(10).all()
                track.append(contacts[x])

            return jsonify(Stuff= track)
                 
        return json.dumps({"error": "No match found"})

    except:
        return json.dumps({"error": "No match found"})

@app.route('/JSON/address/<string:address>')
def getAddress(address):
    try:
        address = session.query(Address).filter(Address.address == address).first()
        if address:
            contact = session.query(Contacts).filter(Contacts.id == address.contact_id).first()
            policy = session.query(Policy).filter(Policy.id == address.policy_id).first()
            policy_type = session.query(PolicyType).filter(PolicyType.policy_id == address.policy_id).first()
            return jsonify(Policy=[contact.serialize,address.serialize,policy.serialize,policy_type.serialize])
        return json.dumps({"error": "No match found"})

    except:
        return json.dumps({"error": "No match found"})

@app.route('/JSON/policytype/<string:ptype>')
def getPolicyType(ptype):
    try:
        policytype= session.query(PolicyType).filter(PolicyType.policy_type == ptype.title()).limit(100).all()
        if len(policytype) == 0:
            return json.dumps({"error": "No match found"})

        print policytype[0].policy_id
        return "hey"

    except:
        return json.dumps({"error": "No match found"})

@app.route('/JSON/advanced/<data>')
def advancedSearch():
    pass


if __name__ == '__main__':
    app.debug= True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
