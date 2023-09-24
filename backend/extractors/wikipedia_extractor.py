from goose3 import Goose


def extract_cats():
    goose = Goose()
    article = goose.extract('https://pt.wikipedia.org/wiki/Gato')

    return article.cleaned_text
