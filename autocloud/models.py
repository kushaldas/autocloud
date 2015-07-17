# -*- coding: utf-8 -*-

import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import autocloud

Base = declarative_base()

class JobDetails(Base):
    __tablename__ = 'job_details'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

# Create an engine that stores data in the local directory
engine = create_engine(autocloud.SQLALCHEMY_URI)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
