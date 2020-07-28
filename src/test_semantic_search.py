from sentence_transformers import SentenceTransformer, util
from data.definition import RESULTS_MATCHED_SENTENCES


model_save_path = RESULTS_MATCHED_SENTENCES + "Bio_ClinicalBERT-2020-07-28_16-33-27"

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
    corpus = ['Normal cardiac contour.', 
        'Clear lung bilaterally.', 
        'No pleural effusion or pneumothorax.', 
        'Degenerative seen throughout cervical spine.', 
        'No acute cardiopulmonary abnormalities.']

    queries = ["Cervical Vertebrae degenerative"]

    find_most_similar_sentences(corpus, queries)