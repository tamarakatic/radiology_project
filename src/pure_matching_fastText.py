import os
import re
import operator
from collections import Counter
from collections import OrderedDict
from gensim.models import FastText
from typing import Dict
from nltk.stem import PorterStemmer 

from data.rule_based_matching import not_annotate_sentence
from data.rule_based_matching import check_splitted_annotation
from data.rule_based_matching import zero_annotation 
from data.rule_based_matching import check_synonyms
from data.rule_based_matching import is_in_synonyms
from data.definition import FASTTEXT_RADIOLOGY_UNIGAM
from data.definition import FASTTEXT_RADIOLOGY_BIGRAM
from data.definition import FASTTEXT_RADIOLOGY_TRIGRAM
from data.definition import TEST


def get_related_terms(word2vec, token, topn=5):
    similar_words = []
    if len(token.split('_')) > 1:
        token = ' '.join(token.split('_'))

    for word, _ in word2vec.wv.most_similar(token, topn=topn):
        if len(word.split('_')) > 1:
            word = ' '.join(word.split('_'))
        if len(word.split('/')) > 1:
           for subword in word.split('/'):
                if subword:
                    similar_words.append(subword) 
        similar_words.append(word)

    return similar_words

# remove duplicates from list but keep order
def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def find_annotations(openI_files):
    ps = PorterStemmer()
    fastText = FastText.load(FASTTEXT_RADIOLOGY_BIGRAM)
    fastText.wv.init_sims()

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
                            if not_annotate_sentence(value_annot):    # delete findings/impression sentences if they have some of those 'NOT_ANNOTATED' words
                                impression_finding_sentences.pop(key_annot)
                                       
                        for nextLine in searchlines[i+1:]:
                            if nextLine.rstrip('\n'):
                                similar_words = []
                                code = nextLine.rstrip('\n').rstrip(":").split("/")
                                disease = code[0].rstrip('\n')
                                matching = []
                                synonyms = None
                                if zero_annotation(disease.lower()):
                                    print("{} {}".format(nextLine.rstrip('\n'), 0), file=fp)
                                    continue
                                    
                                if ', ' in disease:  # if string has synonyms
                                    synonyms = disease.split(', ')

                                if len(disease.split()) > 1:   # disease has more than 1 word
                                        # merge with '_' words
                                    if synonyms: # there are more disease (synonyms)
                                        for dis in synonyms:
                                            similar_words.append(dis.lower())
                                            similar_words.append(ps.stem(dis.lower()))
                                            if len(dis.split()) > 1: # if disease before or after comma has more than 1 word
                                                dis = '_'.join(dis.lower().split())
                                            similar_words += get_related_terms(fastText, dis)
                                        
                                    else:
                                        similar_words.append(disease.lower())
                                        similar_words.append(ps.stem(disease.lower()))
                                        merge_lower_sent = '_'.join(disease.lower().split())
                                        similar_words += get_related_terms(fastText, merge_lower_sent)

                                else:
                                    similar_words.append(disease.lower())
                                    similar_words.append(ps.stem(disease.lower()))
                                    similar_words += get_related_terms(fastText, disease.lower())

                                if similar_words: # if there are duplicates get unique fastText words
                                    similar_words = remove_duplicates(similar_words)          
                                
                                if similar_words: 
                                    for sim_word in similar_words:
                                        matching += [key for key, sent in impression_finding_sentences.items() if sim_word in sent.lower()]
                                    
                                    if is_in_synonyms(disease.lower()):
                                        for key_syn, sent_syn in impression_finding_sentences.items():
                                            if check_synonyms(disease.lower(), sent_syn.lower()):
                                                matching.append(key_syn)
                                            else:
                                                if check_splitted_annotation(disease.lower(), sent_syn.lower()):
                                                    matching.append(key_syn)
                                                
                                    if matching:
                                        matching = remove_duplicates(matching)
                                else:
                                    if synonyms:
                                        matching += [key for dis in synonyms for key, sent in impression_finding_sentences.items() if dis.lower() in sent.lower()]
                                        if is_in_synonyms(disease.lower()):
                                            for key_syn, sent_syn in impression_finding_sentences.items():
                                                if check_synonyms(disease.lower(), sent_syn.lower()):
                                                    matching.append(key_syn)
                                                else:
                                                    if check_splitted_annotation(disease.lower(), sent_syn.lower()):
                                                        matching.append(key_syn)

                                        if matching:
                                            matching = remove_duplicates(matching)
                                    else:
                                        matching += [key for key, sent in impression_finding_sentences.items() if disease.lower() in sent.lower()]    
                                        if is_in_synonyms(disease.lower()):
                                            for key_syn, sent_syn in impression_finding_sentences.items():
                                                if check_synonyms(disease.lower(), sent_syn.lower()):
                                                    matching.append(key_syn)
                                                else:
                                                    if check_splitted_annotation(disease.lower(), sent_syn.lower()):
                                                        matching.append(key_syn)  
                                        if matching:
                                            matching = remove_duplicates(matching)
                            
                                try:
                                    if len(matching) == 1:
                                        print("{} {}".format(nextLine.rstrip('\n'), matching[0]), file=fp)
                                    elif len(matching) > 1:
                                        if code[1:]:    # if code has subheadings
                                            high_influence = OrderedDict()
                                            for sub_key in matching:
                                                high_influence[sub_key] = 0
                                                for anot in code[1:]:
                                                    similar_anot = []
                                                    anot = anot.lower()
                                                    if anot in impression_finding_sentences[sub_key].lower():
                                                        high_influence[sub_key] += 1
                                                    elif is_in_synonyms(anot.lower()):
                                                        if check_synonyms(anot.lower(), impression_finding_sentences[sub_key].lower()):
                                                            high_influence[sub_key] += 1
                                                        else:
                                                            if check_splitted_annotation(anot.lower(), impression_finding_sentences[sub_key].lower()):
                                                                high_influence[sub_key] += 1
                                                    else:
                                                        pass
                                                        # similar_anot.append(anot)
                                                        # if len(anot.split()) > 1:
                                                        #     anot = '_'.join(anot.split()) 
                                                        # similar_anot += get_related_terms(fastText, anot)

                                                        # for ft_anot in similar_anot:
                                                        #     import pdb; pdb.set_trace() 
                                                        #     if ft_anot in impression_finding_sentences[sub_key].lower():
                                                        #         high_influence[sub_key] += 1
                                            max_impact_key = max(high_influence.items(), key=operator.itemgetter(1))[0]
                                            print("{} {}".format(nextLine.rstrip('\n'), max_impact_key), file=fp)
                                        else:   # choose first key as there are no subheadings
                                            finding = [match for match in matching if "F-" in match]
                                            if not finding:
                                                finding = matching
                                            print("{} {}".format(nextLine.rstrip('\n'), finding[0]), file=fp)
                                    else:
                                        print("{} {}".format(nextLine.rstrip('\n'), 0), file=fp)
                                except IndexError:
                                    import pdb; pdb.set_trace()

if __name__ == '__main__':
    find_annotations(TEST)