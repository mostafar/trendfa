from hazm import word_tokenize, POSTagger, Stemmer

POSTAGGER_MODEL = 'resources/postagger.model'

tagger = POSTagger(model=POSTAGGER_MODEL)

BLACK_LIST = ['RT']


def get_names(text):
    tagged_words = tagger.tag(word_tokenize(text))
    return list(filter(
        lambda word: word not in BLACK_LIST,
        [tagged_word[0] for tagged_word in filter(lambda tagged_word: tagged_word[1] == 'N', tagged_words)]
    ))
