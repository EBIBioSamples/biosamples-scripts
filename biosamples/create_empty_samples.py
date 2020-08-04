from datetime import datetime
import pandas as pd

from mongo_connector import MongoConnector
from config_params import DOMAIN

ACCESSION_FILE_PATH = "../resources/cineca_synthrtic_data.csv"


def main():
    sample_creator = MongoSampleCreator()
    release = datetime.utcnow()
    # sample_creator.create_empty_sample("SAMEA123890", "Fake1", DOMAIN, release)
    sample_creator.create_empty_samples(ACCESSION_FILE_PATH, DOMAIN, release)


class MongoSampleCreator:
    def __init__(self):
        self.mongo_connector = MongoConnector()

    def create_empty_samples(self, accession_file_path, domain, release):
        accessions, names = self.get_accessions(accession_file_path)
        for index, accession in enumerate(accessions):
            self.create_empty_sample(accession, names[index], domain, release)

    def create_empty_sample(self, accession, name, domain, release):
        sample = {"_id": accession,
                  "_class": "uk.ac.ebi.biosamples.mongo.model.MongoSample",
                  "name": name,
                  "domain": domain,
                  "release": release,
                  "update": release,
                  "attributes": [],
                  "relationships": [],
                  "externalReferences": [],
                  "organizations": [],
                  "contacts": [],
                  "publications": [],
                  "data": [],"submittedVia" : "JSON_API"
                  }

        accession = self.mongo_connector.upsert_sample(sample)
        print(accession)

    @staticmethod
    def get_accessions(accessions_file_path):
        print("Reading accessions from: " + accessions_file_path)
        pd_accessions = pd.read_csv(accessions_file_path, delimiter=",")
        return pd_accessions["PROVATE_BIOSAMPLE_ID"].tolist(), pd_accessions["SAMPLE_ID"].tolist()


if __name__ == '__main__':
    main()
