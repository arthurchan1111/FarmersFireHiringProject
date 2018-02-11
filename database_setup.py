#!/usr/bin/env python2.7
import sys
import psycopg2
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base= declarative_base()

class Contacts(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    first_name = Column(String(80), nullable= False)
    last_name = Column(String(80), nullable=False)

    @property
    def serialize(self):
        return{
            "first_name" : self.first_name,
            "last_name" : self.last_name

        }

class Policy(Base):
    __tablename__='policy'
    id  = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    number = Column(Integer, nullable=False, unique=True)
    effective_date= Column(Date, nullable=False)
    created = Column(Date, nullable=False)
    updated = Column (Date, nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    contact = relationship(Contacts, cascade="delete")

    @property
    def serialize(self):
        return{
            "policy_number" : self.number,
            "effective_date" : self.effective_date,
            "created": self.created,
            "updated": self.updated

        }

class Address(Base):
    __tablename__= 'address'
    id= Column(Integer, primary_key=True, autoincrement=True, unique=True)
    address = Column(String(80), nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    contact = relationship(Contacts, cascade="delete")
    policy_id = Column(Integer, ForeignKey('policy.id'))
    policy = relationship(Policy, cascade="delete")

    @property
    def serialize(self):
        return{
            "address" : self.address

        }

class PolicyType(Base):
    __tablename__ = 'policytype'
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
    __tablename__= "letter"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(80), nullable= False)
    description = Column(String(200))
    title = Column(String(80))
    text = Column(Text, nullable=False)
    policy_type = Column(String(80))



engine = create_engine('postgresql:///farmerfire')

Base.metadata.create_all(engine)
