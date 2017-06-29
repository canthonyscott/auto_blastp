from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import os
import logging
from NCBPy.BLAST import ProteinBlast
from NCBPy.Filtering import Filtering
import time
import subprocess

print("Calling Init script")
subprocess.call(['/Init.sh'])
print("Init script completed")

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

logging.basicConfig(filename='data/BLAST_LOG.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

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
logging.info("DB connection established")

# creat function to retreive results from RIDs
def get_data_from_RIDS():
    # query RIDS
    logging.info("Attempting to get RID data from BLAST servers")
    rids = []
    query = session.query(Antibodies).filter(Antibodies.rid != None).filter(Antibodies.species == None).all()
    for record in query:
        rids.append(record.rid)
    logging.info("RIDS retreived from DB:")
    logging.info(rids)
    # get results and check if all are complete or failed
    blaster = ProteinBlast()
    blaster.retrieve_results(rids)
    logging.info("Blast jobs incomplete: " + str(blaster.jobs_remaning))

    while blaster.jobs_remaning:
        logging.info("Jobs remaining, sleeping 5 minutes and trying again...")
        time.sleep(300)
        blaster = ProteinBlast()
        blaster.retrieve_results(rids)

    logging.info("All jobs complete (as much as they can be). Moving on...")

    parsed_rids = blaster.get_parsed_rids()
    results = blaster.get_results()
    species = blaster.get_species(results, parsed_rids, filter_pct=0.9)

    # match up RID to database and save species
    logging.info("Updating database with species")
    for item in species:
        rid = item['rid']
        spec = item['species_list']
        spec = ';'.join(list(spec))

        entry = session.query(Antibodies).filter(Antibodies.rid == rid).one()
        entry.species = spec

        session.commit()

    logging.info("Completed batch, moving to next set")

# start with getting pending BLASTS
get_data_from_RIDS()

# start blasting remaning data
while True:
    query = session.query(Antibodies).filter(Antibodies.rid == None)
    query = query.all()[:5]

    # no records, table must be complete
    if len(query) < 1:
        logging.info("Query count is less than 1, I must be done")
        break

    logging.info("Query count: %d" % len(query))
    to_blast = []
    for record in query:
        to_blast.append(record.sequence)

    logging.info("Sequences to blast: ")
    logging.info(to_blast)

    blaster = ProteinBlast()
    blaster.blast(to_blast)

    rids = blaster.get_rids()

    for record, rid in zip(query, rids):
        record.rid = rid

    session.commit()
    logging.info("RIDS added to the database")

    # wait some time jobs blasts to perform
    logging.info("Sleeping 2 minutes...")
    time.sleep(120)

    # try to get data
    get_data_from_RIDS()


logging.info("Completed Table")

# takes all of the species and filter them. Add this data
logging.info("Filtering the species list")
results = session.query(Antibodies).all()
data = []
for result in results:
    data.append(result.species)
filtering = Filtering()
new_data = filtering.filter_list_data(data)

for result, individual in zip(results, new_data):
    result.filtered_species = individual

session.commit()
logging.info("Filtered species commited to the database")
logging.info("Generating CSV files for you.")
subprocess.call(['/Finish.sh'])
logging.info("I am finished. Goodbye!")
