import os

file_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(os.path.dirname(file_path))

RADIOLOGY_SENTENCES = os.path.join(ROOT_PATH, 'data/external/allreports.txt')
FASTTEXT_RADIOLOGY = os.path.join(ROOT_PATH, 'data/external/fastTextMimicCXR/fastTextRadiology.txt')

FASTTEXT_RADIOLOGY_UNIGAM = os.path.join(ROOT_PATH, 'data/external/fastTextMimicCXR/fastTextRadiologyUnigram.txt')
FASTTEXT_RADIOLOGY_BIGRAM = os.path.join(ROOT_PATH, 'data/external/fastTextMimicCXR/fastTextRadiologyBigram.txt')
FASTTEXT_RADIOLOGY_TRIGRAM = os.path.join(ROOT_PATH, 'data/external/fastTextMimicCXR/fastTextRadiologyTrigram.txt')

OPENI_AND_MIMIC_FASTTEXT_RADIOLOGY_UNIGRAM = os.path.join(ROOT_PATH, 'data/external/fastTextOpenI/openI_fastTextRadiologyUnigram.model')
OPENI_AND_MIMIC_FASTTEXT_RADIOLOGY_BIGRAM = os.path.join(ROOT_PATH, 'data/external/fastTextOpenI/openI_fastTextRadiologyBigram.model')
PREPROCESSED_OPENI_AND_MIMIC_FASTTEXT_RADIOLOGY_UNIGRAM = os.path.join(ROOT_PATH, 'data/external/fastTextOpenI/sg_preprocessed_openI_fastTextRadiologyUnigram.model')

MIMIC_CXR = os.path.join(ROOT_PATH, 'data/external/mimic-cxr-reports/')
PREPROCESSED_MIMIC_CXR = os.path.join(ROOT_PATH, 'data/external/preprocessed_mimic_cxr.txt')
PREPROCESSED_OPENI = os.path.join(ROOT_PATH, 'data/external/preprocessed_openI.txt')

WEIGHTS_V1 = os.path.join(ROOT_PATH, 'data/external/weights/sample_weights_v1.txt')
WEIGHTS_V2 = os.path.join(ROOT_PATH, 'data/external/weights/sample_weights_v2.txt')

BASELINE = os.path.join(ROOT_PATH, 'data/openITest_Train/test_baseline/')
HUMAN_LABELS = os.path.join(ROOT_PATH, 'data/label_132_reports/')

TEST_V1 = os.path.join(ROOT_PATH, 'data/openITest_Train/test_v1/')
TEST_V2 = os.path.join(ROOT_PATH, 'data/openITest_Train/test_v2/')

TEST_V1_PATTERN_MATCHING = os.path.join(ROOT_PATH, 'data/openITest_Train/test_pattern_matching_v1/')
TEST_V2_PATTERN_MATCHING = os.path.join(ROOT_PATH, 'data/openITest_Train/test_pattern_matching_v2/')

FASTTEXT_V1 = os.path.join(ROOT_PATH, 'data/openITest_Train/test_fastText_v1/')
FASTTEXT_V2 = os.path.join(ROOT_PATH, 'data/openITest_Train/test_fastText_v2/')

FASTTEXT_V1_PATTERN_MATCHING = os.path.join(ROOT_PATH, 'data/openITest_Train/test_fastText_matching_v1/')
FASTTEXT_V2_PATTERN_MATCHING = os.path.join(ROOT_PATH, 'data/openITest_Train/test_fastText_matching_v2/')

RESULTS = os.path.join(ROOT_PATH, 'results/')
TEST = os.path.join(ROOT_PATH, 'data/test_08_04_update/')
SIAMESE_TRAIN = os.path.join(ROOT_PATH, 'data/siamese_train/')
TRAIN = os.path.join(ROOT_PATH, 'data/openITest_Train/train/')
TRAIN_07_29 = os.path.join(ROOT_PATH, 'data/openITest_Train/train_07_29/')
NEW_TRAIN = os.path.join(ROOT_PATH, 'data/train/')
COPY_FILES = os.path.join(ROOT_PATH, 'data/copy_files_test/')

TRAIN_NO_LABEL = os.path.join(ROOT_PATH, 'data/train_no_label/')
OPENI = os.path.join(ROOT_PATH, 'data/openI/')

ALL_LABELED_REPORTS = os.path.join(ROOT_PATH, 'data/openITest_Train/all_reports_labeled/')
NEW_UPDATED_LABELED_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/changed_new_updated_labeled_reports.jsonl')
NEW_UPDATED_NO_LABELED_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/changed_new_updated_NO_labeled_reports.jsonl')

SEQ_FILLTERED_LABELED_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/sequence_filltered_labeled_reports_07_29_v1.jsonl')
SEQ_FILLTERED_NO_LABELED_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/sequence_filltered_NO_labeled_reports_07_29_v1.jsonl')

