import os
import re
import nltk
import pandas as pd
import operator
from collections import defaultdict
from collections import Counter
from typing import Dict

from data.rule_based_matching import not_annotate_sentence
from data.rule_based_matching import zero_annotation 
from data.rule_based_matching import check_synonyms
from data.rule_based_matching import is_in_synonyms

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# to find exact word without s or ing...
def find_word(search, text):
   result = re.findall('\\b'+search+'\\b', text, flags=re.IGNORECASE)
   if len(result)>0:
      return True
   else:
      return False


def write_matching_to_file(matching, nextLine, fp, code, impression_finding_sentences):
    if len(matching) == 1:
            print("{} {}".format(nextLine.rstrip('\n'), matching[0]), file=fp)
    elif len(matching) > 1:
        if code[1:]:    # if code has subheadings
            high_influence = defaultdict(int)
            for sub_key in matching:
                high_influence[sub_key] = 0
                for anot in code[1:]:
                    if is_in_synonyms(anot.lower()):
                        if check_synonyms(anot.lower(), impression_finding_sentences[sub_key].lower()):
                            high_influence[sub_key] += 1
                    else:
                        if find_word(anot.lower(), impression_finding_sentences[sub_key].lower()):
                            high_influence[sub_key] += 1

            max_impact_key = max(high_influence.items(), key=operator.itemgetter(1))[0]
            print("{} {}".format(nextLine.rstrip('\n'), max_impact_key), file=fp)        
        else:   # choose first key as there are no subheadings
            print("{} {}".format(nextLine.rstrip('\n'), matching[0]), file=fp)

    else:
        print("{} {}".format(nextLine.rstrip('\n'), 0), file=fp)


def find_annotations(openI_files):

    for filename in sorted(os.listdir(openI_files), key=lambda x: int(os.path.splitext(x)[0])): # sort files in folder
        with open(openI_files+filename, 'r+') as fp:
                searchlines = fp.readlines()
                impression_finding_sentences = {}
                annot_idx=0
           
                for idx, sent in enumerate(searchlines):
                        if "ANNOTATION WITH SENTENCE LABEL" in sent.rstrip('\n'):
                            annot_idx = idx
  
                for i, line in enumerate(searchlines):
                    if "SENTENCE LABEL" in line.rstrip('\n'):
                        for nextLine in searchlines[i+1:annot_idx-1]:
                                sentence = nextLine.rstrip('\n')
                                key = sentence.split('[label]:')[1]
                                value = sentence.split('[label]:')[0]
                                impression_finding_sentences[key] = value

                    if "ANNOTATION WITH SENTENCE LABEL" in line.rstrip('\n'):
                        print(f"\nANNOTATION WITH SENTENCE WITH LABELS", file=fp)
                        for key in list(impression_finding_sentences):
                            value = impression_finding_sentences[key]
                            if not_annotate_sentence(value):    # delete findings/impression sentences if they have some of those 'NOT_ANNOTATED' words
                                del impression_finding_sentences[key]

                        for nextLine in searchlines[i+1:]:
                            if nextLine.rstrip('\n'):
                                matching = []
                                code = nextLine.rstrip('\n').rstrip(":").split("/")
                                disease = code[0].rstrip('\n')
                                if zero_annotation(disease.lower()):
                                    print("{} {}".format(nextLine.rstrip('\n'), 0), file=fp)
                                    continue
                                elif is_in_synonyms(disease.lower()):
                                    matching = []
                                    for key, sent in impression_finding_sentences.items():
                                        if check_synonyms(disease.lower(), sent.lower()):
                                            matching.append(key)
                                    write_matching_to_file(matching, nextLine, fp, code, impression_finding_sentences)
                                elif ', ' in disease:  # if string has synonyms
                                    synonyms = disease.split(', ')
                                    matching = [key for dis in synonyms for key, sent in impression_finding_sentences.items() if find_word(dis.lower(), sent.lower())]
                                    if matching:
                                        matching = list(set(matching))
                                    write_matching_to_file(matching, nextLine, fp, code, impression_finding_sentences)
                                else:
                                    matching = [key for key, sent in impression_finding_sentences.items() if find_word(disease.lower(), sent.lower())]
                                    write_matching_to_file(matching, nextLine, fp, code, impression_finding_sentences)
if __name__ == '__main__':
    current_filepath = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.abspath(os.path.join(current_filepath, os.pardir))
    text_openi_files = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_pattern_matching_v1/") 

    find_annotations(text_openi_files)