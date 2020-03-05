# biosamples-scripts
Scripts for data manipulation in BioSamples

## Script Details
- `migrate_domain.py` - Change domain of a sample
- `curate_samples.py` - Add curation to a set of samples
- `hipsci_ega_link_import.py`- Import EGA links to BioSamples using HipSci data

## How to Run
- Copy relevant files into  `PROJECT_HOME/resources` directory.
- Create `.env` file with configurations
- Install dependencies `pip install requirements.txt` (consider using virtualenv)
- Run desired script `python biosamples/migrate_domain.py`

### Configurations
Configuration is read from `.env` file in your project directory. You can copy this from BioSamples internal repository. It should look like below.
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
