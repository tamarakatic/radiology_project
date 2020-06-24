import os
import re
import operator
from collections import defaultdict
from collections import Counter
from gensim.models import FastText
from typing import Dict

from data.rule_based_matching import not_annotate_sentence
from data.rule_based_matching import zero_annotation 
from data.rule_based_matching import check_synonyms
from data.rule_based_matching import is_in_synonyms
from data.definition import FASTTEXT_RADIOLOGY


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

    fastText = FastText.load(FASTTEXT_RADIOLOGY)
    fastText.wv.init_sims()

    for filename in sorted(os.listdir(openI_files), key=lambda x: int(os.path.splitext(x)[0])): # sort files in folder
        with open(openI_files+filename, 'r+') as fp:
                searchlines = fp.readlines()
                sentences = {}
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
                                sentences[key] = value
                    
                    if "ANNOTATION WITH SENTENCE LABEL" in line.rstrip('\n'):
                        # print(f"\nANNOTATION WITH SENTENCE WITH LABELS", file=fp)
                        for key in list(sentences):
                            value = sentences[key]
                            if not_annotate_sentence(value):    # delete findings/impression sentences if they have some of those 'NOT_ANNOTATED' words
                                del sentences[key]

                        impression_finding_sentences = {}
                        for k, v in sentences.items():
                                if v not in impression_finding_sentences.values():  
                                        impression_finding_sentences[k] = v
                                        
                        for nextLine in searchlines[i+1:]:
                            if nextLine.rstrip('\n'):
                                similar_words = []
                                code = nextLine.rstrip('\n').rstrip(":").split("/")
                                disease = code[0].rstrip('\n')
                                matching = []
                                synonyms = None
                                if zero_annotation(disease.lower()):
                                    # print("{} {}".format(nextLine.rstrip('\n'), 0), file=fp)
                                    continue
                                    
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
                                            import pdb; pdb.set_trace()
                                        
                                    else:
                                        merge_lower_sent = '_'.join(disease.lower().split())
                                        similar_words = get_related_terms(fastText, merge_lower_sent)
                                        import pdb; pdb.set_trace()
                                        similar_words.append(disease.lower())

                                else:
                                    similar_words = get_related_terms(fastText, disease.lower())
                                    import pdb; pdb.set_trace()
                                    similar_words.append(disease.lower())

                                if similar_words: # if there are duplicates get unique fastText words
                                    similar_words = set(similar_words)           
                                
                                if similar_words: 
                                    for sim_word in similar_words:
                                        matching += [key for key, sent in impression_finding_sentences.items() if sim_word in sent.lower()]
                                    if is_in_synonyms(disease.lower()):
                                        for key, sent in impression_finding_sentences.items():
                                            if check_synonyms(disease.lower(), sent.lower()):
                                                matching.append(key)
                                    if matching:
                                        matching = list(set(matching))

                                else:
                                    if synonyms:
                                        matching += [key for dis in synonyms for key, sent in impression_finding_sentences.items() if dis.lower() in sent.lower()]
                                        if is_in_synonyms(disease.lower()):
                                            for key, sent in impression_finding_sentences.items():
                                                if check_synonyms(disease.lower(), sent.lower()):
                                                    matching.append(key)

                                        if matching:
                                            matching = list(set(matching))
                                    else:
                                        matching += [key for key, sent in impression_finding_sentences.items() if disease.lower() in sent.lower()]    
                                        if is_in_synonyms(disease.lower()):
                                            for key, sent in impression_finding_sentences.items():
                                                if check_synonyms(disease.lower(), sent.lower()):
                                                    matching.append(key)  
                                        if matching:
                                            matching = list(set(matching))                       
                            
                                try:
                                    if len(matching) == 1:
                                        # print("{} {}".format(nextLine.rstrip('\n'), matching[0]), file=fp)
                                        pass
                                    elif len(matching) > 1:
                                        if code[1:]:    # if code has subheadings
                                            high_influence = defaultdict(int)
                                            for sub_key in matching:
                                                high_influence[sub_key] = 0
                                                for anot in code[1:]:
                                                    similar_anot = []
                                                    anot = anot.lower()
                                                    if is_in_synonyms(anot.lower()):
                                                        if check_synonyms(anot.lower(), impression_finding_sentences[sub_key].lower()):
                                                            high_influence[sub_key] += 1
                                                    else:
                                                        similar_anot.append(anot)
                                                        if len(anot.split()) > 1:
                                                            anot = '_'.join(anot.split()) 
                                                        similar_anot += get_related_terms(fastText, anot)

                                                        for ft_anot in similar_anot: 
                                                            if find_word(ft_anot, impression_finding_sentences[sub_key].lower()):
                                                                high_influence[sub_key] += 1

                                            max_impact_key = max(high_influence.items(), key=operator.itemgetter(1))[0]
                                            # print("{} {}".format(nextLine.rstrip('\n'), max_impact_key), file=fp)
                                                        
                                        else:   # choose first key as there are no subheadings
                                            # print("{} {}".format(nextLine.rstrip('\n'), matching[0]), file=fp)
                                            pass
                                    else:
                                        # print("{} {}".format(nextLine.rstrip('\n'), 0), file=fp)
                                        pass
                                except IndexError:
                                    import pdb; pdb.set_trace()

if __name__ == '__main__':
    current_filepath = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.abspath(os.path.join(current_filepath, os.pardir))
    text_openi_files = os.path.join(root_path, "/home/tamara/Documents/research/radiology_project/radiology_project/data/test/") 

    find_annotations(text_openi_files)