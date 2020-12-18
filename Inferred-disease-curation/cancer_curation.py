import sys
import json
import re

"""
Curate sample with the attributes is_tumor == yes and the study disease corresponding to cancer research.
"""

def main(jsonFile, AAP_USERNAME, AAP_PASSWORD):
    jf = open(jsonFile, 'r')
    data = json.load(jf)
    file1 = open('curation_tumor.sh', 'w')
    file1.write('#!/bin/bash'+ '\n' + '\n')
    file1.write("curl -u " + AAP_USERNAME + ":" + AAP_PASSWORD + " https://api.aai.ebi.ac.uk/auth > aap.jwt" + '\n')
    file1.write('TOKEN=`cat aap.jwt`' + '\n' + '\n')
    file2 = open('Accession_curation_tumor.txt', 'w')
    length = dict(data)
    j = 0
    for i in range(0,len(length['_embedded']['samples'])):
        sample = dict(data['_embedded']['samples'][i])
        accession = sample['accession']
        tumor = sample['characteristics']['is tumor']
        study =  sample['characteristics']['study disease']
        t = str(tumor)
        if re.search("Yes", t) is not None:
            s = str(study)
            if  re.search("Acute Megakaryoblastic Leukemia", s) is not None or re.search("Acute Myeloid Leukemia", s) is not None or re.search("Adenocarcinoma", s) is not None or re.search("Adenocarcinoma Of Esophagus", s) is not None or re.search("Adenocarcinoma of lung", s) or re.search("Adrenocortical Carcinoma", s) is not None or re.search("Burkitt Lymphoma", s) is not None or re.search("Cancer, Colorectal", s) is not None or re.search("Carcinoma in Sit", s) is not None or re.search("Carcinoma, Ductal, Breast", s) is not None or re.search("Carcinoma, Hepatocellular", s) is not None or re.search("Carcinoma, Lobular", s) is not None or re.search("Carcinoma, Neuroendocrine", s) is not None or re.search("Carcinoma, Non-Small-Cell Lung", s) is not None or re.search("Carcinoma, Pancreatic Ductal", s) is not None or re.search("Carcinoma, Renal Cell", s) is not None or re.search("Carcinoma, Squamous Cell", s) or re.search("Carcinoma, Transitional Cell", s) is not None or re.search("Carcinoma, squamous cell of head and neck", s) is not None or re.search("Cholangiocarcinoma", s) is not None or re.search("Chronic Lymphocytic Leukemia", s) is not None or re.search("Cystadenocarcinoma", s) is not None or re.search("Cystadenocarcinoma, Serous", s) is not None or re.search("Endometrial Carcinomas", s) is not None or re.search("Esophageal Adenocarcinoma", s) is not None or re.search("Glioblastoma", s) is not None or re.search("Hepatoblastoma", s) is not None or re.search("Histiocytic Sarcoma", s) is not None or re.search("Leukemia, Hairy Cell", s) or re.search("Leukemia, Lymphocytic, Chronic, B-Cell", s) is not None or re.search("Leukemia, T-cell", s) is not None or re.search("Leukemia, Myeloid, Acute", s) is not None or re.search("Liposarcoma", s) is not None or re.search("Lymphoma, AIDS-Related", s) is not None or re.search("Lymphoma, Follicular", s) is not None or re.search("Lymphoma, Large B-Cell, Diffuse", s) is not None or re.search("Lymphoma, Non-Hodgkin", s) is not None or re.search("Lymphoma, T-Cell, Peripheral", s) is not None or re.search("Medulloblastoma", s) is not None or re.search("Melanoma", s) is not None or re.search("Melanoma,  Cutaneous Malignant", s) or re.search("Multiple Myeloma", s) is not None or re.search("Precursor B-Cell Lymphoblastic Leukemia-Lymphoma", s) is not None or re.search("Precursor Cell Lymphoblastic Leukemia-Lymphoma", s) is not None or re.search("Precursor T-Cell Lymphoblastic Leukemia-Lymphoma", s) is not None or re.search("Primary Myelofibrosis", s) is not None or re.search("Retinoblastoma", s) is not None or re.search("Rhabdomyosarcoma", s) is not None or re.search("Sarcoma", s) is not None or re.search("Sarcoma, Ewing", s) is not None or re.search("Sezary Syndrome", s) is not None or re.search("Small Cell Lung Carcinoma", s) is not None or re.search("Squamous Cell Carcinoma", s) or re.search("Thyroid cancer, Hurthle cell", s) is not None or re.search("Uveal melanoma", s) is not None or re.search("Wilms Tumor", s) is not None or re.search("Waldenstrom Macroglobulinemia", s) is not None or re.search("Leukemia, Lymphoid", s) is not None:
                j+=1
                sample_curation = {
                                    "sample" : accession,
                                    "curation" : {
                                    "attributesPre" : [ ],
                                    "attributesPost" : [ {
                                                        "type" : "Biosamples inferred disease",
                                                        "value" : "cancer",
                                                        "iri" : [ "http://www.ebi.ac.uk/efo/EFO_0000311" ]
                                                        } ]},
                                    "domain" : sample['domain'],
                                    "created" : sample['create']
                                    }
                
                
                if j != 1000:
                    file1.write("curl 'https://www.ebi.ac.uk/biosamples/samples/"+ accession + "/curationlinks'"+ " -i -X POST -H " + '"Content-Type: application/json;charset=UTF-8"'
                        + ' -H ' + '"Accept: application/hal+json"' +' -H '+ '"Authorization: Bearer $TOKEN"' + " -d " + "'"  + json.dumps(sample_curation) + "'" +'\n'+'\n'+'\n'+'\n')
                    file2.write(accession + '\n')
                else:
                    j = 0
                    file1.write("curl -u" + AAP_USERNAME + ":" + AAP_PASSWORD + " https://api.aai.ebi.ac.uk/auth > aap.jwt" + '\n')
                    file1.write('TOKEN=`cat aap.jwt`' + '\n' + '\n')
                    file1.write("curl 'https://www.ebi.ac.uk/biosamples/samples/"+ accession + "/curationlinks'"+ " -i -X POST -H " + '"Content-Type: application/json;charset=UTF-8"' + ' -H ' + '"Accept: application/hal+json"' +' -H '+ '"Authorization: Bearer $TOKEN"' + " -d " + "'"  + json.dumps(sample_curation) + "'" +'\n'+'\n'+'\n'+'\n')
                    file2.write(accession + '\n')

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])








