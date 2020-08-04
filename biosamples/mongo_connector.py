from enum import Enum

from pymongo import MongoClient

from config_params import DB_URL, DB_USERNAME, DB_PASSWORD


class MongoCollections(Enum):
    CURATION_LINK = 'mongoCurationLink'
    SAMPLE = 'mongoSample'


class MongoConnector:
    def __init__(self):
        if DB_USERNAME:
            self.client = MongoClient(DB_URL, username=DB_USERNAME, password=DB_PASSWORD,
                                      authSource='admin', authMechanism='SCRAM-SHA-1')
        else:
            self.client = MongoClient(DB_URL)
        self.db = self.client.biosamples

    def get_curation_records(self):
        curations = self.db[MongoCollections.CURATION_LINK.value].find()
        for curation in curations:
            yield curation

    def get_samples(self, find_query):
        samples = self.db[MongoCollections.SAMPLE.value].find(find_query)
        for sample in samples:
            yield sample

    def get_sample(self, accession):
        find = {"_id": accession}
        return self.db[MongoCollections.SAMPLE.value].find_one(find)

    def update_sample(self, accession, field, value):
        find = {"_id": accession}
        update = {"$set": {field: value}}
        self.db[MongoCollections.SAMPLE.value].update_one(find, update)

    def create_sample(self, sample):
        return self.db[MongoCollections.SAMPLE.value].insert_one(sample, upsert=True).inserted_id

    def upsert_sample(self, sample):
        return self.db[MongoCollections.SAMPLE.value].replace_one({"_id": sample["_id"]}, sample, upsert=True)
