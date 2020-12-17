# EGA_domain script

Scripts for changing the domain  and add organism attribute for all EGA samples in Biosamples.

## Scripts details
• `Change_attributes_EGA.py`  Change the domain and add organism to the samples.

• `Change_EGA_domain.sh`  Create appropriate files and run all the scripts.

• `Import_BSD_API.py`  Write the curl command to extract json file from each sample. 

## How to run

• Create a file named BSD_ID_of_EGA_samples with all extracted Biosamples ID from ERAPRO, using this line: 

`SELECT BIOSAMPLE_ID FROM SAMPLE WHERE BIOSAMPLE_ID LIKE ‘SAME%’ AND EGA_ID IS NOT NULL AND FIRST_CREATED > ‘$DATE’`

`$DATE` corresponding in the date of the last use of EGA domain script.

Last curation : 20-NOV-20

### For example:
`SELECT BIOSAMPLE_ID FROM SAMPLE WHERE BIOSAMPLE_ID LIKE ‘SAME%’ AND EGA_ID IS NOT NULL AND FIRST_CREATED > ‘20-NOV-20’`


• Run  Change_EGA_domain.sh  

### For example:

`bash Change_EGA_domain.sh`

`AAP Username: biosample-usr`

`AAP Password: biosample-pwd`

`Enter the file with all Biosamples ID: BSD_ID_of_EGA_samples`
