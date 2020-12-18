# Curation Biosamples inferred disease script

Scripts for adding the attribute ‘Biosamples inferred disease’ following the [rules](https://docs.google.com/document/d/1o4WxjuHVsq1qa8obmnestl9_MIF-uzmyH2x16h5n-Zg/edit?usp=sharing).

## Scripts details

• `Curate_cancer_samples.sh`  Create appropriate files and run all the scripts for cancer curation.

• `cancer_curation.py`  Curate the samples with ‘Biosamples inferred disease : cancer’ and ontology.

• `Curate_diabetes_samples.sh` Create appropriate files and run all the scripts for diabetes curation.

• `diabetes_curation.py` Curate the samples with diabetes entries in ‘Biosamples inferred disease’ and ontology.

## How to run
• Copy relevant files into  PROJECT_HOME/resources directory

• Update in [Biosamples documentation](https://github.com/EBIBioSamples/biosamples-v4/blob/dev/webapps/core/src/main/asciidoc/guides_curation.adoc) the date of the curation.


### Cancer

• Create a Json file named `cancer_samples` with all extracted samples extracted with the query [`filter=attr%3Ais+tumor%3AYes&filter=attr%3Astudy+disease`](https://www.ebi.ac.uk/biosamples/samples.json?filter=attr%3Ais+tumor%3AYes&filter=attr%3Astudy+disease)

• Run  `bash Curate_cancer_samples.sh` Enter Biosamples AAP username and password. Enter the name of the created file, e.g cancer_samples. 



### Diabetes
• Create a Json file named `diabetes_samples` with all extracted samples extracted with the query [`filter=attr%3Adiabetes`](https://www.ebi.ac.uk/biosamples/samples.json?filter=attr%3Adiabetes)

• Run  `bash Curate_cancer_samples.sh` Enter Biosamples AAP username and password. Enter the name of the created file, e.g diabetes_samples. 
