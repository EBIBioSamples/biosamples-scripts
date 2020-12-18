#!/bin/sh

#Ask for AAP account
read -p 'AAP Username: ' AAP_USERNAME
read -sp 'AAP Password: ' AAP_PASSWORD

## Ask for the json file extracted from Biosamples with the query 'is tumor:yes' + 'study disease'
read -p 'Enter the JSON file with all extracted samples:s ' cancer_samples

# Add the attribute 'disease:cancer' when you have 'is tumor:Yes' and the attribute 'study disease' corresponds to a cancer.
# Create a file with all accession ID for all curated samples and another file to curate the samples.
python cancer_curation.py $cancer_samples $AAP_USERNAME $AAP_PASSWORD

# Run through BSD API.
bash curation_tumor.sh
