import os
import nltk
import re
from collections import defaultdict
from collections import Counter
from typing import Dict

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def find_annotations(openI_files):
    for filename in sorted(os.listdir(openI_files), key=lambda x: int(os.path.splitext(x)[0])): # sort files in folder
        with open(openI_files+filename, 'r+') as fp:
                fp.seek(0)
                searchlines = fp.readlines()
                impression_sentences = []
                findings_sentences = []
                impression_finding_sentences = []
                print(f"\n\nSENTENCE LABEL", file=fp)
                for i, line in enumerate(searchlines):

                    if "FINDINGS" in line:
                        if len(line.split('\t')) > 1:
                            findings = line.split('\t')[1].rstrip('\n')
                            findings_sentences = tokenizer.tokenize(findings)
                            for idx, sent in enumerate(findings_sentences, start=1):
                                print(f"{sent} F-{idx}", file=fp)
                            findings_sentences = [sent.rstrip('.') for sent in findings_sentences if sent]
                            impression_finding_sentences = findings_sentences

                    if "IMPRESSION" in line:
                        if len(line.split('\t')) > 1:
                            impression = line.split('\t')[1].rstrip('\n')
                            impression_sentences = tokenizer.tokenize(impression)
                            try:
                                impression_sentences = [sent for sent in impression_sentences if not sent.replace('.', '').isdigit()]
                                p = re.compile("(\.){1}")
                                impression_sentences = [sent for sent in impression_sentences if p.sub("", sent)]
                            except IndexError:
                                import pdb; pdb.set_trace()
                            for idx, sent in enumerate(impression_sentences, start=1):
                                print(f"{sent} I-{idx}", file=fp)
                            impression_sentences = [sent.rstrip('.') for sent in impression_sentences if sent]
                            impression_finding_sentences += impression_sentences


                    impression_finding_sentences = impression_sentences + findings_sentences
                    if "Annotation:" in line:
                        print(f"\nANNOTATION WITH SENTENCE LABEL", file=fp)
                        for nextLine in searchlines[i+1:]:
                            code = nextLine.split("/")
                            disease = code[0].rstrip('\n')
                            synonyms = disease.split(', ')
                            if impression_finding_sentences:
                                if len(synonyms) > 1:
                                    matching = [sent for dis in synonyms for sent in impression_finding_sentences if dis.lower() in sent.lower()]
                                    if matching:
                                        matching = list(set(matching))
                                else:
                                    matching = [sent for sent in impression_finding_sentences if disease.lower() in sent.lower()]
                            
                                if len(matching) > 0:
                                    print("{}".format(nextLine.rstrip('\n')), file=fp)
                                else:
                                    print("{}".format(nextLine.rstrip('\n')), file=fp)

if __name__ == '__main__':
    current_filepath = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.abspath(os.path.join(current_filepath, os.pardir))
    text_openi_files = os.path.join(root_path, "/Users/tamarakatic/Desktop/radiology/openI_data/openITest_Train/train/") 

    find_annotations(text_openi_files)