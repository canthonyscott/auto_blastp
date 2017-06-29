#! /bin/bash

# export the sqlite database to file full
echo -e ".headers on\n.mode csv\n.output /data/results_full.csv\n SELECT * from antibodies;" | sqlite3 /data/antibody.db

# export simple file
echo -e ".headers on\n.mode csv\n.output /data/results_simple.csv\n SELECT clone, gene, sequence, filtered_species from antibodies;" | sqlite3 /data/antibody.db

