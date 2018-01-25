#!/usr/bin/env python2.7
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base= declarative_base()

class Contacts(Base):
    _tablename_ = 'contacts'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    first_name = Column(String(80), nullable= False)
    last_name = Column(String(80), nullable=False)


class Address(Base):
    _tablename_= 'address'
    id= Column(Integer, primary_key=True, autoincrement=True, unique=True)
    address = Column(String(80), nullable=False)
    contact_id = Column(Integer, ForeignKey('contact.id'))
    contact = relationship(Contacts, cascade="delete")

class Policy(Base):
    _tablename_='policy'
    id  = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    number = Column(Integer, nullable=False)
    effective_date= Column(Date, nullable=False)
    created = Column(Date, nullable=False)
    updated = Column (Date, nullable=False)
    contact_id = Column(Integer, ForeignKey('contact.id'))
    contact = relationship(Contacts, cascade="delete")

class PolicyType(Base):
    _tablename_ = 'policytype'
    id  = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    policy_name = Column(String(80), nullable = False)
    policy_id = Column(Integer, ForeignKey('policy.id'))
    policy = relationship(Policy, cascade="delete")

class Letter(Base):
    _tablename_= "letter"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(80), nullable= False)
    description = Column(String(200))
    text = Column(Text, nullable=False)
    policy_type = Column(Integer, ForeignKey('policytype.id'))
    policy = relationship(PolicyType, cascade="delete")


engine = create_engine('postgresql:///farmerfire')

Base.metadata.create_all(engine)
