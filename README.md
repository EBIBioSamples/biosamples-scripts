# biosamples-scripts
Scripts for data manipulation in BioSamples

## Script Details
- `migrate_domain.py` - Change domain of a sample
- `curate_samples.py` - Add curation to a set of samples
- `hipsci_ega_link_import.py`- Import EGA links to BioSamples using HipSci data

## How to Run

### Configurations
Configuration is read from `.env` file in your project folder. You can copy this from BioSamples internal repository. It looks like something below.
```
BIOSAMPLES_URL=https:localhost:8081
AAP_URL=https://api.aai.ebi.ac.uk/auth
AAP_USERNAME=myUser
AAP_PASSWORD=myPassword
DOMAIN=self.myDomain

DB_URL=localhost
DB_USERNAME=dbUser
DB_PASSWORD=dbPass
```
