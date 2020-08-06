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
from data.definition import OPENI_AND_MIMIC_FASTTEXT_RADIOLOGY_UNIGRAM
from data.definition import FASTTEXT_RADIOLOGY_BIGRAM
from data.definition import FASTTEXT_RADIOLOGY_TRIGRAM
from data.definition import TEST

from sentence_transformers import SentenceTransformer, util
from data.definition import RESULTS_MATCHED_SENTENCES

# model_save_path = RESULTS_MATCHED_SENTENCES + "Bio_ClinicalBERT-2020-07-28_20-03-24"
model_save_path = RESULTS_MATCHED_SENTENCES + "Bio_ClinicalBERT-2020-07-29_20-32-07"

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

    
def find_synonyms(disease, impression_finding_sentences):
    synonyms_matching = []
    for key_syn, sent_syn in impression_finding_sentences.items():
        if is_in_synonyms(disease):
            if check_synonyms(disease, sent_syn.lower()):
                synonyms_matching.append(key_syn)
        else:
            if check_splitted_annotation(disease, sent_syn.lower()):
                synonyms_matching.append(key_syn)
    return synonyms_matching

def find_most_similar_sentences(sentence_key_pairs, query):
    corpus = list(sentence_key_pairs.values())
    embedder =  SentenceTransformer(model_save_path)
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

    similar_sentences = None
    key_result = "0"

    closest_n = 1
 
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]

    results = zip(range(len(scores)), scores)
    results = sorted(results, key=lambda x: x[1], reverse=True)

    for idx, score in results[0:closest_n]:
        similar_sentences = corpus[idx].strip()
    
    for k, v in sentence_key_pairs.items():
        if similar_sentences.rstrip() in v.rstrip():
            key_result = k
            break

    return key_result


def find_annotations(openI_files):
    ps = PorterStemmer()
    fastText = FastText.load(OPENI_AND_MIMIC_FASTTEXT_RADIOLOGY_UNIGRAM)
    fastText.wv.init_sims()
    siamese = 0

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
                            similar_words = []
                            code = nextLine.rstrip('\n').rstrip(":").split("/")
                            disease = code[0].rstrip('\n')
                            matching = []
                            disease_synonym = None
                            if zero_annotation(disease.lower()):
                                print("{} {}".format(nextLine.rstrip('\n'), 0), file=fp)
                                continue
                                
                            if ', ' in disease:  # if string has synonyms
                                disease_synonym = disease.split(', ')

                            if len(disease.split()) > 1:   # disease has more than 1 word
                                    # merge with '_' words
                                if disease_synonym: # there are more disease (disease_synonym)
                                    for dis in disease_synonym:
                                        similar_words.append(dis.lower()) # add subword of disease
                                        similar_words.append(ps.stem(dis.lower()))  # add stem of that disease
                                        if len(dis.split()) > 1: # if disease before or after comma has more than 1 word
                                            dis = '_'.join(dis.lower().split())
                                        similar_words += get_related_terms(fastText, dis)
                                    
                                else:
                                    similar_words.append(disease.lower())
                                    for dis in disease.lower().split():
                                        similar_words.append(dis)
                                        similar_words.append(ps.stem(dis.lower())) 
                                    similar_words.append(ps.stem(disease.lower()))
                                    merge_lower_sent = '_'.join(disease.lower().split())
                                    similar_words += get_related_terms(fastText, merge_lower_sent)
                            else:
                                similar_words.append(disease.lower())
                                similar_words.append(ps.stem(disease.lower()))
                                similar_words += get_related_terms(fastText, disease.lower())         
                            
                            if similar_words: # if there are duplicates get unique fastText words
                                similar_words = remove_duplicates(similar_words)      
                                matching += find_synonyms(disease.lower(), impression_finding_sentences)
                                for sim_word in similar_words:
                                    matching += [key for key, sent in impression_finding_sentences.items() 
                                                    if sim_word in sent.lower()]
                            else:
                                matching += [key for key, sent in impression_finding_sentences.items() 
                                                 if disease.lower() in sent.lower()]
                                matching += find_synonyms(disease.lower(), impression_finding_sentences)
                        
                            try:
                                if matching:
                                    matching = remove_duplicates(matching)
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
                                        max_impact_key = max(high_influence.items(), key=operator.itemgetter(1))[0]
                                        print("{} {}".format(nextLine.rstrip('\n'), max_impact_key), file=fp)
                                    else:   # choose first key as there are no subheadings
                                        finding = [match for match in matching if "F-" in match]
                                        if not finding:
                                            finding = matching
                                        print("{} {}".format(nextLine.rstrip('\n'), finding[0]), file=fp)
                                else:
                                    siamese += 1
                                    annotation = " ".join(code)
                                    res_siamese = find_most_similar_sentences(impression_finding_sentences, annotation)
                                    print("{} {}".format(nextLine.rstrip('\n'), res_siamese), file=fp)
                            except IndexError:
                                import pdb; pdb.set_trace()
    print(f"Number of siamese searching: {siamese}")

if __name__ == '__main__':
    find_annotations(TEST)