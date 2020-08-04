import random
import re

import pandas as pd
import requests

from config_params import BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN

# https://wwwdev.ebi.ac.uk/biosamples/samples?filter=attr:project:UKB_SYNTHETIC_DATA
# Number of submitted samples: 2504
# Diabetes percentage = 30.830670926517573
# Cancer percentage = 14.81629392971246
# Heart disease percentage = 39.77635782747604
# Diabetes + Cancer percentage = 4.073482428115016
# Diabetes + Heart disease percentage = 11.701277955271566
# Covid percentage = 1.7571884984025559.4

CANCER_PERCENTAGE = 15
DIABETES_PERCENTAGE = 30
HEART_DISEASE_PERCENTAGE = 40
COVID_PERCENTAGE = 1
DIABETES_AND_HEART_DISEASE_PERCENTAGE = 50
DIABETES_AND_CANCER_PERCENTAGE = 2

DATA_FILE_NAME = "../resources/ukb_synthetic_data_tofu.csv"
EGA_SUBJECT_ID_FILE = "../resources/ukb_ega_subject_ids.csv"
ACCESSION_FILE = "../resources/ukb_bsd_accessions.csv"
ACCESSION_FILE_PRIVATE = "../resources/cineca_synthrtic_data.csv"


DIABETES_VALUES = ["With coma",
                   "With ketoacidosis",
                   "With renal complications",
                   "With ophthalmic complications",
                   "With neurological complications",
                   "With peripheral circulatory complications",
                   "With other specified complications",
                   "With multiple complications",
                   "With unspecified complications",
                   "Without complications"]
HEART_DISEASE_VALUES = ["Acute transmural myocardial infarction of anterior wall2283",
                        "Acute transmural myocardial infarction of inferior wall2785",
                        "Acute transmural myocardial infarction of other sites341",
                        "Acute transmural myocardial infarction of unspecified site171",
                        "Acute subendocardial myocardial infarction2168",
                        "Acute myocardial infarction, unspecified4789",
                        "Subsequent myocardial infarction of anterior wall117",
                        "Subsequent myocardial infarction of inferior wall205",
                        "Subsequent myocardial infarction of other sites90",
                        "Subsequent myocardial infarction of unspecified site545",
                        "Haemopericardium as current complication following acute myocardial infarction1",
                        "Atrial septal defect as current complication following acute myocardial infarction4",
                        "Ventricular septal defect as current complication following acute myocardial infarction10",
                        "Rupture of cardiac wall without haemopericardium as current complication following acute myocardial infarction1",
                        "Rupture of papillary muscle as current complication following acute myocardial infarction2",
                        "Thrombosis of atrium, auricular appendage and ventricle as current complications following acute myocardial infarction5",
                        "Other current complications following acute myocardial infarction50",
                        "Coronary thrombosis not resulting in myocardial infarction319",
                        "Dressler's syndrome37",
                        "Other forms of acute ischaemic heart disease882",
                        "Acute ischaemic heart disease, unspecified1163",
                        "Atherosclerotic cardiovascular disease, so described91",
                        "Atherosclerotic heart disease26274",
                        "Old myocardial infarction12045",
                        "Aneurysm of heart165",
                        "Coronary artery aneurysm98",
                        "Ischaemic cardiomyopathy434",
                        "Silent myocardial ischaemia15",
                        "Other forms of chronic ischaemic heart disease9071",
                        "Chronic ischaemic heart disease, unspecified"]

DIABETES_ATTRIBUTES = ["Age diabetes diagnosed",
                       "Age high blood pressure diagnosed",
                       "Date K85 first reported (acute pancreatitis)",
                       "Source of report of K85 (acute pancreatitis)",
                       "Date K86 first reported (other diseases of pancreas)",
                       "Source of report of K86 (other diseases of pancreas)",
                       "Diabetes diagnosed by doctor",
                       "Age diabetes diagnosed",
                       "Triglycerides",
                       "Cholesterol",
                       "HDL",
                       "LDL"
                       ]
CANCER_ATTRIBUTES = ["Cancer year / age first occurred",
                     "Cancer record origin",
                     "Cancer record format",
                     "Reported occurrences of cancer",
                     "Date of cancer diagnosis",
                     "Age at cancer diagnosis",
                     "Type of cancer: ICD10",
                     "Type of cancer: ICD10 addendum",
                     "Type of cancer: ICD9",
                     "Histology of cancer tumour",
                     "Type of cancer: ICD9 addendum",
                     "Behaviour of cancer tumour"
                     ]
HEART_DISEASE_ATTRIBUTES = [
    # "Diagnoses - ICD10",
    # "Diagnoses - main ICD10",
    # "Diagnoses - secondary ICD10"
]
SKIP_ATTRIBUTES = [
    "Diagnoses - ICD10",
    "Diagnoses - main ICD10",
    "Diagnoses - secondary ICD10"
]

