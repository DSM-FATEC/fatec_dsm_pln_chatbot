from fastapi import FastAPI
from nltk import sent_tokenize, download

from extractors.wikipedia_extractor import extract_cats
from parsers.spacy_parser import clean_text
from models.message_model import MessageModel
from responders.chatbot import get_answer_index


# Baixando dependencias do NLTK
download('punkt')

# Instanciando o FastAPI
app = FastAPI()



@app.post('/msg')
def answer_msg(body: MessageModel):
    # Extraindo texto bruto da wikipedia
    cats_article = extract_cats()

    # Criando tokens NLTK do texto bruto
    cats_article_tokens = sent_tokenize(cats_article)

    # Preprocessando sentenças e limpando texto bruto
    preprocessed_sentences = [clean_text(token) for token in cats_article_tokens]
    preprocessed_message = clean_text(body.message)

    index = get_answer_index(preprocessed_sentences=preprocessed_sentences,
                             preprocessed_message=preprocessed_message)

    return cats_article_tokens[index]
