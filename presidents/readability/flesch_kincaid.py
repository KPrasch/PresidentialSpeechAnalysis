import nltk


D = nltk.corpus.cmudict.dict()


def word_syllabales(word):
    # n = [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]
    # syllables = 0
    # for data in D[word.lower()]:
    #     for y in data:
    #         if y[-1].isdigit():
    #             syllables += int(y[-1])

    return [len(list(y for y in x if y[-1].isdigit())) for x in D[word.lower()]][0]


def parse(text):
    words = nltk.word_tokenize(text)
    syllables = sum(word_syllabales(w) for w in words)
    sentences = nltk.sent_tokenize(text)

    return len(words), syllables, len(sentences)


def score(syllables, words, sentences):
    step_one = (words/sentences) * 1.015
    step_two = (syllables/words) * 84.6
    step_three = (step_one-step_two) - 206.835
    return step_three