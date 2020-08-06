from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer,  SentencesDataset, LoggingHandler
from sentence_transformers import losses, models, util
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from sentence_transformers.readers import STSDataReader

from data.definition import SENTENCE_SIMILARITY, RESULTS_MATCHED_SENTENCES
from data.definition import TRAIN_SENTENCE_SIMILARITY, TEST_SENTENCE_SIMILARITY, DEV_SENTENCE_SIMILARITY

from scipy.spatial.distance import cdist
from datetime import datetime
import logging
import sys
import math

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])

train_batch_size = 32
num_epochs = 4

model_save_path = RESULTS_MATCHED_SENTENCES +"Bio_ClinicalBERT"+'-'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
sts_reader = STSDataReader(SENTENCE_SIMILARITY, normalize_scores=False)

word_embedding_model = models.Transformer("emilyalsentzer/Bio_ClinicalBERT")
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                               pooling_mode_mean_tokens=True,
                               pooling_mode_cls_token=False,
                               pooling_mode_max_tokens=False)
model = SentenceTransformer(modules=[word_embedding_model, pooling_model])

# Convert the dataset to a DataLoader ready for training
logging.info("Read OpenI train dataset")
train_dataset = SentencesDataset(sts_reader.get_examples('train_07_29.csv'), model)
train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=train_batch_size)
train_loss = losses.CosineSimilarityLoss(model=model)

logging.info("Read OpenI dev dataset")
dev_data = SentencesDataset(examples=sts_reader.get_examples('dev_07_29.csv'), model=model)
dev_dataloader = DataLoader(dev_data, shuffle=False, batch_size=train_batch_size)
evaluator = EmbeddingSimilarityEvaluator(dev_dataloader)


# Configure the training. We skip evaluation in this example
warmup_steps = math.ceil(len(train_dataset) * num_epochs / train_batch_size * 0.1) #10% of train data for warm-up
logging.info("Warmup-steps: {}".format(warmup_steps))

# Train the model
model.fit(train_objectives=[(train_dataloader, train_loss)],
          evaluator=evaluator,
          epochs=num_epochs,
          evaluation_steps=1000,
          warmup_steps=warmup_steps,
          output_path=model_save_path)

#####################################################
#
# Load the stored model and evaluate its performance
#
#####################################################

model = SentenceTransformer(model_save_path)
test_data = SentencesDataset(examples=sts_reader.get_examples("test_07_29.csv"), model=model)
test_dataloader = DataLoader(test_data, shuffle=False, batch_size=train_batch_size)
evaluator = EmbeddingSimilarityEvaluator(test_dataloader)
model.evaluate(evaluator)