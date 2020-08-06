from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer,  SentencesDataset
from sentence_transformers import util
from sentence_transformers.readers import STSDataReader
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from data.definition import RESULTS_MATCHED_SENTENCES, SENTENCE_SIMILARITY


model_save_path = RESULTS_MATCHED_SENTENCES + "Bio_ClinicalBERT-2020-07-28_20-03-24"

def find_most_similar_sentences(corpus, queries):
    embedder =  SentenceTransformer(model_save_path)
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

    closest_n = 3
    for query in queries:
        query_embedding = embedder.encode(query, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]

        results = zip(range(len(scores)), scores)
        results = sorted(results, key=lambda x: x[1], reverse=True)

        print("\n\n======================\n\n")
        print("Query:", query)
        print("\nTop 3 most similar sentences in corpus:")

        for idx, score in results[0:closest_n]:
            print(corpus[idx].strip(), f"(Score: {score:.4f})")

if __name__ == '__main__':
    # Evaluate model
    model = SentenceTransformer(model_save_path)
    sts_reader = STSDataReader(SENTENCE_SIMILARITY, normalize_scores=False) 
    test_data = SentencesDataset(examples=sts_reader.get_examples("test.csv"), model=model)
    test_dataloader = DataLoader(test_data, shuffle=False, batch_size=32)
    evaluator = EmbeddingSimilarityEvaluator(test_dataloader)
    print(model.evaluate(evaluator))
    
    # Evaluate some test examples
    corpus = ['Normal cardiac contour.', 
        'Clear lung bilaterally.', 
        'No pleural effusion or pneumothorax.', 
        'Degenerative seen throughout cervical spine.', 
        'No acute cardiopulmonary abnormalities.']

    queries = ["Cervical Vertebrae degenerative"]

    find_most_similar_sentences(corpus, queries)