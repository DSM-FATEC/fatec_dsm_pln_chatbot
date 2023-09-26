FROM python:3.11

WORKDIR /app

COPY . . 

RUN pip install -r requirements.txt

RUN python -m spacy download pt_core_news_sm

RUN python -m nltk.downloader punkt

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

