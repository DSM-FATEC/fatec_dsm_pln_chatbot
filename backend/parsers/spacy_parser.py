import spacy


def token_is_valid(token):
    return not (
        token.is_stop
        or token.like_num
        or token.is_punct
        or token.is_space
        or len(token) == 1
    )


def clean_text(sentence):
    nlp = spacy.load('pt_core_news_sm')
    sentence_lower = sentence.lower()

    tokens = [token.text for token in nlp(sentence_lower) if token_is_valid(token)]

    return ' '.join(tokens)
