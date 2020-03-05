from decouple import config

BIOSAMPLES_URL = config("BIOSAMPLES_URL", default="http://wwwdev.ebi.ac.uk")
AAP_URL = config("AAP_URL", default="https://explore.api.aai.ebi.ac.uk/auth")
AAP_USERNAME = config("AAP_USERNAME")
AAP_PASSWORD = config("AAP_PASSWORD")
DOMAIN = config("DOMAIN", default="self.MyDomain")

DB_URL = config("DB_URL", default="localhost")
DB_USERNAME = config("DB_USERNAME")
DB_PASSWORD = config("DB_PASSWORD")

ACCESSION_FILE_PATH = config("ACCESSION_FILE_PATH", default="../resources/accession_list.txt")
HIPSCI_DATA_FILE_PATH = config("HIPSCI_DATA_FILE_PATH", default="../resources/hipsci_samples_ega_mapping.json")

print("Reading configurations....")
print("==============================================================")
print("BIOSAMPLES_URL = " + BIOSAMPLES_URL)
print("AAP_URL = " + AAP_URL)
print("AAP_USERNAME = " + AAP_USERNAME)
print("AAP_PASSWORD = " + "XXX")
print("DOMAIN = " + DOMAIN)
print("DB_URL = " + DB_URL)
print("DB_USERNAME = " + DB_USERNAME)
print("DB_PASSWORD = " + "XXX")
print("ACCESSION_FILE_PATH = " + ACCESSION_FILE_PATH)
print("HIPSCI_DATA_FILE_PATH = " + HIPSCI_DATA_FILE_PATH)
print("==============================================================")
