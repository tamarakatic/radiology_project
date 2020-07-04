import os
import re
import pandas as pd
import operator
from collections import defaultdict
from collections import OrderedDict
from nltk.stem import PorterStemmer 
from collections import Counter
from typing import Dict

from data.rule_based_matching import not_annotate_sentence
from data.rule_based_matching import check_splitted_annotation
from data.rule_based_matching import zero_annotation 
from data.rule_based_matching import check_synonyms
from data.rule_based_matching import is_in_synonyms
from data.definition import TEST

sample_weights = []

# to find exact word without extension
def find_word(word, text):
   if re.search(r'\b' + word + r'\b', text):
       return True
   else:
      return False

# remove duplicates from list but keep order
def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def write_matching_to_file(matching, nextLine, fp, code, impression_finding_sentences):
    if len(matching) == 1:
        finding = [match for match in matching if "F-" in match]
        if not finding:
            finding = matching
        print("{} {}".format(nextLine.rstrip('\n'), finding[0]), file=fp)
            # sample_weights.append(2)
            # print("{} {}".format(nextLine.rstrip('\n'), matching[0]), file=fp)
    elif len(matching) > 1:
        # sample_weights.append(2.5)
        if code[1:]:    # if code has subheadings
            high_influence = defaultdict(int)
            for sub_key in matching:
                high_influence[sub_key] = 0
                for anot in code[1:]:
                    if find_word(anot.lower(), impression_finding_sentences[sub_key].lower()):
                            high_influence[sub_key] += 1
                    elif is_in_synonyms(anot.lower()):
                        if check_synonyms(anot.lower(), impression_finding_sentences[sub_key].lower()):
                            high_influence[sub_key] += 1
                    else:
                        if check_splitted_annotation(anot.lower(), impression_finding_sentences[sub_key].lower()):
                            high_influence[sub_key] += 1

            max_impact_key = max(high_influence.items(), key=operator.itemgetter(1))[0]
            # sample_weights.append(3)
            print("{} {}".format(nextLine.rstrip('\n'), max_impact_key), file=fp)        
        else:   # choose first key as there are no subheadings
            # sample_weights.append(2)
            finding = [match for match in matching if "F-" in match]
            if not finding:
                finding = matching
            print("{} {}".format(nextLine.rstrip('\n'), finding[0]), file=fp)

    else:
        # sample_weights.append(1)
        print("{} {}".format(nextLine.rstrip('\n'), 0), file=fp)


def find_annotations(openI_files):
    ps = PorterStemmer()

    for filename in sorted(os.listdir(openI_files), key=lambda x: int(os.path.splitext(x)[0])): # sort files in folder
        with open(openI_files+filename, 'r+') as fp:
            searchlines = fp.readlines()
            impression_finding = OrderedDict()
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
                        impression_finding[key] = value

                    impression_finding_sentences = OrderedDict()
                    for k, v in impression_finding.items():
                        if v not in impression_finding_sentences.values():  
                            impression_finding_sentences[k] = v

                if "ANNOTATION WITH SENTENCE LABEL" in line.rstrip('\n'):
                    print(f"\nANNOTATION WITH SENTENCE WITH LABELS", file=fp)
                    new_impression_finding_sentences = impression_finding_sentences.copy()
                    for key_annot, value_annot in new_impression_finding_sentences.items():
                        if not_annotate_sentence(value_annot):    # delete sentences with 'NOT_ANNOTATED' words
                            impression_finding_sentences.pop(key_annot)

                    for nextLine in searchlines[i+1:]:
                        if nextLine.rstrip('\n'):
                            matching = []
                            similar_words = []
                            code = nextLine.rstrip('\n').rstrip(":").split("/")
                            disease_synonym = None
                            disease = code[0].rstrip('\n')

                            if zero_annotation(disease.lower()):
                                # sample_weights.append(3)
                                print("{} {}".format(nextLine.rstrip('\n'), 0), file=fp)
                                continue
                            elif is_in_synonyms(disease.lower()):
                                for key, sent in impression_finding_sentences.items():
                                    if is_in_synonyms(disease.lower()):
                                        if check_synonyms(disease.lower(), sent.lower()):
                                            matching.append(key)
                                    if is_in_synonyms(ps.stem(disease.lower())):
                                        if check_synonyms(ps.stem(disease.lower()), sent.lower()):
                                            matching.append(key)
                                if matching:
                                    matching = remove_duplicates(matching)
                                write_matching_to_file(matching, nextLine, fp, code, impression_finding_sentences)
                            elif ', ' in disease:  # if string has synonyms
                                disease_synonym = disease.split(', ')
                                for dis_syn in disease_synonym:
                                    similar_words.append(dis_syn.lower())
                                    similar_words.append(ps.stem(dis_syn.lower()))
                                matching = [key for dis in similar_words for key, sent in impression_finding_sentences.items() if find_word(dis.lower(), sent.lower())]
                                if matching:
                                    matching = remove_duplicates(matching)
                                write_matching_to_file(matching, nextLine, fp, code, impression_finding_sentences)
                            else:
                                matching = [key for key, sent in impression_finding_sentences.items() if find_word(disease.lower(), sent.lower())]
                                matching += [key for key, sent in impression_finding_sentences.items() if find_word(ps.stem(disease.lower()), sent.lower())]
                                write_matching_to_file(matching, nextLine, fp, code, impression_finding_sentences)

if __name__ == '__main__':
    find_annotations(TEST)