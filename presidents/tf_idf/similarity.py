import string

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Tuple

pk = int



def stem_tokens(tokens):
    stemmer = nltk.stem.porter.PorterStemmer()
    return (stemmer.stem(item) for item in tokens)


def normalize(text: str):
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    yield from stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


VECTORIZER = TfidfVectorizer(min_df=1, stop_words='english', tokenizer=normalize)


def similarity_vectorizer(speech: str, corpus: List[Tuple[pk, str]], threshold=0.5, quick=False, quick_quantity=10) -> iter:
    """
    tfidf = vect.fit_transform(["I'd like an apple",
                                "An apple a day keeps the doctor away",
                                "Never compare an apple to an orange",
                                "I prefer scikit-learn to Orange"])

    (tfidf * tfidf.T).A

    array([[ 1.        ,  0.25082859,  0.39482963,  0.        ],
           [ 0.25082859,  1.        ,  0.22057609,  0.        ],
           [ 0.39482963,  0.22057609,  1.        ,  0.26264139],
           [ 0.        ,  0.        ,  0.26264139,  1.        ]])


    """

    for pk, other_speech in corpus:

        documents = [speech, other_speech]
        tfidf = VECTORIZER.fit_transform(documents)
        pairwise_similarity = (tfidf * tfidf.T).A[1, 0]

        if pairwise_similarity > threshold:
            yield pk, pairwise_similarity

            quick_quantity -= 1
            if quick and quick_quantity <= 0:
                break


