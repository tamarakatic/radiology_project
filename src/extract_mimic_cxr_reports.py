import os
from nltk.tokenize import sent_tokenize

from data.definition import MIMIC_CXR
from data.definition import PREPROCESSED_MIMIC_CXR


def preprocess_sent(report, findings=True):
    sentences = [sent.rstrip("\n") for sent in report if sent.strip() != '']
    sentences = [" ".join(sent.split()) for sent in sentences]

    if findings:
        sentences = [s for s in sentences if 'FINDINGS:' not in s]

    sentences = [s.lower().rstrip('.') for s in sentences if 'IMPRESSION:' not in s]
    sentences = [sent.replace('___', '') if '___' in sent else sent for sent in sentences]
    merge_sentences = ' '.join(sentences)
    return sent_tokenize(merge_sentences)


def extract_isentences(mimic_csr_folder):
    all_sentences = []
    for folder in sorted(os.listdir(mimic_csr_folder)):
        for subfolder in sorted(os.listdir(mimic_csr_folder+folder)):
            for filename in sorted(os.listdir(mimic_csr_folder+folder+"/"+subfolder)):
                with open(mimic_csr_folder+folder+"/"+subfolder+"/"+filename, 'r') as fp:
                    searchlines = fp.readlines()
                    startIndex = 0
                    endIndex = 0
                    
                    for i, line in enumerate(searchlines):
                        if "FINDINGS:" in line:
                            startIndex = i
                
                        if "IMPRESSION:" in line:
                            endIndex = i
                        
                    if startIndex != 0:
                        all_sentences += preprocess_sent(searchlines[startIndex:])
                        
                    elif endIndex != 0:
                        all_sentences += preprocess_sent(searchlines[endIndex:], False)
                    else:
                        pass
    
    return all_sentences


if __name__ == '__main__':
    preprocessed_sent = extract_isentences(MIMIC_CXR)

    with open(PREPROCESSED_MIMIC_CXR, 'a') as f:
        for sent in preprocessed_sent:
            print(sent.rstrip('.'), file=f)