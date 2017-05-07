# -*- coding: UTF-8 -*-

from hazm import word_tokenize, POSTagger, Stemmer, Chunker, tree2brackets

POSTAGGER_MODEL = 'resources/postagger.model'

tagger = POSTagger(model=POSTAGGER_MODEL)
chunker = Chunker(model='resources/chunker.model')

BLACK_LIST = ['RT']


def is_word_ok(word):
    return len(word) >= 3 and word not in BLACK_LIST


def get_names(text):
    tagged_words = tagger.tag(word_tokenize(text))
    return list(filter(
        lambda word: is_word_ok(word),
        [tagged_word[0] for tagged_word in filter(lambda tagged_word: tagged_word[1] == 'N', tagged_words)]
    ))


if __name__ == '__main__':
    print(
        get_names(
           'حس می کنم'
        )
    )
