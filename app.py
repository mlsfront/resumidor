from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
import spacy

app = Flask(__name__)

# Carregar o modelo de linguagem em português
nlp = spacy.load('pt_core_news_sm')

def remover_stop_words(sentencas):
    # Usar spaCy para remover stop words de cada sentença
    sentencas_processadas = []
    for sentenca in sentencas:
        doc = nlp(sentenca)
        sentenca_processada = ' '.join([token.text for token in doc if not token.is_stop and not token.is_punct])
        sentencas_processadas.append(sentenca_processada)
    return sentencas_processadas

def formatar_resumo(resumo):
    # Substituir o caractere especial por ponto seguido de quebra de linha
    return resumo.replace('|', '.<br>')

def calcular_resumo_tfidf(texto):
    # Dividir o texto em sentenças
    sentencas = re.split(r'(?<=[.!?]) +', texto)

    # Remover stop words de cada sentença
    sentencas = remover_stop_words(sentencas)

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
    
    # Criar o resumo com as sentenças mais relevantes e adicionar caractere especial ao final de cada sentença
    resumo = '|'.join(sentencas[i] for i in sorted(indices_relevantes))
    return formatar_resumo(resumo)

def calcular_resumo_spacy(texto):
    # Dividir o texto em sentenças
    sentencas = re.split(r'(?<=[.!?]) +', texto)

    # Remover stop words de cada sentença
    sentencas = remover_stop_words(sentencas)

    # Usar spaCy para processar o texto
    doc = nlp(' '.join(sentencas))  # Juntar as sentenças processadas
    
    # Extrair as sentenças
    sentencas = list(doc.sents)
    
    # Calcular a pontuação de cada sentença com base na contagem de palavras
    pontuacoes = [(sent, len(sent.text.split())) for sent in sentencas]

    # Obter as 3 sentenças mais longas
    sentencas_relevantes = sorted(pontuacoes, key=lambda x: x[1], reverse=True)[:3]
    
    # Criar o resumo e adicionar caractere especial ao final de cada sentença
    resumo = '|'.join(str(sent[0]) for sent in sorted(sentencas_relevantes, key=lambda x: sentencas.index(x[0])))
    return formatar_resumo(resumo)

def calcular_resumo_avancado(texto):
    # Dividir o texto em sentenças
    sentencas = re.split(r'(?<=[.!?]) +', texto)

    # Remover stop words de cada sentença
    sentencas = remover_stop_words(sentencas)
    
    num_sentencas = max(1, min(5, len(sentencas) // 4))  # Ajuste baseado no tamanho do texto
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentencas)
    
    dense = tfidf_matrix.todense().A
    soma_tfidf = np.sum(dense, axis=1)
    
    sentencas_relevantes = sorted(enumerate(soma_tfidf), key=lambda x: x[1], reverse=True)
    
    indices_relevantes = [idx for idx, _ in sentencas_relevantes[:num_sentencas]]
    # Adicionar caractere especial ao final de cada sentença
    resumo = '|'.join(sentencas[i] for i in sorted(indices_relevantes))
    return formatar_resumo(resumo)

@app.route('/', methods=['GET', 'POST'])
def home():
    resumo_tfidf = ""
    resumo_spacy = ""
    resumo_avancado = ""
    texto = ""
    
    if request.method == 'POST':
        texto = request.form['texto']  # Armazena o texto do textarea
        if 'resumir' in request.form:
            resumo_tfidf = calcular_resumo_tfidf(texto)
            resumo_spacy = calcular_resumo_spacy(texto)
        elif 'resumir_avancado' in request.form:
            resumo_avancado = calcular_resumo_avancado(texto)
    
    return render_template('index.html', resumo_tfidf=resumo_tfidf, resumo_spacy=resumo_spacy, resumo_avancado=resumo_avancado, texto=texto)

if __name__ == '__main__':
    app.run(debug=True)
