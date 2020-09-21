import math
import re

import pandas as pd
import requests

from config_params import BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN

# https://wwwdev.ebi.ac.uk/biosamples/samples?filter=attr:project:UKB_SYNTHETIC_DATA
# Number of submitted samples: 2504

CANCER_PERCENTAGE = 15
DIABETES_PERCENTAGE = 30
HEART_DISEASE_PERCENTAGE = 40
COVID_PERCENTAGE = 1
DIABETES_AND_HEART_DISEASE_PERCENTAGE = 50
DIABETES_AND_CANCER_PERCENTAGE = 2

DATA_FILE_NAME = "../resources/ukb_synthetic_data_tofu_updated.csv"

SKIP_ATTRIBUTES = [
    "Diagnoses - ICD10",
    "Diagnoses - main ICD10",
    "Diagnoses - secondary ICD10"
    "Type of cancer: ICD10 addendum",
    "Type of cancer: ICD9 addendum",
]


def main():
    update_samples()


def update_samples():
    sample_client = SamplesClient(BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN)
    jwt = sample_client.authenticate()
    syn_data = read_synthetic_data(DATA_FILE_NAME)
    sample_count = 0

    for index, row in syn_data.iterrows():
        sample = convert_to_sample_with_accession(row, DOMAIN)
        sample_client.submit_sample(sample, jwt)
        sample_count += 1

    print("Number of submitted samples: " + str(sample_count))


def read_synthetic_data(file_name):
    synthetic_data = pd.read_csv(file_name)
    return synthetic_data


def convert_to_sample_with_accession(row, domain) -> dict:
    sample_attributes = add_sample_attributes(row)

    ega_dataset_ref = {
        "url": "https://ega-archive.org/datasets/EGAD00001006308",
        "duo": ["DUO:0000004"]
    }
    ega_sample_ref = {
        "url": "https://ega-archive.org/metadata/v2/samples/" + row["EGA sample id"]
    }

    sample = {
        "accession": row["Accession"],
        "name": row["Sample name"],
        "domain": domain,
        "release": "2010-01-17T00:00:00Z",
        "characteristics": sample_attributes,
        "relationships": [],
        "externalReferences": [ega_dataset_ref, ega_sample_ref],
        "organization": [],
        "contact": [],
        "publications": []
    }

    return sample


def add_sample_attributes(row) -> dict:
    sample_attributes = dict()
    sample_attributes["project"] = [{"text": "UKB_SYNTHETIC_DATA"}]
    sample_attributes["description"] = [
        {"text": "Synthetic samples generated using statistical distribution of UKB as a part of CINECA project"}]
    sample_attributes["organism"] = [{"text": "Homo sapiens",
                                      "ontologyTerms": ["http://purl.obolibrary.org/obo/NCBITaxon_9606"]}]

    for index, value in row.iteritems():
        attribute_name = get_attribute_name(index)

        if index == "Sample name" or index == "Accession" or index == "EGA sample id" or not value:
            continue

        if isinstance(value, float) and math.isnan(value):
            continue

        if index == "eid":
            sample_attributes["alias"] = [{"text": value}]
            continue

        # add phenotype with ontologies
        if index == "phenotype":
            if value == "Diabetes mellitus":
                sample_attributes["phenotype"] = [{"text": "Diabetes mellitus",
                                                   "ontologyTerms": ["http://purl.obolibrary.org/obo/HP_0000819"]}]
            elif value == "Neoplasm":
                sample_attributes["phenotype"] = [{"text": "Neoplasm",
                                                   "ontologyTerms": ["http://purl.obolibrary.org/obo/HP_0002664"]}]
            elif value == "Myocardial infarction":
                sample_attributes["phenotype"] = [{"text": "Myocardial infarction",
                                                   "ontologyTerms": ["http://purl.obolibrary.org/obo/HP_0001658"]}]
            else:
                sample_attributes["phenotype"] = [{"text": value}]

            continue

        # add sex with ontologies
        if index == "Sex":
            if value == "female":
                sample_attributes["sex"] = [{"text": "female",
                                             "ontologyTerms": ["http://purl.obolibrary.org/obo/PATO_0000383"]}]
            elif value == "male":
                sample_attributes["sex"] = [{"text": "male",
                                             "ontologyTerms": ["http://purl.obolibrary.org/obo/PATO_0000384"]}]
            else:
                sample_attributes["sex"] = [{"text": value}]

            continue

        # Only add attribute onetime to skip array and instance indexes
        if attribute_name in sample_attributes:
            continue

        # skip these attributes
        if attribute_name in SKIP_ATTRIBUTES:
            continue

        sample_attributes[attribute_name] = [{"text": value}]

    return sample_attributes


def get_attribute_name(attribute):
    return re.sub("-[0-9]+\\.[0-9]+", "", str(attribute))


class SamplesClient:

    def __init__(self, biosamples_url, aap_url, username, password, domain):
        self.biosamples_url = biosamples_url
        self.aap_url = aap_url
        self.username = username
        self.password = password
        self.domain = domain

    def authenticate(self):
        r = requests.get(self.aap_url, auth=(self.username, self.password))
        if r.status_code == requests.codes.ok:
            return r.text
        else:
            raise r.raise_for_status()

    def get_sample(self, accession):
        sample_get_url = self.biosamples_url + "/biosamples/samples" + accession + "?curationdomain="
        response = requests.get(sample_get_url)
        if response.status_code == requests.codes.ok:
            sample = response.json()
        else:
            sample = None
            print("Failed to get sample: " + accession)

        return sample

    def submit_sample(self, sample, jwt):
        sample_submit_endpoint = self.biosamples_url + "/biosamples/samples"

        header = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/hal+json",
            "Authorization": "Bearer " + jwt
        }

        if "accession" in sample:
            sample_submit_endpoint = sample_submit_endpoint + "/" + sample["accession"]
            response = requests.put(sample_submit_endpoint, headers=header, json=sample)
        else:
            response = requests.post(sample_submit_endpoint, headers=header, json=sample)

        if response.status_code == requests.codes.created or response.status_code == requests.codes.accepted:
            print("Submitted to biosamples: " + response.text)
        else:
            print("Failed to submit sample: " + sample["name"])

        return response.json()["accession"]


if __name__ == '__main__':
    main()
