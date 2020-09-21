import argparse
import sys

import requests

from config_params import BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN


def main(argv):
    # parser = argparse.ArgumentParser()
    # parser.add_argument("count", type=int, help="Number of samples to generate")
    # parser.add_argument("prefix", help="Prefix for sample names")
    # parser.add_argument("-i", "--start_index", type=int, help="Start index for sample names")
    # args = parser.parse_args()

    accessioner = Accessioner(BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN)
    accessions = accessioner.generate_accessions(1000, "ADOPT")
    # accessions = accessioner.generate_accessions(args.count, args.prefix)
    print(accessions)


class Accessioner:
    def __init__(self, biosamples_url, aap_url, username, password, domain):
        self.biosamples_url = biosamples_url
        self.aap_url = aap_url
        self.username = username
        self.password = password
        self.domain = domain

    def generate_accessions(self, no_of_accessions, name_prefix, start_index=1) -> list:
        accessions = []
        jwt = self.authenticate()
        for i in range(start_index, start_index + no_of_accessions):
            accession = self.pre_accession(name_prefix + "_" + str(i), jwt)
            if accession is not None:
                accessions.append(accession)

        return accessions

    def pre_accession(self, name, jwt) -> str:
        accession_endpoint = self.biosamples_url + "/biosamples/samples/accession"
        params = {"preAccessioning": "true"}
        sample = {"name": name, "domain": self.domain}
        header = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/hal+json",
            "Authorization": "Bearer " + jwt
        }

        accession = None
        response = requests.post(accession_endpoint, headers=header, json=sample, params=params)
        if response.status_code == requests.codes.ok:
            print("Sample created: " + response.text)
            accession = response.text
        else:
            print("Something went wrong: " + str(response.status_code))
            response.raise_for_status()

        return accession

    def authenticate(self):
        r = requests.get(self.aap_url, auth=(self.username, self.password))
        if r.status_code == requests.codes.ok:
            return r.text
        else:
            raise r.raise_for_status()


if __name__ == "__main__":
    main(sys.argv[1:])

