#!/usr/bin/env python2.7
from database_setup import Base, Contacts, Address, Policy, PolicyType, Letter
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template,render_template_string, request, redirect, url_for, flash, jsonify, make_response, g
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
options = {
    'page-size': 'Letter',
    'margin-top': '1in',
    'margin-right': '1in',
    'margin-bottom': '1in',
    'margin-left': '1in',
    'encoding': "UTF-8",
    'user-style-sheet': 'letter.css',
    'custom-header' : [
        ('Accept-Encoding', 'gzip')
    ],
}


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
        print commercial
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

@app.route('/letters/<int:id>/edit', methods=['GET'])
def editLetter(id):
    editStatus = True
    pnum = document_session['pnum']
    policy = session.query(Policy).filter(Policy.number == pnum).first()
    contact = session.query(Contacts).filter(Contacts.id == policy.contact_id).first()
    address = session.query(Address).filter(Address.policy_id == policy.id).first()
    address_heading = address.address.split(",", 1)
    policy_type = session.query(PolicyType).filter(PolicyType.policy_id == policy.id).first()
    today = (str(date.today().strftime('%m/%d/%Y')))
    letter = session.query(Letter).filter(Letter.id == id).one()
    html_template_string = """
        <section class="container">
            <p class="text-right">Date: %s</p>
        </section>
        <section class="container">
            <address>%s %s<br>%s<br>%s</address>
        </section>
        <section class="container">
            <h4 class="text-center">%s</h4>
        </section>
          <p>Dear Insured: </p>
          <p>Our records indicate that under %s policy # %s we currently insure your dwelling located at the
        following address:</p>
          <p id="address">%s</p>
          %s
        <p>Respectfully,<br>The Farmers Fire Insurance Company </p>
    """% (today,contact.first_name.title(),contact.last_name.title(),address_heading[0].title(),address_heading[1].title(), letter.title, policy_type.policy_type.title(),str(policy.number),address.address.title(),letter.text)
    return render_template('edit.html', html=html_template_string, id=id)


@app.route('/letters/<int:id>/pdf', methods=['GET'])
def pdfLetter(id, **kwargs):
    pnum = document_session['pnum']
    css = ["static/bootstrap.min.css", "static/pdf.css"]
    policy = session.query(Policy).filter(Policy.number == pnum).first()
    contact = session.query(Contacts).filter(Contacts.id == policy.contact_id).first()
    address = session.query(Address).filter(Address.policy_id == policy.id).first()
    address_heading = address.address.split(",", 1)
    policy_type = session.query(PolicyType).filter(PolicyType.policy_id == policy.id).first()
    today = (str(date.today().strftime('%m/%d/%Y')))
    letter = session.query(Letter).filter(Letter.id == id).one()
    rendered_template = render_template('pdf.html', date=today, letter=letter, policy=policy, contact = contact, address = address, policy_type = policy_type, address_heading = address_heading)
    pdffile= pdfkit.from_string(rendered_template, False, options=options, css=css)

    response = make_response(pdffile)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response


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
                contact = session.query(Contacts).filter(Contacts.id == policyinfo.contact_id).first()
                address = session.query(Address).filter(Address.policy_id == policyinfo.id).first()
                policy = {"first_name": contact.first_name, "last_name": contact.last_name, "address": address.address,
                    "policy": policytype[x].policy_type, "policy_number": policyinfo.number}

                policyTypes.append(policy)

            policyTypes.append("pt")

            return jsonify(Policy=policyTypes)

        return make_response(jsonify({'error': 'Not found'}), 404)

    except:
        return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/JSON/advanced')
def advancedSearch():
    try:
        query_all = session.query(Contacts, Policy, Address, PolicyType).join(Policy, Policy.contact_id == Contacts.id).join(Address, and_(Address.contact_id == Contacts.id, Address.policy_id == Policy.id)).join(PolicyType, PolicyType.policy_id == Policy.id)
        arg_dict = {'first_name': request.args.get("fname"), "last_name": request.args.get("lname"), "address" : request.args.get("address"), "policy": request.args.get("pnum"), "policytype": request.args.get("ptype")}
        truthiness = {}
        response = []
        for keys in arg_dict.items():
            if keys[1]:
                truthiness[keys[0]]  = True

            else:
                truthiness[keys[0]]  = False


        valid_inputs = {k:v for k,v in truthiness.items() if v == True}
        valid_keys = valid_inputs.keys()

        if len(valid_keys) > 0:
            for x in range(len(valid_keys)):
                if(valid_keys[x] == 'first_name'):
                    query_all = query_all.filter(Contacts.first_name == request.args.get("fname"))

                if(valid_keys[x] == 'last_name'):
                    query_all = query_all.filter(Contacts.last_name == request.args.get("lname"))

                if(valid_keys[x]== 'address'):
                    query_all = query_all.filter(Address.address == request.args.get("address"))

                if(valid_keys[x] == 'policy'):
                    print "here"
                    query_all = query_all.filter(Policy.number == int(request.args.get("pnum")))

                if(valid_keys[x] == 'policytype'):
                    query_all = query_all.filter(PolicyType.policy_type == str(request.args.get("ptype")))

            get_filtered_list = query_all.all()

            if len(get_filtered_list) > 0 :
                for x in range(len(get_filtered_list)):
                    contact = {"id": get_filtered_list[x][0].id, "first_name": get_filtered_list[x][0].first_name,
                            "last_name": get_filtered_list[x][0].last_name, "policy_number": get_filtered_list[x][1].number,
                             "address": get_filtered_list[x][2].address, "policy": get_filtered_list[x][3].policy_type}

                    response.append(contact)

                response.append("adv")
                return jsonify(Policy = response)



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
