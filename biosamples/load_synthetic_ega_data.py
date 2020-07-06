import random

import requests
import pandas as pd
import re

from config_params import BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN, ACCESSION_FILE_PATH


CANCER_PERCENTAGE = 15
DIABETES_PERCENTAGE = 30
HEART_DISEASE_PERCENTAGE = 40
COVID_PERCENTAGE = 1
DIABETES_AND_HEART_DISEASE_PERCENTAGE = 50
DIABETES_AND_CANCER_PERCENTAGE = 2

CANCER_IDS = [84, 40021, 40019, 40009, 40005, 40008, 40006, 40016, 40013, 40011, 40017, 40012]
DIABETES_IDS = [2976, 2966, 131682, 131683, 131684, 131685, 2443, 2976, 30870, 30690, 30760, 30780, 41270, 41202, 41204]
HEART_DISEASE_IDS = [41270, 41204, 41270]


sample_request = {
    "name": "sample_name",
    "domain": "self.domain",
    "release": "2020-01-17T00:00:00Z",
    "characteristics": [],
    "relationships": [],
    "externalReferences": [],
    "organization": [],
    "contact": [],
    "publications": []
}


def main():
    sample_client = SamplesClient(BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN)
    jwt = sample_client.authenticate()
    file_name = "../resources/synthetic-20200616154603.csv"
    syn_data = read_synthetic_data(file_name)
    sample_count = 0
    for index, row in syn_data.iterrows():
        sample = convert_to_sample(row, DOMAIN)
        sample_client.submit_sample(sample, jwt)
        sample_count += 1

    print("Number of submitted samples: " + str(sample_count))


def read_synthetic_data(file_name):
    synthetic_data = pd.read_csv(file_name)
    return synthetic_data


def convert_to_sample(row, domain) -> dict:
    sample_attributes = add_sample_attributes(row)

    sample = {
        "name": row["eid"],
        "domain": domain,
        "release": "2010-01-17T00:00:00Z",
        "characteristics": sample_attributes,
        "relationships": [],
        "externalReferences": [],
        "organization": [],
        "contact": [],
        "publications": []
    }
    return sample


def add_sample_attributes(row) -> dict:
    diabetes = should_generate(DIABETES_PERCENTAGE)
    cancer = should_generate(CANCER_PERCENTAGE)
    heart_disease = should_generate(HEART_DISEASE_PERCENTAGE)
    covid = should_generate(COVID_PERCENTAGE)

    sample_attributes = dict()
    name = ""
    for index, value in row.iteritems():
        if index == "eid":
            sample_attributes["name"] = value
            name = value # todo remove this after checking name assignment
        else:
            attribute_name = get_attribute_name(index)
            if diabetes:
                print("Should add diabetic values")
            if cancer:
                print("Should add cancer values")
            if heart_disease:
                print("Should add heart disease values")
            if covid:
                print("Should add covid values")

            if attribute_name not in sample_attributes:
                sample_attributes[attribute_name] = [{"text": value}]
            # else:
            #     sample_attributes[attribute_name].append({"text": value})

    sample_attributes["project"] = [{"text": "UKBB"}]


    return sample_attributes


def get_attribute_name(attribute):
    return re.sub("-[0-9]+\\.[0-9]+", "", str(attribute))

def should_generate(percentage):
    return random.randrange(100) <= percentage


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

    def submit_sample(self, sample, jwt):
        sample_submit_endpoint = self.biosamples_url + "/biosamples/samples"

        header = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/hal+json",
            "Authorization": "Bearer " + jwt
        }

        response = requests.post(sample_submit_endpoint, headers=header, json=sample)
        if response.status_code == requests.codes.created:
            print("Submitted to biosamples: " + response.text)
        else:
            print("Failed to submit sample: " + sample["name"])


if __name__ == '__main__':
    main()
