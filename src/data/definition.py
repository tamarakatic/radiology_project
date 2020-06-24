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

WEIGHTS_V1 = os.path.join(ROOT_PATH, 'data/external/weights/sample_weights_v1.txt')
WEIGHTS_V2 = os.path.join(ROOT_PATH, 'data/external/weights/sample_weights_v2.txt')

BASELINE = os.path.join(ROOT_PATH, 'data/openITest_Train/test_baseline/')
HUMAN_LABELS = os.path.join(ROOT_PATH, 'data/openITest_Train/label_132_reports/')

TEST_V1 = os.path.join(ROOT_PATH, 'data/openITest_Train/test_v1/')
TEST_V2 = os.path.join(ROOT_PATH, 'data/openITest_Train/test_v2/')

TEST_V1_PATTERN_MATCHING = os.path.join(ROOT_PATH, 'data/openITest_Train/test_pattern_matching_v1/')
TEST_V2_PATTERN_MATCHING = os.path.join(ROOT_PATH, 'data/openITest_Train/test_pattern_matching_v2/')

FASTTEXT_V1 = os.path.join(ROOT_PATH, 'data/openITest_Train/test_fastText_v1/')
FASTTEXT_V2 = os.path.join(ROOT_PATH, 'data/openITest_Train/test_fastText_v2/')

FASTTEXT_V1_PATTERN_MATCHING = os.path.join(ROOT_PATH, 'data/openITest_Train/test_fastText_matching_v1/')
FASTTEXT_V2_PATTERN_MATCHING = os.path.join(ROOT_PATH, 'data/openITest_Train/test_fastText_matching_v2/')

RESULTS = os.path.join(ROOT_PATH, 'results/')
TEST = os.path.join(ROOT_PATH, 'data/openITest_Train/test/')
TRAIN = os.path.join(ROOT_PATH, 'data/openITest_Train/train/')