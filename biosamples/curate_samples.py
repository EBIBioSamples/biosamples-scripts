import requests

from config_params import BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN, ACCESSION_FILE_PATH


# applies a curation to biosamples record, curation should be in the form of
# {
#     "attributesPre": [],
#     "attributesPost": [],
#     "externalReferencesPre": [],
#     "externalReferencesPost": []
#  }
def main():
    curation = {
        "attributesPre": [],
        "attributesPost": [{
            "type": "Organism",
            "value": "Homo sapiens",
            "iri": ["http://purl.obolibrary.org/obo/NCBITaxon_9606"]
        }]
    }

    print("Start executing script")
    sample_curator = SamplesCurator(BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN)
    sample_curator.curate_samples_from_file(ACCESSION_FILE_PATH, curation)


class SamplesCurator:

    def __init__(self, biosamples_url, aap_url, username, password, domain):
        self.biosamples_url = biosamples_url
        self.aap_url = aap_url
        self.username = username
        self.password = password
        self.domain = domain

    def curate_samples_from_file(self, accession_file_path, curation):
        accession_list = self.get_accessions(accession_file_path)
        self.curate_samples(accession_list, curation)
        print("Curated " + str(len(accession_list)) + " samples")

    def curate_samples(self, accessions, curation):
        jwt = self.authenticate()
        for accession in accessions:
            self.curate_sample(accession, curation, jwt)

    def curate_sample(self, accession, curation, jwt):
        curation_endpoint = self.biosamples_url + "/biosamples/samples/" + accession + "/curationlinks"
        sample_curation = {
            "curation": curation,
            "sample": accession,
            "domain": self.domain
        }
        header = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/hal+json",
            "Authorization": "Bearer " + jwt
        }

        response = requests.post(curation_endpoint, headers=header, json=sample_curation)
        if response.status_code == requests.codes.created:
            print("Applied curation to sample: " + accession + ", curation: " + response.text)
        else:
            print("Something went wrong with sample: " + accession)

    def authenticate(self):
        r = requests.get(self.aap_url, auth=(self.username, self.password))
        if r.status_code == requests.codes.ok:
            return r.text
        else:
            raise r.raise_for_status()

    @staticmethod
    def get_accessions(accessions_file_path):
        print("Reading accessions from: " + accessions_file_path)
        with open(accessions_file_path) as f:
            accessions = f.read().splitlines()
        return accessions


if __name__ == "__main__":
    main()
