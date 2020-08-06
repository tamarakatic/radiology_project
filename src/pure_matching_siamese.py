import os
import re
import operator
from collections import Counter
from collections import OrderedDict
from typing import Dict

from data.definition import SIAMESE_TRAIN
from data.rule_based_matching import zero_annotation

from sentence_transformers import SentenceTransformer, util
from data.definition import RESULTS_MATCHED_SENTENCES

model_save_path = RESULTS_MATCHED_SENTENCES + "Bio_ClinicalBERT-2020-07-28_20-03-24"

# remove duplicates from list but keep order
def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


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

                    # remove duplicates as there are sometimes in Findinggs and Impression duplicate sentences
                    impression_finding_sentences = OrderedDict()
                    for k, v in impression_finding.items():
                        if v not in impression_finding_sentences.values():  
                            impression_finding_sentences[k] = v

                if "ANNOTATION WITH SENTENCE LABEL" in line.rstrip('\n'):
                    print(f"\nANNOTATION WITH SENTENCE WITH LABELS", file=fp)
                                
                    for nextLine in searchlines[i+1:]:
                        if nextLine.rstrip('\n'):
                            similar_words = []
                            code = nextLine.rstrip('\n').rstrip(":").split("/")
                            disease = code[0].rstrip('\n')
                            matching = []
                            disease_synonym = None
                            try:
                                if zero_annotation(disease.lower()):
                                    print("{} {}".format(nextLine.rstrip('\n'), 0), file=fp)
                                    continue
                                else:
                                    annotation = " ".join(code)
                                    res_siamese = find_most_similar_sentences(impression_finding_sentences, annotation)
                                    print("{} {}".format(nextLine.rstrip('\n'), res_siamese), file=fp)    
                            except IndexError:
                                import pdb; pdb.set_trace()

if __name__ == '__main__':
    find_annotations(SIAMESE_TRAIN)