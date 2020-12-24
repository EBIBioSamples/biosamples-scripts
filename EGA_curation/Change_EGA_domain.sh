#!/bin/sh

#Ask for AAP account
read -p 'AAP Username: ' AAP_USERNAME
read -sp 'AAP Password: ' AAP_PASSWORD

#Ask for the text file with all Biosamples ID
read -p 'Enter the file with all Biosamples ID: ' BSD_ID_of_EGA_samples

#Remove EOF, to avoid extracting all BSD samples
perl -pi -e 'chomp if eof' $BSD_ID_of_EGA_samples

# Extract BSD ID of EGA samples from ERAPRO (BSD_ID_of_EGA_samples.txt)
# With BSD ID, write the curl command for BSD API to extract json file for each sample.
python Import_BSD_API.py $BSD_ID_of_EGA_samples $AAP_USERNAME $AAP_PASSWORD

# Extract json file for each EGA sample.
bash Import_json.sh

#Remove EOF
perl -pi -e 'chomp if eof' Json_EGA_samples.txt

#Change 'template:true'
sed 's/"templated" : true/"templated" : "true"/g' < Json_EGA_samples.txt > Json_EGA_samples_ready.txt

# Change the domain and add organism in the json file. Write the curl command to add changes in BSD API.
python Change_attributes_EGA.py Json_EGA_samples_ready.txt $AAP_USERNAME $AAP_PASSWORD

# Check if there are not apostrophe left alone, which can create a bug in the curl command.
sed "s/'[^h{ ]/'\\\\&'/g" BSD_API_for_EGA_samples.sh > BSD_API_for_EGA_samples_ready.sh

# Run through BioSamples API
bash BSD_API_for_EGA_samples_ready.sh
