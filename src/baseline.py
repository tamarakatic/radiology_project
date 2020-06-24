import os
import re
import nltk
import pandas as pd
import operator
import random
from collections import defaultdict
from collections import Counter
from typing import Dict


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# to find exact word without s or ing...
def find_word(search, text):
   result = re.findall('\\b'+search+'\\b', text, flags=re.IGNORECASE)
   if len(result)>0:
      return True
   else:
      return False


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
                        for nextLine in searchlines[i+1:]:
                            if nextLine.rstrip('\n'):
                                random_sent = random.choice(list(impression_finding_sentences.keys()))
                                print("{} {}".format(nextLine.rstrip('\n'), random_sent), file=fp)

if __name__ == '__main__':
    current_filepath = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.abspath(os.path.join(current_filepath, os.pardir))
    text_openi_files = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_baseline/") 

    find_annotations(text_openi_files)