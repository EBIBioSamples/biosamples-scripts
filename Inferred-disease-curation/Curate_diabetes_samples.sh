#!/bin/sh

#Ask for AAP account
read -p 'AAP Username: ' AAP_USERNAME
read -sp 'AAP Password: ' AAP_PASSWORD

## Ask for the json file extracted from Biosamples with the query 'diabetes'
read -p 'Enter the JSON file with all extracted samples: ' diabetes_samples

# Add the attribute 'Biosamples inferred disease' following the rules.
# Create a file with all accession ID for all curated samples and another file to curate the samples.
python diabetes_curation.py $diabetes_samples $AAP_USERNAME $AAP_PASSWORD

# Run through BioSamples API.
bash curation_diabetes.sh
