import nltk
import math
from typing import List


def get_vocab(text: str) -> List[tuple]:
    tokenized = nltk.Text(text)
    vocab = dict(tokenized.vocab())
    return vocab


def term_frequency(word: str, vocab: dict) -> int:
    try:
        frequency = vocab[word]
    except KeyError:
        raise Exception(f'{word} not in this document.')
    else:
        return frequency


def inverse_document_frequency(word: str, corpus: List[str]) -> int:
    inverse = sum(1 for speech in corpus if word in speech)
    return inverse


def score_word(word: str, speech: str, corpus: List[str], vocab: dict) -> float:
    tf = term_frequency(word, vocab)
    idf = 1 + inverse_document_frequency(word, corpus)
    product = tf * idf
    normalized = math.log(product)
    return normalized


def describe():
    pass


def score_corpus(speech: str, corpus: List[str]) -> List[tuple]:
    words = nltk.word_tokenize(speech)
    vocab = get_vocab(words)

    word_scores = list()
    for word in words:
        score = score_word(word, speech, corpus, vocab)
        word_scores.append((word, score))

    sorted_scores = sorted(word_scores, key=lambda t: t[1])
    return sorted_scores

