from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
import spacy

app = Flask(__name__)

# Carregar o modelo de linguagem em português
nlp = spacy.load('pt_core_news_sm')

def calcular_resumo_tfidf(texto):
    # Remover quebras de linha e espaços extras
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # Dividir o texto em sentenças
    sentencas = re.split(r'(?<=[.!?]) +', texto)

    # Criar o vetor TF-IDF para as sentenças
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentencas)
    
    # Obter a soma dos pesos TF-IDF para cada sentença
    dense = tfidf_matrix.todense().A
    soma_tfidf = np.sum(dense, axis=1)

    # Criar um par de (índice da sentença, soma TF-IDF)
    sentencas_relevantes = sorted(enumerate(soma_tfidf), key=lambda x: x[1], reverse=True)

    # Extrair as 3 sentenças mais relevantes
    indices_relevantes = [idx for idx, _ in sentencas_relevantes[:3]]
    
    # Criar o resumo com as sentenças mais relevantes
    resumo = ' '.join(sentencas[i] for i in sorted(indices_relevantes))

    return resumo

def calcular_resumo_spacy(texto):
    # Usar spaCy para processar o texto
    doc = nlp(texto)
    
    # Extrair as sentenças
    sentencas = list(doc.sents)
    
    # Calcular a pontuação de cada sentença com base na contagem de palavras
    pontuacoes = [(sent, len(sent.text.split())) for sent in sentencas]

    # Obter as 3 sentenças mais longas
    sentencas_relevantes = sorted(pontuacoes, key=lambda x: x[1], reverse=True)[:3]
    
    # Criar o resumo
    resumo = ' '.join(str(sent[0]) for sent in sorted(sentencas_relevantes, key=lambda x: sentencas.index(x[0])))

    return resumo


@app.route('/', methods=['GET', 'POST'])
def home():
    resumo_tfidf = ""
    resumo_spacy = ""
    
    if request.method == 'POST':
        texto = request.form['texto']
        resumo_tfidf = calcular_resumo_tfidf(texto)  # Sumarização com TF-IDF
        resumo_spacy = calcular_resumo_spacy(texto)  # Sumarização com spaCy
    
    return render_template('index.html', resumo_tfidf=resumo_tfidf, resumo_spacy=resumo_spacy)

if __name__ == '__main__':
    app.run(debug=True)
