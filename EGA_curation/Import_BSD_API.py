import sys


"""
    With file with samples accession BioSamples ID, get all json files.
    WARNING: remove EOF of AccessionFile
"""

def main(AccessionFile, AAP_USERNAME, AAP_PASSWORD):
    af = open(AccessionFile, 'r')
    file1 = open('Import_json.sh', 'w')
    file1.write('#!/bin/bash' + '\n' + '\n')
    BSD_ID = af.read().split('\n')
    j = 0
    file1.write("curl -u " + AAP_USERNAME + ":" + AAP_PASSWORD + " https://api.aai.ebi.ac.uk/auth > aap.jwt" + '\n')
    file1.write('TOKEN=`cat aap.jwt`' + '\n' + '\n')
    for i in range (0,len(BSD_ID)):
        j+=1
        if j != 999:
            accession = BSD_ID[i]
            accession = accession.replace('\r','')
            file1.write("curl 'https://www.ebi.ac.uk/biosamples/samples/"+ accession + "'"+ " -X GET -H " + '"Content-Type: application/json;charset=UTF-8"'
                    + ' -H ' + '"Accept: application/hal+json"' +' -H '+ '"Authorization: Bearer $TOKEN" ' + '>> Json_EGA_samples.txt' + '\n' + '\n' + 'echo -e ' +"'\n'"+ '>> Json_EGA_samples.txt' + '\n' + '\n')
        else:
            j = 0
            file1.write("curl -u " + AAP_USERNAME + ":" + AAP_PASSWORD + " https://api.aai.ebi.ac.uk/auth > aap.jwt" + '\n')
            file1.write('TOKEN=`cat aap.jwt`' + '\n' + '\n')
            accession = BSD_ID[i]
            accession = accession.replace('\r','')
            file1.write("curl 'https://www.ebi.ac.uk/biosamples/samples/"+ accession + "'"+ " -X GET -H " + '"Content-Type: application/json;charset=UTF-8"'
                + ' -H ' + '"Accept: application/hal+json"' +' -H '+ '"Authorization: Bearer $TOKEN" ' + '>> Json_EGA_samples.txt' + '\n' + '\n' + 'echo -e ' +"'\n'"+ '>> Json_EGA_samples.txt' + '\n' + '\n')
        


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])



