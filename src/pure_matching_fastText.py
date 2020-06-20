import os
import re
import nltk
import operator
from collections import defaultdict
from collections import Counter
from gensim.models import FastText
from typing import Dict


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def get_related_terms(word2vec, token, topn=5):
    similar_words = []
    if len(token.split('_')) > 1:
        token = ' '.join(token.split('_'))

    for word, _ in word2vec.wv.most_similar(token, topn=topn):
        if len(word.split('_')) > 1:
            word = ' '.join(word.split('_'))
        similar_words.append(word)

    return similar_words

# to find exact word without s or ing...
def find_word(search, text):
   result = re.findall('\\b'+search+'\\b', text, flags=re.IGNORECASE)
   if len(result)>0:
      return True
   else:
      return False

def find_annotations(openI_files):

    fastText = FastText.load('models/radiology_mimic/trigram_fasstext/radiology_trigram_fasttext_3_20_100_model.txt')
    fastText.wv.init_sims()

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
                                similar_words = []
                                code = nextLine.rstrip('\n').rstrip(":").split("/")
                                disease = code[0].rstrip('\n')
                                matching = []
                                synonyms = None
                                if ', ' in disease:  # if string has synonyms
                                    synonyms = disease.split(', ')

                                if len(disease.split()) > 1:   # disease has more than 1 word
                                        # merge with '_' words
                                    if synonyms: # there are more disease (synonyms)
                                        for dis in synonyms:
                                            similar_words.append(dis.lower())
                                            if len(dis.split()) > 1: # if disease before or after comma has more than 1 word
                                                dis = '_'.join(dis.lower().split())
                                            similar_words += get_related_terms(fastText, dis)
                                        
                                    else:
                                        merge_lower_sent = '_'.join(disease.lower().split())
                                        similar_words = get_related_terms(fastText, merge_lower_sent)
                                        similar_words.append(disease.lower())

                                else:
                                    similar_words = get_related_terms(fastText, disease.lower())
                                    similar_words.append(disease.lower())

                                if similar_words: # if there are duplicates get unique fastText words
                                    similar_words = set(similar_words) 
                                
                                
                                if similar_words: 
                                    for sim_word in similar_words:
                                        matching += [key for key, sent in impression_finding_sentences.items() if sim_word in sent.lower()]
                                    if matching:
                                        matching = list(set(matching))

                                else:
                                    if synonyms:
                                        matching += [key for dis in synonyms for key, sent in impression_finding_sentences.items() if dis.lower() in sent.lower()]
                                        if matching:
                                            matching = list(set(matching))

                                    else:
                                        matching += [key for key, sent in impression_finding_sentences.items() if disease.lower() in sent.lower()]                             
                            
                                try:
                                    if len(matching) == 1:
                                        print("{} {}".format(nextLine.rstrip('\n'), matching[0]), file=fp)
                                    elif len(matching) > 1:
                                        if code[1:]:    # if code has subheadings
                                            high_influence = defaultdict(int)
                                            for sub_key in matching:
                                                high_influence[sub_key] = 0
                                                for anot in code[1:]:
                                                    similar_anot = []
                                                    anot = anot.lower()
                                                    similar_anot.append(anot)
                                                    if len(anot.split()) > 1:
                                                        anot = '_'.join(anot.split()) 
                                                    similar_anot += get_related_terms(fastText, anot)
                                                    for ft_anot in similar_anot: 
                                                        if find_word(ft_anot, impression_finding_sentences[sub_key].lower()):
                                                            high_influence[sub_key] += 1

                                            max_impact_key = max(high_influence.items(), key=operator.itemgetter(1))[0]
                                            print("{} {}".format(nextLine.rstrip('\n'), max_impact_key), file=fp)
                                                        
                                        else:   # choose first key as there are no subheadings
                                            print("{} {}".format(nextLine.rstrip('\n'), matching[0]), file=fp)

                                    else:
                                        print("{} {}".format(nextLine.rstrip('\n'), 0), file=fp)
                                except IndexError:
                                    import pdb; pdb.set_trace()

if __name__ == '__main__':
    current_filepath = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.abspath(os.path.join(current_filepath, os.pardir))
    text_openi_files = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_fastText_v2/") 

    find_annotations(text_openi_files)