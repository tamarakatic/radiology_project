from sentence_transformers import SentenceTransformer, util
from data.definition import RESULTS_MATCHED_SENTENCES


model_save_path = RESULTS_MATCHED_SENTENCES + "Bio_ClinicalBERT-2020-07-27_17-39-59"
embedder =  SentenceTransformer(model_save_path)

corpus = ['Heart size mediastinal contours are normal in appearance',
        'No focal airspace consolidation',
        'No pleural effusion or pneumothorax',
        'Mild degenerative changes of the thoracic spine',
        'No acute cardiopulmonary abnormalities.']

import pdb; pdb.set_trace()
corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

queries = ["Thoracic Vertebrae degenerative mild"]

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