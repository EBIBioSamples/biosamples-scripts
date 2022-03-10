import argparse
import sys

import requests
import json
import pandas as pd

from config_params import BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN

EGA_SAMPLE_URL = "https://ega-archive.org/metadata/v2/samples/"
EGA_FILE_PATH = "../resources/ega_public_import_accessions.csv"


def main():
    ega_ids = get_accessions(EGA_FILE_PATH)
    for ega_id in ega_ids:
        update_sample_record(ega_id)


def get_accessions(accessions_file_path):
    print("Reading accessions from: " + accessions_file_path)
    pd_accessions = pd.read_csv(accessions_file_path, delimiter="; ", )
    return pd_accessions["ACCESSION"].tolist()


def update_sample_record(ega_id):
    ega_sample = get_ega_sample(ega_id)
    gender = ega_sample['response']['result'][0]['gender']
    subject_id = ega_sample['response']['result'][0]['subjectId']
    phenotype = ega_sample['response']['result'][0]['phenotype']  # ignore for now
    biosample_id = ega_sample['response']['result'][0]['bioSampleId']

    bsd_sample = get_biosample(biosample_id)
    bsd_sample['release'] = "2021-05-10T02:06:08Z"
    if 'male' == gender.lower():
        bsd_sample['characteristics']['gender'] = [{
            "text": gender,
            "ontologyTerms": ["http://purl.obolibrary.org/obo/PATO_0000384"]
        }]
    elif 'female' == gender.lower():
        bsd_sample['characteristics']['gender'] = [{
            "text": gender,
            "ontologyTerms": ["http://purl.obolibrary.org/obo/PATO_0000383"]
        }]
    else:
        bsd_sample['characteristics']['gender'] = [{
            "text": gender
        }]

    bsd_sample['characteristics']['subjectId'] = [{
        "text": subject_id
    }]

    ega_dataset_id = get_ega_dataset_id(ega_id)
    if ega_dataset_id:
        duo_codes = get_duo_codes(ega_dataset_id)
        ega_dataset_link = "https://ega-archive.org/datasets/" + ega_dataset_id
    ega_sample_link = "https://ega-archive.org/metadata/v2/samples/" + ega_id
    add_sample_ega_link = True
    add_ega_dataset_link = True
    if 'externalReferences' in bsd_sample:
        for ref in bsd_sample['externalReferences']:
            if ref['url'] == ega_sample_link:
                add_sample_ega_link = False
            elif ega_dataset_id and ref['url'] == ega_dataset_link:
                add_ega_dataset_link = False
        external_ref = bsd_sample['externalReferences']
    else:
        external_ref = []
        bsd_sample['externalReferences'] = external_ref

    if add_sample_ega_link:
        external_ref.append({
            "url": ega_sample_link
        })
    if ega_dataset_id and add_ega_dataset_link:
        external_ref.append({
            "url": ega_dataset_link,
            "duo": duo_codes
        })

    update_sample(bsd_sample)


def get_ega_dataset_id(egan_id):
    url = "https://ega-archive.org/metadata/v2/datasets?queryBy=sample&queryId=" + egan_id
    response = requests.get(url)

    dataset_id = ''
    if response.status_code == requests.codes.ok:
        response_json = json.loads(response.text)
        if response_json['response']['result']:
            dataset_id = response_json['response']['result'][0]["egaStableId"]
    else:
        print("Something went wrong: " + str(response.status_code))
        response.raise_for_status()

    return dataset_id


def get_duo_codes(egad_id):
    url = "https://ega-archive.org/catalog5/api/datasets/" + egad_id
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        data_use_conditions = json.loads(response.text)['dataUseConditions']
    else:
        print("Something went wrong: " + str(response.status_code))
        response.raise_for_status()

    duo_codes = []
    if data_use_conditions:
        for data_use_condition in data_use_conditions:
            duo_codes.append('DUO:' + data_use_condition['code'])

    return duo_codes


def get_ega_sample(egan_id):
    response = requests.get(EGA_SAMPLE_URL + egan_id)
    if response.status_code == requests.codes.ok:
        ega_sample = response.text
    else:
        print("Something went wrong: " + str(response.status_code))
        response.raise_for_status()

    return json.loads(ega_sample)


def get_biosample(accession):
    jwt = authenticate()
    bsd_url = BIOSAMPLES_URL + "/biosamples/samples/" + accession + '.json'
    header = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/hal+json",
        "Authorization": "Bearer " + jwt
    }

    response = requests.get(bsd_url, headers=header)
    if response.status_code == requests.codes.ok:
        sample = json.loads(response.text)
    else:
        print("Something went wrong: " + str(response.status_code))
        response.raise_for_status()

    return sample


def update_sample(sample):
    jwt = authenticate()
    bsd_url = BIOSAMPLES_URL + "/biosamples/samples/" + sample['accession']
    header = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/hal+json",
        "Authorization": "Bearer " + jwt
    }

    response = requests.put(bsd_url, data=json.dumps(sample), headers=header)
    if response.status_code == requests.codes.ok:
        sample = json.loads(response.text)
        print("Sample updated: " + sample["accession"])
    else:
        print("Something went wrong: " + str(response.status_code))
        response.raise_for_status()


def authenticate():
    r = requests.get(AAP_URL, auth=(AAP_USERNAME, AAP_PASSWORD))
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        raise r.raise_for_status()


if __name__ == "__main__":
    main()
