from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import os
import logging
from NCBPy.BLAST import ProteinBlast
import time

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# If using a AWS MySQL Database, uncomment and modify below
# engine = create_engine('mysql+pymysql://user:password@database.cvtmmkwukt6q.us-east-1.rds.amazonaws.com:3306/table', echo=False)

# If using local sqlite database, uncomment
engine = create_engine('sqlite:////data/antibody.db', echo=False)

Base = declarative_base()

# define database schema to hold data during the blast
class Antibodies(Base):
    __tablename__ = 'antibodies'
    id = Column(Integer, primary_key=True)
    clone = Column(String(100))
    gene = Column(String(10))
    sequence = Column(String(1000))
    rid = Column(String(50), nullable=True) # nullable because this data will be gathered
    species = Column(String(10000), nullable=True)
    filtered_species = Column(String(10000), nullable=True)

Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
logging.info("DB created")
