import scispacy
import spacy


def most_similar(word):
    by_similarity = sorted(word.vocab, key=lambda w: word.similarity(w), reverse=True)
    return [w.orth_ for w in by_similarity[:10]]


def most_similar_rare(word):
    queries = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
    by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
    return by_similarity[:10]


if __name__ == '__main__':
    nlp = spacy.load("en_core_sci_sm")

    print(most_similar(nlp.vocab[u'tumor']))
    print([w.lower_ for w in most_similar_rare(nlp.vocab[u'tumor'])])