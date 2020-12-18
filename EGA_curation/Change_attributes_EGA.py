import sys
import json
import ast

"""
    With json files, change domain and organims for EGA samples.
    REMINDER: change '"templated" : true' to '"templated" : "true"' in json file.
"""

def main(JsonFile, AAP_USERNAME, AAP_PASSWORD):
    jf = open(JsonFile, 'r')
    file1 = open('BSD_API_for_EGA_samples.sh', 'w')
    file1.write('#!/bin/bash' + '\n' + '\n')
    file1.write("curl -u " + AAP_USERNAME + ":" + AAP_PASSWORD + " https://api.aai.ebi.ac.uk/auth > aap.jwt" + '\n')
    file1.write('TOKEN=`cat aap.jwt`' + '\n' + '\n')
    aux = jf.read().split('\n    }\n  }\n}\n\n')
    j =  0
    for i in range (len(aux)):
        j+=1
        if i != len(aux)-1:
            aux1 = aux[i] +'\n    }\n  }\n}'
        else:
            aux1 = aux[i]
        aux2 = json.dumps(aux1)
        aux3 = json.loads(aux2)
        sample = eval(aux3)
        sample['domain'] = 'self.EGA_BioSamples_Demo'
        sample['characteristics']['organism'] = [ {
                                                     "text" : "Homo sapiens",
                                                     "ontologyTerms" : [ "http://purl.obolibrary.org/obo/NCBITaxon_9606" ]
                                                    } ]
        if j != 999:
            file1.write("curl 'https://www.ebi.ac.uk/biosamples/samples/"+ sample['accession'] + "'"+ " -i -X PUT -H " + '"Content-Type: application/json;charset=UTF-8"'
                + ' -H ' + '"Accept: application/hal+json"' +' -H '+ '"Authorization: Bearer $TOKEN"' + " -d " + "'"  + json.dumps(sample) + "'" +'\n'+'\n''\n'+'\n')
        else:
            j = 0
            file1.write("curl -u " + AAP_USERNAME + ":" + AAP_PASSWORD + " https://api.aai.ebi.ac.uk/auth > aap.jwt" + '\n')
            file1.write('TOKEN=`cat aap.jwt`' + '\n' + '\n')
            file1.write("curl 'https://www.ebi.ac.uk/biosamples/samples/"+ sample['accession'] + "'"+ " -i -X PUT -H " + '"Content-Type: application/json;charset=UTF-8"'
                            + ' -H ' + '"Accept: application/hal+json"' +' -H '+ '"Authorization: Bearer $TOKEN"' + " -d " + "'"  + json.dumps(sample) + "'" +'\n'+'\n''\n'+'\n')


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
