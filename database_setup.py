#!/usr/bin/env python2.7
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base= declarative_base()

class Contacts(Base):
    _tablename_ = 'contacts'
    __table_args__ = {'extend_existing': True} 
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    first_name = Column(String(80), nullable= False)
    last_name = Column(String(80), nullable=False)

    @property
    def serialize(self):
        return{
            "first_name" : self.first_name,
            "last_name" : self.last_name

        }

class Address(Base):
    _tablename_= 'address'
    id= Column(Integer, primary_key=True, autoincrement=True, unique=True)
    address = Column(String(80), nullable=False)
    contact_id = Column(Integer, ForeignKey('contact.id'))
    contact = relationship(Contacts, cascade="delete")

    @property
    def serialize(self):
        return{
            "address" : self.address

        }

class Policy(Base):
    _tablename_='policy'
    id  = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    number = Column(Integer, nullable=False)
    effective_date= Column(Date, nullable=False)
    created = Column(Date, nullable=False)
    updated = Column (Date, nullable=False)
    contact_id = Column(Integer, ForeignKey('contact.id'))
    contact = relationship(Contacts, cascade="delete")

    @property
    def serialize(self):
        return{
            "policy_number" : self.number,
            "effective_date" : self.effective_date,
            "created": self.created,
            "updated": self.updated

        }

class PolicyType(Base):
    _tablename_ = 'policytype'
    id  = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    policy_type = Column(String(80), nullable = False)
    policy_id = Column(Integer, ForeignKey('policy.id'))
    policy = relationship(Policy, cascade="delete")

    @property
    def serialize(self):
        return{
            "policy_type" : self.policy_type,


        }

class Letter(Base):
    _tablename_= "letter"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(80), nullable= False)
    description = Column(String(200))
    title = Column(String(80))
    text = Column(Text, nullable=False)
    policy_type = Column(String(80))


    @property
    def serialize(self):
        return {
            "name": self.name,
            "description": self.description,
            "title" : self.title,
            "text": self.text,
            "policy_category": self.policy_type

        }


engine = create_engine('postgresql:///farmerfire')

Base.metadata.create_all(engine)
