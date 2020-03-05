import json

import requests
from tqdm import tqdm

from config_params import BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN, HIPSCI_DATA_FILE_PATH
from curate_samples import SamplesCurator


def main():
    collect_and_save_hipsci_samples()
    add_ega_links_to_biosamples()


def collect_and_save_hipsci_samples():
    page = 1
    size = 20
    hipsci_crawler = HipsciCrawler(page, size)
    hipsci_crawler.collect_and_save_to_file(HIPSCI_DATA_FILE_PATH)


def add_ega_links_to_biosamples():
    samples_curator = SamplesCurator(BIOSAMPLES_URL, AAP_URL, AAP_USERNAME, AAP_PASSWORD, DOMAIN)
    with open(HIPSCI_DATA_FILE_PATH, 'r') as f:
        samples_map = json.load(f)

    jwt = samples_curator.authenticate()
    for accession, links in samples_map.items():
        curation = {"externalReferencesPost": []}
        ega_dataset_id_set = set()  # add only one time, though biosamples will remove duplicates
        for link in links:
            if not link["ega_accession"] in ega_dataset_id_set:
                ega_dataset_id_set.add(link["ega_accession"])
                curation["externalReferencesPost"].append({
                    "url": link["ega_url"]
                })
        samples_curator.curate_sample(accession, curation, jwt)

    print("Applied " + str(len(samples_map.items())) + " curations to biosamples")


class HipsciCrawler:
    hipsci_search_endpoint = "http://www.hipsci.org/lines/api/file/_search"

    def __init__(self, page, page_size):
        self.page = page
        self.page_size = page_size
        self.collected_records = 0
        self.samples_link_mapping = {}

    def collect_and_save_to_file(self, file_path):
        hipsci_page = self.get_hipsci_data(self.page, self.page_size)
        total_records = hipsci_page["hits"]["total"]
        print("Start crawling HipSci for " + str(total_records) + " records, page size = " + str(self.page_size))
        self.collected_records += self.process_page(hipsci_page["hits"]["hits"])
        progress_bar = tqdm(total=total_records)
        while self.page * self.page_size < total_records:
            self.page += 1
            hipsci_page = self.get_hipsci_data(self.page, self.page_size)
            self.collected_records += self.process_page(hipsci_page["hits"]["hits"])
            progress_bar.update(self.page_size)

        print("Crawled " + str(self.page) + " pages, collecting " + str(self.collected_records) + " records")
        self.save_to_file(file_path)

    def get_hipsci_data(self, page, size):
        hipsci_ega_query = {
            "query": {
                "match": {
                    "archive.name": "EGA"
                }
            },
            "from": (page - 1) * size,
            "size": size
        }
        response = requests.get(self.hipsci_search_endpoint, json=hipsci_ega_query)
        if response.status_code != requests.codes.ok:
            print(response.status_code + " : couldn't get HipSci records for, page: " + page + ", size" + size)

        return response.json()

    def process_page(self, records):
        for record in records:
            archive_record = {
                "ega_accession": record["_source"]["archive"]["accession"],
                "ega_accession_type": record["_source"]["archive"]["accessionType"],
                "ega_url": record["_source"]["archive"]["url"]
            }

            for sample in record["_source"]["samples"]:
                sample_accession = sample["bioSamplesAccession"]
                if sample_accession in self.samples_link_mapping:
                    self.samples_link_mapping[sample_accession].append(archive_record)
                else:
                    self.samples_link_mapping[sample_accession] = [archive_record]

        return len(records)

    def save_to_file(self, file_path):
        print("Got mappings for " + str(len(self.samples_link_mapping)) + " samples")
        with open(file_path, 'w') as output_file:
            json.dump(self.samples_link_mapping, output_file, indent=2)


if __name__ == "__main__":
    main()