NEW_SEQ_FILLTERED_LABELED_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/new_sequence_filltered_labeled_reports.jsonl')
NEW_SEQ_FILLTERED_NO_LABELED_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/new_sequence_filltered_NO_labeled_reports.jsonl')

REPETITION_SEQ_FILLTERED_LABELED_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/repetition_sequence_filltered_labeled_reports.jsonl')
REPETITION_SEQ_FILLTEREDD_NO_LABELED_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/repetition_sequence_filltered_NO_labeled_reports.jsonl')

PREPROCESSED_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/preprocessed_reports.jsonl')
PREPROCESSED_NO_LABEL_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/preprocessed_no_labeled_reports.jsonl')

NEW_PREPROCESSED_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/new_preprocessed_reports_08_03.jsonl')
NEW_PREPROCESSED_NO_LABEL_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/new_preprocessed_no_labeled_reports_08_03.jsonl')

FILLTERED_PREPROCESSED_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/filltered_preprocessed_reports.jsonl')
FILLTERED_PREPROCESSED_NO_LABEL_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/filltered_preprocessed_no_labeled_reports.jsonl')

UPDATED_ALL_LABELED_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/updated_all_reports_labeled.jsonl')
SEPARATE_ANNOT_SENT_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/separate_annot_sent.jsonl')
ANNOTATION_PAPER_REPRODUCATION = os.path.join(ROOT_PATH, 'data/openITest_Train/annotation_paper_reproduction.jsonl')

TEST_SUMMARIZATION = os.path.join(ROOT_PATH, 'data/summarization/test.jsonl')
TRAIN_SUMMARIZATION = os.path.join(ROOT_PATH, 'data/summarization/train.jsonl')
DEV_SUMMARIZATION = os.path.join(ROOT_PATH, 'data/summarization/dev.jsonl')

TEST_SEP_ANNOT_SENT_SUMMAR = os.path.join(ROOT_PATH, 'data/sep_annot_sent_summar/test.jsonl')
TRAIN_SEP_ANNOT_SENT_SUMMAR = os.path.join(ROOT_PATH, 'data/sep_annot_sent_summar/train.jsonl')
DEV_SEP_ANNOT_SENT_SUMMAR = os.path.join(ROOT_PATH, 'data/sep_annot_sent_summar/dev.jsonl')

TEST_REPRODUCTION_SUMMARI = os.path.join(ROOT_PATH, 'data/reproduction/test.jsonl')
TRAIN_REPRODUCTION_SUMMARI = os.path.join(ROOT_PATH, 'data/reproduction/train.jsonl')
DEV_REPRODUCTION_SUMMARI = os.path.join(ROOT_PATH, 'data/reproduction/dev.jsonl')

TRAIN_UPDATED_SUMMARIZATION = os.path.join(ROOT_PATH, 'data/new_seq_filltered_reports_08_06/train.jsonl')
TEST_UPDATED_SUMMARIZATION = os.path.join(ROOT_PATH, 'data/new_seq_filltered_reports_08_06/test.jsonl')
DEV_UPDATED_SUMMARIZATION = os.path.join(ROOT_PATH, 'data/new_seq_filltered_reports_08_06/dev.jsonl')

SENTENCE_SIMILARITY = os.path.join(ROOT_PATH, 'data/similarity_sent_result/')
TRAIN_SENTENCE_SIMILARITY = os.path.join(ROOT_PATH, 'data/similarity_sent_result/train_07_29.csv')
DEV_SENTENCE_SIMILARITY = os.path.join(ROOT_PATH, 'data/similarity_sent_result/dev_07_29.csv')
TEST_SENTENCE_SIMILARITY = os.path.join(ROOT_PATH, 'data/similarity_sent_result/test_07_29.csv')
MATCHED_SENTENCES = os.path.join(ROOT_PATH, 'data/matched_sentences/')
MATCHED_SENTENCES_CHECKED = os.path.join(ROOT_PATH, 'data/matched_sentences_checked/')

RESULTS_MATCHED_SENTENCES = os.path.join(ROOT_PATH, 'results/similarity_output/')
ALL_REPORTS_LABELED = os.path.join(ROOT_PATH, 'data/all_reports_labeled/')
THOUSAND_REPORTS_LABELED = os.path.join(ROOT_PATH, 'data/1000_reports_labeled/')

SIAMESE_SEQ_FILLTERED_LABELED_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/siamese_sequence_filltered_labeled_reports_08_06.jsonl')
SIAMESE_FILLTERED_NO_LABELED_REPORTS_JSON = os.path.join(ROOT_PATH, 'data/openITest_Train/siamese_sequence_filltered_NO_labeled_reports_08_06.jsonl')