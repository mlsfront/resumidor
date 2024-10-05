from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from sentence_transformers import SentenceTransformer, util
from nltk.tokenize import sent_tokenize
import torch

app = Flask(__name__)

# Carregar o modelo de embeddings
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Carregando o modelo
#model = SentenceTransformer('modelo-sentence-transformer')


def calcular_resumo_tfidf(texto):
    texto = re.sub(r'\s+', ' ', texto).strip()
    sentencas = re.split(r'(?<=[.!?]) +', texto)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentencas)
    dense = tfidf_matrix.todense().A
    soma_tfidf = np.sum(dense, axis=1)
    sentencas_relevantes = sorted(enumerate(soma_tfidf), key=lambda x: x[1], reverse=True)
    indices_relevantes = [idx for idx, _ in sentencas_relevantes[:3]]
    resumo = ' '.join(sentencas[i] for i in sorted(indices_relevantes))
    return resumo

# Função de sumarização
def calcular_resumo_embeddings(texto):
    sentencas = sent_tokenize(texto)
    embeddings = model.encode(sentencas)

    # Calcular similaridade
    similaridade = util.pytorch_cos_sim(embeddings, embeddings)

    # Debug prints
    print("Número de sentenças:", len(sentencas))
    print("Similaridade:", similaridade)
    print("Forma da similaridade:", similaridade.shape)

    num_sentencas = similaridade.shape[1]
    if num_sentencas < 3:
        print("Menos de 3 sentenças disponíveis.")
        return "O texto deve ter pelo menos 3 sentenças para ser resumido."

    indices_relevantes = similaridade.argsort()[0][-3:][::-1]

    # Retornar as sentenças relevantes
    resumo = [sentencas[i] for i in indices_relevantes]
    return " ".join(resumo)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        texto = request.form['texto']
        resumo_embeddings = calcular_resumo_embeddings(texto)  # Sumarização com embeddings
        return render_template('index.html', resumo=resumo_embeddings)
    return render_template('index.html', resumo='')

if __name__ == '__main__':
    app.run(debug=True)

