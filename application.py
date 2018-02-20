#!/usr/bin/env python2.7
from database_setup import Base, Contacts, Address, Policy, PolicyType, Letter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, g
from flask import session as document_session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import date
import pdfkit



app = Flask(__name__)
admin = Admin(app)


engine = create_engine('postgresql:///farmerfire')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

admin.add_view(ModelView(Contacts, session))
admin.add_view(ModelView(Address, session))
admin.add_view(ModelView(Policy, session))
admin.add_view(ModelView(PolicyType, session))
admin.add_view(ModelView(Letter, session))

session.rollback()



@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        data= request.get_json()
        id= data["letter_id"]
        resultlist = data["data"]
        url_base= "http://localhost:5000/letters/"+str(id)+"?pnum="
        urls = []

        if str(resultlist[0]).isdigit():
            for x in range(len(resultlist)):
                urls.append(url_base + str(resultlist[x]))

            return jsonify(Url = urls)

        for x in range(len(resultlist)):
            address = session.query(Address).filter(Address.address == resultlist[x]).first()
            policy = session.query(Policy).filter(Policy.id == address.policy_id).first()
            urls.append(url_base + str(policy.number))

        return jsonify(Url = urls)


    else:
        general = session.query(Letter).filter(Letter.policy_type == "General").all()
        commercial = session.query(Letter).filter(Letter.policy_type == "Commercial").all()
        dwellers = session.query(Letter).filter(Letter.policy_type == "Dwellers Fire").all()
        home = session.query(Letter).filter(Letter.policy_type == "Homeowners").all()
        return render_template('index.html', general=general, commercial= commercial, dwellers=dwellers, home=home)


@app.route('/letters/<int:id>', methods=['GET', 'POST'])
def letter(id, **kwargs):
    pnum = request.args.get('pnum')
    document_session['pnum'] = pnum
    policy = session.query(Policy).filter(Policy.number == pnum).first()
    contact = session.query(Contacts).filter(Contacts.id == policy.contact_id).first()
    address = session.query(Address).filter(Address.policy_id == policy.id).first()
    address_heading = address.address.split(",", 1)
    policy_type = session.query(PolicyType).filter(PolicyType.policy_id == policy.id).first()
    today = (str(date.today().strftime('%m/%d/%Y')))
    letter = session.query(Letter).filter(Letter.id == id).one()
    return render_template('letter_template.html', id=id, date=today, letter=letter, policy=policy, contact = contact, address = address, policy_type = policy_type, address_heading = address_heading)

@app.route('/JSON/policy/<int:policy>')
def getPolicy(policy):
    try:
        policy = session.query(Policy).filter(Policy.number == policy).first()

        if policy:
            contact = session.query(Contacts).filter(
                Contacts.id == policy.contact_id).first()
            address = session.query(Address).filter(
                Address.policy_id == policy.id).first()
            policy_type = session.query(PolicyType).filter(
                PolicyType.policy_id == policy.id).first()
            return jsonify(Policy=[contact.serialize, address.serialize, policy.serialize, policy_type.serialize, "pn"])

        return make_response(jsonify({'error': 'Not found'}), 404)

    except:
        return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/JSON/contacts')
def getContacts():
    try:
        first_name = request.args.get("fname")
        last_name = request.args.get("lname")
        if last_name is None:
            contacts = session.query(Contacts).filter(Contacts.first_name == first_name).limit(100).all()
            return jsonify(Policy= iterContacts(contacts))

        else:
            contacts = session.query(Contacts).filter(Contacts.first_name == first_name).filter(Contacts.last_name == last_name).limit(100).all()
            return jsonify(Policy= iterContacts(contacts))

        return make_response(jsonify({'error': 'Not found'}), 404)

    except:
        return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/JSON/address/<string:address>')
def getAddress(address):
    try:
        address = session.query(Address).filter(
            Address.address == address).first()
        if address:
            contact = session.query(Contacts).filter(
                Contacts.id == address.contact_id).first()
            policy = session.query(Policy).filter(
                Policy.id == address.policy_id).first()
            policy_type = session.query(PolicyType).filter(
                PolicyType.policy_id == address.policy_id).first()
            return jsonify(Policy=[contact.serialize, address.serialize, policy.serialize, policy_type.serialize, "add"])
        return make_response(jsonify({'error': 'Not found'}), 404)

    except:
        return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/JSON/policytype/<string:ptype>')
def getPolicyType(ptype):
    try:

        policytype = session.query(PolicyType).filter(PolicyType.policy_type == ptype).limit(100).all()
        if len(policytype) > 0:
            policyTypes = []
            for x in range(len(policytype)):
                policyinfo = session.query(Policy).filter(Policy.id == policytype[x].policy_id).first()
                policy = {"policy": policytype[x].policy_type,
                          "policy_number": policyinfo.number}

                policyTypes.append(policy)

            policyTypes.append("pt")

            return jsonify(Policy=policyTypes)

        return make_response(jsonify({'error': 'Not found'}), 404)

    except:
        return make_response(jsonify({'error': 'Not found'}), 404)


def iterContacts(contactList):
    result = []
    if len(contactList) > 0:
        for x in range(len(contactList)):
            address = session.query(Address).filter(Address.contact_id == contactList[x].id).all()
            print address
            addresslist = [a.address for a in address]
            print addresslist
            contact = {"id": contactList[x].id,"first_name": contactList[x].first_name,
                        "last_name": contactList[x].last_name, "addresses": addresslist}
            result.append(contact)

        result.append("ct")
    return result



if __name__ == '__main__':
    app.debug = True,
    app.config['SECRET_KEY'] = 'super_secret_key'
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
