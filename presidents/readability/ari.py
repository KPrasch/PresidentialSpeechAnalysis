"""

Python module for scoring a body of text on the A.R.I. Scoring scale.

ARI Wiki: https://en.wikipedia.org/wiki/Automated_readability_index

"""


import re
import math
import nltk
from typing import Tuple, List

text = str


# def get_data(path: str) -> text:
#     """
#     Takes the symbol, path, or link to the file to a file
#     and returns it as unicode text contents.
#
#     """
#     with open(path, 'r') as f:
#         raw_text = f.read()
#         return raw_text


def character_count(text: str) -> int:
    stripped = re.sub(r'[^a-zA-Z0-9]', '', text)
    count = len(stripped)
    return count


def parse(text: str) -> Tuple[int, int, int]:
    """
    Takes raw text as input and returns a 
    tuple of sentence, word, and character count.
    
    """
    words = len(nltk.word_tokenize(text))
    sentences = len(nltk.sent_tokenize(text))

    characters = character_count(text)

    return characters, words, sentences


def calculate(characters: int, words: int, sentences: int) -> int:
    """
    Takes in ints to plug into the ARI formula.
    Returns the ARI score, rounded up to the ceiling.
    
    
    https://en.wikipedia.org/wiki/Automated_readability_index
    
    """
    try:
        step_one = 4.71 * (characters/words)
        step_two = 0.5 * (words/sentences)
    except ZeroDivisionError:
        result = 0     # TODO
    else:
        step_three = (step_one+step_two) - 21.43
        result = math.ceil(step_three)
    finally:
        return result


def ari_score(text):
    ari_scale = {
         1: {'ages':   '5-6', 'grade_level': 'Kindergarten'},
         2: {'ages':   '6-7', 'grade_level':    '1st Grade'},
         3: {'ages':   '7-8', 'grade_level':    '2nd Grade'},
         4: {'ages':   '8-9', 'grade_level':    '3rd Grade'},
         5: {'ages':  '9-10', 'grade_level':    '4th Grade'},
         6: {'ages': '10-11', 'grade_level':    '5th Grade'},
         7: {'ages': '11-12', 'grade_level':    '6th Grade'},
         8: {'ages': '12-13', 'grade_level':    '7th Grade'},
         9: {'ages': '13-14', 'grade_level':    '8th Grade'},
        10: {'ages': '14-15', 'grade_level':    '9th Grade'},
        11: {'ages': '15-16', 'grade_level':   '10th Grade'},
        12: {'ages': '16-17', 'grade_level':   '11th Grade'},
        13: {'ages': '17-18', 'grade_level':   '12th Grade'},
        14: {'ages': '18-22', 'grade_level':      'College'}
    }

    chars, words, sents = parse(text)
    score = calculate(chars, words, sents)

    try:
        scoredata = ari_scale[score]
    except KeyError:
        if score > 14 and score < 150:
            scoredata = ari_scale[14]
        elif score < 1 or score > 150:
            print('Calculation might be Wrong')
            score = 0
            scoredata = {'grade_level': 'Unknown'}

    return score, scoredata