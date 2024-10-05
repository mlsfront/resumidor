# Resumidor de Texto com TF-IDF e spaCy

Este projeto é um aplicativo web simples que resume textos utilizando duas abordagens diferentes: TF-IDF e spaCy. O aplicativo é construído com Flask e permite que o usuário insira um texto e obtenha resumos gerados com essas técnicas.

## Estrutura do Projeto

```
.
├── app.py
├── requirements.txt
└── templates
    └── index.html
```

### Arquivos

- **app.py**: O código principal do aplicativo Flask.
- **templates/index.html**: O template HTML que renderiza a interface do usuário.
- **requirements.txt**: As dependências necessárias para o projeto.

## Instalação

### Pré-requisitos

Antes de começar, você precisa ter o Python 3 e o pip instalados em seu sistema. Se você preferir usar o Anaconda, você pode instalar o ambiente a partir do Anaconda Navigator ou via linha de comando.

### Opção 1: Usando Anaconda

1. **Criar um ambiente virtual:**

   ```bash
   conda create --name resumidor python=3.8
   conda activate resumidor
   ```

2. **Instalar as dependências:**

   Execute o seguinte comando para instalar as dependências do projeto:

   ```bash
   conda install flask scikit-learn
   ```

3. **Instalar spaCy e o modelo de linguagem:**

   ```bash
   conda install -c conda-forge spacy
   python -m spacy download pt_core_news_sm
   ```

### Opção 2: Usando Python e pip

1. **Criar um ambiente virtual (opcional, mas recomendado):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use: venv\Scripts\activate
   ```

2. **Instalar as dependências:**

   Execute o seguinte comando para instalar as dependências do projeto:

   ```bash
   pip install -r requirements.txt
   ```

3. **Instalar spaCy e o modelo de linguagem:**

   ```bash
   pip install spacy
   python -m spacy download pt_core_news_sm
   ```

## Execução do Aplicativo

Depois de instalar as dependências, você pode iniciar o aplicativo com o seguinte comando:

```bash
python app.py
```

O aplicativo será executado em `http://127.0.0.1:5000/` por padrão.

## Uso

1. **Instalação das Dependências**:
   - Crie um ambiente virtual usando `Anaconda` ou `venv`.
   - Instale as dependências:
     ```bash
     pip install -r requirements.txt
     ```

2. **Rodar o Aplicativo**:
   ```bash
   python app.py
   ```
   O aplicativo estará disponível em `http://127.0.0.1:5000/`.

3. **Interface do Usuário**:
   - Insira o texto que deseja resumir no campo de texto.
   - Escolha entre "Resumir" ou "Resumir Avançado".
   - Os resumos aparecerão abaixo do campo de texto, formatados com quebras de linha.
   - Você pode copiar cada resumo usando o botão correspondente.

## Funcionalidade

- **Resumir com TF-IDF:** O aplicativo usa a técnica TF-IDF para identificar as sentenças mais relevantes do texto. Ele retorna as três sentenças com a maior soma dos valores TF-IDF.
  
- **Resumir com spaCy:** O aplicativo utiliza a biblioteca spaCy para processar o texto e retorna as três sentenças mais longas, considerando a contagem de palavras.

- **Resumo Avançado**: Uma opção de resumo que utiliza pré-processamento e remoção de stop words.

- **Interface Interativa**: O usuário pode inserir um texto, escolher um método de resumo e visualizar os resultados formatados.

## Alterações e Melhorias Implementadas

- **Remoção de Stop Words**: Agora, o aplicativo remove stop words para melhorar a qualidade dos resumos.
- **Formatação de Resumos**: Resumos agora são formatados para incluir quebras de linha e pontuação adequada.
- **Caractere Especial para Quebras de Linha**: Um caractere especial é utilizado para formatar as sentenças de maneira mais eficaz.
- **Preservação do Texto**: O texto inserido no `textarea` é mantido após a submissão do formulário.
- **Botões de Ação**: Incluídos botões para "Limpar" o texto, atualizar a página e copiar resumos específicos.

## Dependências

- Flask
- scikit-learn
- spaCy (instalar o modelo em português: `python -m spacy download pt_core_news_sm`)

## Contribuição

Sinta-se à vontade para contribuir com o projeto. Você pode abrir issues ou pull requests no repositório.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE). 

## Contato

Para dúvidas ou sugestões, entre em contato pelo e-mail [contato@mlsfront.com].

---

Aproveite o Resumidor de Texto!