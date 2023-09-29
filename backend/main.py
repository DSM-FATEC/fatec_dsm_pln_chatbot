from pickle import dump, load
from os import getenv, path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from nltk import sent_tokenize, download

from extractors.wikipedia_extractor import extract_cats
from parsers.spacy_parser import clean_text
from models.message_model import MessageModel
from responders.chatbot import get_answer_index


SENTENCES_PICKLE = 'datasources/sentences.pickle'
TOKENS_PICKLE = 'datasources/tokens.pickle'

# Instanciando o FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_data_to_pickle() -> None:
    cats_article = extract_cats()

    # Criando tokens NLTK do texto bruto
    cats_article_tokens = sent_tokenize(cats_article)

    # Preprocessando sentenças e limpando texto bruto
    preprocessed_sentences = [clean_text(token) for token in cats_article_tokens]

    with open(SENTENCES_PICKLE, 'wb') as writer:
        dump(preprocessed_sentences, writer)

    with open(TOKENS_PICKLE, 'wb') as writer:
        dump(cats_article_tokens, writer)


def load_data_from_pickle():
    sentences = None
    tokens = None

    with open(SENTENCES_PICKLE, 'rb') as reader:
        sentences = load(reader)

    with open(TOKENS_PICKLE, 'rb') as reader:
        tokens = load(reader)

    return sentences, tokens


@app.post('/msg')
def answer_msg(body: MessageModel) -> str:
    # Preprocessando mensagem
    preprocessed_message = clean_text(body.message)

    sentences, tokens = load_data_from_pickle()

    index = get_answer_index(preprocessed_sentences=sentences,
                             preprocessed_message=preprocessed_message)
    if index is None:
        return "Desculpe, não consegui pensar em nenhuma resposta"

    try:
        return tokens[index]
    except:
        return "Desculpe, não consegui pensar em nenhuma resposta"


if __name__ == '__main__':
    # Instala dependências do NLTK
    download('punkt')

    if not path.isfile(SENTENCES_PICKLE) or not path.isfile(TOKENS_PICKLE):
        extract_data_to_pickle()

    port = int(getenv('PORT', 8000))

    run(app='main:app', host='0.0.0.0', port=port)
