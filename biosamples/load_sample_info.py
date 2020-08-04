import requests
import pandas as pd

from config_params import BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN

ACCESSION_FILE_PATH = "../resources/hpscreg_domain_mismatch_non_WTSI.csv"
OUTPUT_FILE_PATH = "../hpscreg_domain_mismatch_non_WTSI_domains.csv"


def main():
    print("Start executing script")
    sample_curator = SamplesLoader(BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN)
    sample_curator.load_samples_from_file(ACCESSION_FILE_PATH, OUTPUT_FILE_PATH)


class SamplesLoader:

    def __init__(self, biosamples_url, aap_url, username, password, domain):
        self.biosamples_url = biosamples_url
        self.aap_url = aap_url
        self.username = username
        self.password = password
        self.domain = domain

    def load_samples_from_file(self, accession_file_path, output_file_path):
        sample_list = []
        domain_set = set()
        accession_list = self.get_accessions(accession_file_path)
        for accession in accession_list:
            sample = self.load_sample(accession)
            domain_set.add(sample["domain"])
            sample_list.append(sample)

        pd_samples = pd.DataFrame(sample_list, columns=["accession", "domain", "update"])
        pd_samples.to_csv(output_file_path, index=False)
        print("Domains " + str(domain_set))
        print("Retrieved " + str(len(sample_list)) + " samples")

    def load_sample(self, accession):
        sample = {"accession" : accession}
        sample_url = self.biosamples_url + "/biosamples/samples/" + accession + "?curationdomain="
        response = requests.get(sample_url)
        if response.status_code == requests.codes.ok:
            sample["domain"] = response.json()["domain"]
            sample["update"] = response.json()["update"]
        else:
            print("Something went wrong with sample: " + accession)

        return sample

    def authenticate(self):
        r = requests.get(self.aap_url, auth=(self.username, self.password))
        if r.status_code == requests.codes.ok:
            return r.text
        else:
            raise r.raise_for_status()

    @staticmethod
    def get_accessions(accessions_file_path):
        print("Reading accessions from: " + accessions_file_path)
        pd_accessions = pd.read_csv(accessions_file_path, delimiter="; ", )
        return pd_accessions["ACCESSION"].tolist()


if __name__ == "__main__":
    main()
