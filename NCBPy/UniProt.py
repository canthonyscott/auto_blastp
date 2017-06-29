import requests, xmltodict
import time
import pandas as pd


class UniProtQuery:

    def __init__(self):
        self.results = dict()
        self.status_code = 0
        self.response = 0
        self.full_url = 0

    def get_protein_sequence(self, query: str):

        url = 'http://www.uniprot.org/uniprot/'
        item = query

        params = dict(
            query="%s AND organism:9606" % item,
            format='xml',
            # include='organism,sequence,genes',
            limit=5,
            sort='score',
        )

        resp = requests.get(url=url, params=params)
        self.status_code = resp.status_code
        self.response = resp.text
        self.full_url = resp.url

        data = xmltodict.parse(resp.text)
        entrys = data['uniprot']['entry']

        # if only one result is found, use that result
        try:
            # sorted by score, take best match from results
            winner = entrys[0]
        except KeyError:
            winner = entrys

        sequence = winner['sequence']['#text']

        # remove new line chars from the string
        sequence = ''.join(sequence.split('\n'))
        name = winner['name']

        data = dict(
            sequence=sequence,
            name=name,
        )

        self.results = data

        return True