COVID_ATTRIBUTES = []

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

diabetes_count = 0
cancer_count = 0
heart_disease_count = 0
diabetes_cancer_count = 0
diabetes_heart_disease_count = 0
covid_count = 0


def main():
    # generate_samples()
    update_samples()
    # update_sample_ega_link()


def generate_samples():
    sample_client = SamplesClient(BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN)
    jwt = sample_client.authenticate()
    syn_data = read_synthetic_data(DATA_FILE_NAME)
    accessions = []
    sample_count = 0

    with open(EGA_SUBJECT_ID_FILE) as f:
        lines = f.read().splitlines()

    for index, row in syn_data.iterrows():
        sample = convert_to_sample(row, lines[index], DOMAIN)
        accession = sample_client.submit_sample(sample, jwt)
        accessions.append({"accession": accession, "subject_id": lines[index]})
        sample_count += 1

    pd_accessions = pd.DataFrame(accessions, columns=["accession", "subject_id"])
    with open(ACCESSION_FILE, 'w') as f:
        pd_accessions.to_csv(f, index=False)

    print("Number of submitted samples: " + str(sample_count))
    print("Diabetes percentage = " + str(diabetes_count * 100 / sample_count))
    print("Cancer percentage = " + str(cancer_count * 100 / sample_count))
    print("Heart disease percentage = " + str(heart_disease_count * 100 / sample_count))
    print("Diabetes + Cancer percentage = " + str(diabetes_cancer_count * 100 / sample_count))
    print("Diabetes + Heart disease percentage = " + str(diabetes_heart_disease_count * 100 / sample_count))
    print("Covid percentage = " + str(covid_count * 100 / sample_count))


def update_samples():
    sample_client = SamplesClient(BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN)
    jwt = sample_client.authenticate()
    syn_data = read_synthetic_data(DATA_FILE_NAME)
    sample_count = 0

    with open(EGA_SUBJECT_ID_FILE) as f:
        ega_subject_ids = f.read().splitlines()

    pd_accessions = pd.read_csv(ACCESSION_FILE_PRIVATE)
    accessions = pd_accessions["PROVATE_BIOSAMPLE_ID"].tolist()
    names = pd_accessions["SAMPLE_ID"].tolist()
    ega_sample_ids = pd_accessions["EGA_SAMPLE_ID"].tolist()

    ega_dataset_ref = {
        "url": "https://ega-archive.org/datasets/EGAD00001006308",
        "duo": ["DUO:0000005", "DUO:0000014", "DUO:0000019", "DUO:0000026", "DUO:0000028"]
    }

    for index, row in syn_data.iterrows():
        ega_sample_ref = {
            "url": "https://ega-archive.org/metadata/v2/samples/" + ega_sample_ids[index]
        }
        external_ref = [ega_dataset_ref, ega_sample_ref]

        sample = convert_to_sample_with_accession(row, accessions[index], names[index], ega_subject_ids[index], DOMAIN, external_ref)
        sample_client.submit_sample(sample, jwt)
        sample_count += 1

    print("Number of submitted samples: " + str(sample_count))
    print("Diabetes percentage = " + str(diabetes_count * 100 / sample_count))
    print("Cancer percentage = " + str(cancer_count * 100 / sample_count))
    print("Heart disease percentage = " + str(heart_disease_count * 100 / sample_count))
    print("Diabetes + Cancer percentage = " + str(diabetes_cancer_count * 100 / sample_count))
    print("Diabetes + Heart disease percentage = " + str(diabetes_heart_disease_count * 100 / sample_count))
    print("Covid percentage = " + str(covid_count * 100 / sample_count))


def update_sample_ega_link():
    sample_client = SamplesClient(BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN)
    jwt = sample_client.authenticate()

    with open(ACCESSION_FILE) as f:
        lines = f.read().splitlines()

    for accession in lines:
        sample = sample_client.get_sample(accession)
        sample["externalLinks"] = []


def read_synthetic_data(file_name):
    synthetic_data = pd.read_csv(file_name)
    return synthetic_data


def convert_to_sample(row, subject_id, domain) -> dict:
    sample_attributes = add_sample_attributes(row, subject_id)

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


def convert_to_sample_with_accession(row, accession, name, subject_id, domain, external_ref) -> dict:
    sample_attributes = add_sample_attributes(row, subject_id)

    sample = {
        "accession": accession,
        "name": name,
        "domain": domain,
        "release": "2010-01-17T00:00:00Z",
        "characteristics": sample_attributes,
        "relationships": [],
        "externalReferences": external_ref,
        "organization": [],
        "contact": [],
        "publications": []
    }

    return sample


