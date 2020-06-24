import os

file_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(os.path.dirname(file_path))

RADIOLOGY_SENTENCES = os.path.join(ROOT_PATH, 'data/external/allreports.txt')
FASTTEXT_RADIOLOGY = os.path.join(ROOT_PATH, 'data/external/fastTextNew/fastTextRadiology.txt')

FASTTEXT_RADIOLOGY_UNIGAM = os.path.join(ROOT_PATH, 'data/external/fastTextNew/fastTextRadiologyUnigram.txt')
FASTTEXT_RADIOLOGY_BIGRAM = os.path.join(ROOT_PATH, 'data/external/fastTextNew/fastTextRadiologyBigram.txt')
FASTTEXT_RADIOLOGY_TRIGRAM = os.path.join(ROOT_PATH, 'data/external/fastTextNew/fastTextRadiologyTrigram.txt')

MIMIC_CXR = os.path.join(ROOT_PATH, 'data/external/mimic-cxr-reports/')
PREPROCESSED_MIMIC_CXR = os.path.join(ROOT_PATH, 'data/external/preprocessed_mimic_cxr.txt')