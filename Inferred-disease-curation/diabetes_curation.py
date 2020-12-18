import sys
import json
import re

"""
    With Json file from the query 'diabetes' in BSD, write the inferred disease with ontology.
"""

def main(JsonFile, AAP_USERNAME, AAP_PASSWORD):
    jf = open(JsonFile, 'r')
    data = json.load(jf)
    file1 = open('curation_diabetes.sh', 'w')
    file1.write('#!/bin/bash'+ '\n' + '\n')
    file1.write("curl -u " + AAP_USERNAME + ":" + AAP_PASSWORD + " https://api.aai.ebi.ac.uk/auth > aap.jwt" + '\n')
    file1.write('TOKEN=`cat aap.jwt`' + '\n' + '\n')
    file2 = open('Accession_curation_diabetes.txt', 'w')
    length = dict(data)
    j=0
    for i in range(0,len(length['_embedded']['samples'])):
        sample = dict(data['_embedded']['samples'][i])
        if  "diabetes type" not in sample["characteristics"]:
            accession = sample["accession"]
            diabetes = sample["characteristics"]["diabetes"]
            d = str(diabetes)
            if re.search("false", d) is not None or re.search("No", d) is not None or re.search("no", d) is not None:
                j+=1
                sample_curation = {
                                    "sample" : accession,
                                    "curation" : {
                                    "attributesPre" : [ ],
                                    "attributesPost" : [ {
                                                        "type" : "Biosamples inferred disease",
                                                        "value" : "Not diabetes"
                                                        } ]},
                                    "domain" : sample['domain'],
                                    "created" : sample['create']
                                    }
                file2.write(accession + '\n')
            elif re.search("Yes", d) is not None or re.search("yes", d) is not None:
                j+=1
                sample_curation = {
                                    "sample" : accession,
                                    "curation" : {
                                    "attributesPre" : [ ],
                                    "attributesPost" : [ {
                                                        "type" : "Biosamples inferred disease",
                                                        "value" : "Diabetes",
                                                        "iri" : [ "http://purl.obolibrary.org/obo/MONDO_0005015" ]
                                                        } ]},
                                    "domain" : sample['domain'],
                                    "created" : sample['create']
                                    }
                file2.write(accession + '\n')
            elif re.search("yes.type.I", d) is not None or re.search("d (IDDM)", d) is not None :
                j+=1
                sample_curation = {
                                    "sample" : accession,
                                    "curation" : {
                                    "attributesPre" : [ ],
                                    "attributesPost" : [ {
                                                    "type" : "Biosamples inferred disease",
                                                    "value" : "Type I diabetes",
                                                    "iri" : [ "http://www.ebi.ac.uk/efo/EFO_0001359" ]
                                                    } ]},
                                    "domain" : sample['domain'],
                                    "created" : sample['create']
                                    }
                file2.write(accession + '\n')
            elif re.search("T2D", d) is not None or re.search("type II diabetes mellitus", d) is not None or re.search("d (NIDDM)", d) is not None :
                j+=1
                sample_curation = {
                                    "sample" : accession,
                                    "curation" : {
                                    "attributesPre" : [ ],
                                    "attributesPost" : [ {
                                                    "type" : "Biosamples inferred disease",
                                                    "value" : "Type II diabetes mellitus",
                                                    "iri" : [ "http://www.ebi.ac.uk/efo/EFO_0001360" ]
                                                    } ]},
                                    "domain" : sample['domain'],
                                    "created" : sample['create']
                                    }
                file2.write(accession + '\n')
            elif re.search("nondiabetic", d) is not None :
                j+=1
                sample_curation = {
                                    "sample" : accession,
                                    "curation" : {
                                    "attributesPre" : [ ],
                                    "attributesPost" : [ {
                                                    "type" : "Biosamples inferred disease",
                                                    "value" : "non-diabetic",
                                                    "iri" : [ "http://www.ebi.ac.uk/efo/EFO_0001461" ]
                                                    } ]},
                                    "domain" : sample['domain'],
                                    "created" : sample['create']
                                    }
                file2.write(accession + '\n')
            else:
                sample_curation = {
                                    "sample" : accession,
                                    "curation" : {
                                    "attributesPre" : [ ],
                                    "attributesPost" : [ ]},
                                    "domain" : sample['domain'],
                                    "created" : sample['create']
                                    }
                file2.write(accession + '\n')
        else:
            accession = sample["accession"]
            diabetes = sample["characteristics"]["diabetes"]
            d = str(diabetes)
            type = sample["characteristics"]["diabetes type"]
            t = str(type)
            if re.search("Diagnosed by a medical professional", d) is not None:
                if re.search("Type I diabetes", t) is not None:
                    j+=1
                    sample_curation = {
                                    "sample" : accession,
                                    "curation" : {
                                        "attributesPre" : [ ],
                                        "attributesPost" : [ {
                                                    "type" : "Biosamples inferred disease",
                                                    "value" : "Type I diabetes",
                                                    "iri" : [ "http://www.ebi.ac.uk/efo/EFO_0001359" ]
                                                    } ]},
                                    "domain" : sample['domain'],
                                    "created" : sample['create']
                                    }
                    file2.write(accession + '\n')
                elif re.search("Type II diabetes", t) is not None:
                    j+=1
                    sample_curation = {
                                    "sample" : accession,
                                    "curation" : {
                                    "attributesPre" : [ ],
                                    "attributesPost" : [ {
                                                    "type" : "Biosamples inferred disease",
                                                    "value" : "Type II diabetes",
                                                    "iri" : [ "http://www.ebi.ac.uk/efo/EFO_0001360" ]
                                                    } ]},
                                    "domain" : sample['domain'],
                                    "created" : sample['create']
                                    }
                    file2.write(accession + '\n')
                elif re.search("Gestational diabetes", t) is not None:
                    j+=1
                    sample_curation = {
                                    "sample" : accession,
                                    "curation" : {
                                    "attributesPre" : [ ],
                                    "attributesPost" : [ {
                                                    "type" : "Biosamples inferred disease",
                                                    "value" : "Gestational diabetes",
                                                    "iri" : [ "http://www.ebi.ac.uk/efo/EFO_0004593" ]
                                                    } ]},
                                    "domain" : sample['domain'],
                                    "created" : sample['create']
                                    }
                    file2.write(accession + '\n')
            else:
                sample_curation = {
                                    "sample" : accession,
                                    "curation" : {
                                    "attributesPre" : [ ],
                                    "attributesPost" : [ ]},
                                    "domain" : sample['domain'],
                                    "created" : sample['create']
                                    }
        if j != 1000:
            file1.write("curl 'https://www.ebi.ac.uk/biosamples/samples/"+ accession + "/curationlinks'"+ " -i -X POST -H " + '"Content-Type: application/json;charset=UTF-8"'
                            + ' -H ' + '"Accept: application/hal+json"' +' -H '+ '"Authorization: Bearer $TOKEN"' + " -d " + "'"  + json.dumps(sample_curation) + "'" +'\n'+'\n'+'\n'+'\n')
        
        else:
            j = 0
            file1.write("curl -u" + AAP_USERNAME + ":" + AAP_PASSWORD + " https://api.aai.ebi.ac.uk/auth > aap.jwt" + '\n')
            file1.write('TOKEN=`cat aap.jwt`' + '\n' + '\n')
            file1.write("curl 'https://www.ebi.ac.uk/biosamples/samples/"+ accession + "/curationlinks'"+ " -i -X POST -H " + '"Content-Type: application/json;charset=UTF-8"' + ' -H ' + '"Accept: application/hal+json"' +' -H '+ '"Authorization: Bearer $TOKEN"' + " -d " + "'"  + json.dumps(sample_curation) + "'" +'\n'+'\n'+'\n'+'\n')


            
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
