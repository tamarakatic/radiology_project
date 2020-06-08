import os
import re
import nltk
import pandas as pd
from collections import defaultdict
from collections import Counter
from gensim.models import FastText
from typing import Dict


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
results = defaultdict(list)

def get_related_terms(word2vec, token, topn=5):
    similar_words = []
    if len(token.split('_')) > 1:
        token = ' '.join(token.split('_'))

    for word, _ in word2vec.wv.most_similar(token, topn=topn):
        if len(word.split('_')) > 1:
            word = ' '.join(word.split('_'))
        similar_words.append(word)

    return similar_words

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
                impression_finding_sentences = []
                num_bullets_per_file = 0
                num_covered_sentences = 0
                print(f"\n\nPURE MATCHING", file=fp)
                for i, line in enumerate(searchlines):

                    if "FINDINGS" in line:
                        if len(line.split('\t')) > 1:
                            findings = line.split('\t')[1].rstrip('\n')
                            findings_tokenizer = tokenizer.tokenize(findings)
                            findings_sentences = [sent.rstrip('.') for sent in findings_tokenizer if sent]
                            impression_finding_sentences = findings_sentences
                            
                    elif "IMPRESSION" in line:
                        if len(line.split('\t')) > 1:
                            impression = line.split('\t')[1].rstrip('\n')
                            impression_tokenizer = tokenizer.tokenize(impression)
                            impression_sentences = [sent.rstrip('.') for sent in impression_tokenizer if sent]
                            impression_finding_sentences += impression_sentences
                    
                    elif "Annotation:" in line:
                        # with open("results/all_sentences.txt", 'a+') as fw:
                        #     for sent in impression_finding_sentences:
                        #         if ', ' in sent:
                        #             sent = sent.replace(',','')
                        #         if 'XXXX' in sent:
                        #             sent = sent.replace('XXXX','')
                        #         if bool(re.search(r'\d', sent)) or not sent:
                        #             pass
                        #         else:
                        #             print(sent.lower() , file=fw)

                        results['filename'].append(filename)
                        results['num_sentences'].append(len(impression_finding_sentences))
                        num_bullets_per_file += len(searchlines[i+1:])
                        results['num_bullets'].append(num_bullets_per_file)
                        for nextLine in searchlines[i+1:]:
                            code = nextLine.split("/")
                            disease = code[0].rstrip('\n')
                            synonyms = disease.split(', ')
                        
                            if len(synonyms) > 1:
                                matching = [sent for dis in synonyms for sent in impression_finding_sentences if find_word(dis.lower(), sent.lower())]
                                if matching:
                                    matching = list(set(matching))
                            else:
                                matching = [sent for sent in impression_finding_sentences if find_word(disease.lower(), sent.lower())]

                            num_covered_sentences += len(matching)
                            
                            if len(matching) > 0:
                                print("{}: {}\n\t\t{}".format(nextLine.rstrip('\n'), len(matching), matching), file=fp)
                            else:
                                print("{}: {}".format(nextLine.rstrip('\n'), len(matching)), file=fp)
                        results['num_matching'].append(num_covered_sentences)
                    else:
                        pass
        df = pd.DataFrame(results)
        df.to_csv('updated_matching_results.csv', index=False)

if __name__ == '__main__':
    current_filepath = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.abspath(os.path.join(current_filepath, os.pardir))
    text_openi_files = os.path.join(root_path, "openI/text_openi_updated/") 

    find_annotations(text_openi_files)