def add_sample_attributes(row, subject_id) -> dict:
    diabetes = should_generate(DIABETES_PERCENTAGE)
    cancer = should_generate(CANCER_PERCENTAGE)
    heart_disease = should_generate(HEART_DISEASE_PERCENTAGE)
    covid = should_generate(COVID_PERCENTAGE)
    count_samples(diabetes, cancer, heart_disease, covid)

    sample_attributes = dict()
    for index, value in row.iteritems():
        if index == "eid" or not value:
            continue

        # Only add attribute onetime to skip array and instance indexes
        attribute_name = get_attribute_name(index)
        if attribute_name in sample_attributes:
            continue

        # skip these attributes and later add manually
        if attribute_name in SKIP_ATTRIBUTES:
            continue

        if attribute_name in DIABETES_ATTRIBUTES:
            if diabetes:
                sample_attributes[attribute_name] = [{"text": value}]
            else:
                continue

        if attribute_name in CANCER_ATTRIBUTES:
            if cancer:
                sample_attributes[attribute_name] = [{"text": value}]
            else:
                continue

        if attribute_name in HEART_DISEASE_ATTRIBUTES:
            if heart_disease:
                sample_attributes[attribute_name] = [{"text": value}]
            else:
                continue

        if attribute_name in COVID_ATTRIBUTES:
            if covid:
                sample_attributes[attribute_name] = [{"text": value}]
            else:
                continue

        sample_attributes[attribute_name] = [{"text": value}]

    if diabetes:
        sample_attributes["phenotype"] = [{"text": "Diabetes mellitus",
                                           "ontologyTerms": ["http://purl.obolibrary.org/obo/HP_0000819"]}]

        random_value = random.choice(DIABETES_VALUES)
        sample_attributes["Diagnoses - ICD10"] = [{"text": random_value}]
        sample_attributes["Diagnoses - main ICD10"] = [{"text": random_value}]
        sample_attributes["Diagnoses - secondary ICD10"] = [{"text": random_value}]

    if cancer:
        sample_attributes["phenotype"] = [{"text": "Neoplasm",
                                           "ontologyTerms": ["http://purl.obolibrary.org/obo/HP_0002664"]}]

    if heart_disease:
        sample_attributes["phenotype"] = [{"text": "Myocardial infarction",
                                           "ontologyTerms": ["http://purl.obolibrary.org/obo/HP_0001658"]}]

        random_value = random.choice(HEART_DISEASE_VALUES)
        if "Diagnoses - ICD10" not in sample_attributes:
            sample_attributes["Diagnoses - ICD10"] = [{"text": random_value}]
        else:
            sample_attributes["Diagnoses - ICD10"].append({"text": random_value})
        if "Diagnoses - main ICD10" not in sample_attributes:
            sample_attributes["Diagnoses - main ICD10"] = [{"text": random_value}]
        else:
            sample_attributes["Diagnoses - main ICD10"].append({"text": random_value})
        if "Diagnoses - secondary ICD10" not in sample_attributes:
            sample_attributes["Diagnoses - secondary ICD10"] = [{"text": random_value}]
        else:
            sample_attributes["Diagnoses - secondary ICD10"].append({"text": random_value})

    if covid:
        sample_attributes["Records of Covid-19 test results"] = [{"text": str(random.randint(1, 5))}]

    sample_attributes["subject id"] = [{"text": subject_id}]
    sample_attributes["project"] = [{"text": "UKB_SYNTHETIC_DATA"}]
    sample_attributes["organism"] = [{"text": "Homo sapiens",
                                      "ontologyTerms": ["http://purl.obolibrary.org/obo/NCBITaxon_9606"]}]

    female = should_generate(50)
    if female:
        sample_attributes["sex"] = [{"text": "female",
                                    "ontologyTerms": ["http://purl.obolibrary.org/obo/PATO_0000383"]}]
    else:
        sample_attributes["sex"] = [{"text": "male",
                                     "ontologyTerms": ["http://purl.obolibrary.org/obo/PATO_0000384"]}]

    return sample_attributes


def get_attribute_name(attribute):
    return re.sub("-[0-9]+\\.[0-9]+", "", str(attribute))


def should_generate(percentage):
    return random.randrange(100) <= percentage


def count_samples(diabetes, cancer, heart_disease, covid):
    global diabetes_count
    global cancer_count
    global heart_disease_count
    global diabetes_cancer_count
    global diabetes_heart_disease_count
    global covid_count
    if diabetes:
        diabetes_count += 1
        if cancer:
            diabetes_cancer_count += 1
        if heart_disease:
            diabetes_heart_disease_count += 1
    if cancer:
        cancer_count += 1
    if heart_disease:
        heart_disease_count += 1
    if covid:
        covid_count +=1


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
