from os import getenv

from fastapi import FastAPI
from uvicorn import run
from nltk import sent_tokenize, download

from extractors.wikipedia_extractor import extract_cats
from parsers.spacy_parser import clean_text
from models.message_model import MessageModel
from responders.chatbot import get_answer_index


# Instanciando o FastAPI
app = FastAPI()

# Instala dependências do NLTK
download('punkt')

# Extraindo texto bruto da wikipedia
cats_article = extract_cats()

# Criando tokens NLTK do texto bruto
cats_article_tokens = sent_tokenize(cats_article)

# Preprocessando sentenças e limpando texto bruto
preprocessed_sentences = [clean_text(token) for token in cats_article_tokens]


@app.post('/msg')
async def answer_msg(body: MessageModel) -> str:
    # Preprocessando mensagem
    preprocessed_message = clean_text(body.message)

    index = get_answer_index(preprocessed_sentences=preprocessed_sentences,
                             preprocessed_message=preprocessed_message)
    if index is None:
        return "Desculpe, não consegui pensar em nenhuma resposta"

    try:
        return cats_article_tokens[index]
    except:
        return "Desculpe, não consegui pensar em nenhuma resposta"


if __name__ == '__main__':
    port = int(getenv('PORT', 8000))

    run(app='main:app', host='0.0.0.0', port=port)
