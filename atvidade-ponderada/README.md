# Sistema de Auxílio à Tomada de Decisões para Investimento em Cripto Ativos

Este projeto é uma implementação de um sistema de apoio à decisão para investidores de cripto ativos. O sistema analisa o histórico de preços da criptomoeda BTC-USD e faz previsões sobre os melhores momentos para compra e venda. A construção utiliza modelos de machine learning para análise preditiva, com o objetivo de maximizar o retorno dos investimentos.

## Tecnologias Utilizadas

- **Python 3.10**: Linguagem de programação para implementar o sistema.
- **Flask**: Framework web utilizado para expor a API de previsões.
- **Machine Learning (LSTM)**: Modelo escolhido para previsão de séries temporais (preços de cripto).
- **Docker**: Para containerização e facilitar o deploy do sistema.
- **Docker Compose**: Para orquestrar o ambiente do sistema.

## Estrutura do Projeto
```bash
/app
  ├── app.py            # Arquivo principal que define a aplicação Flask.
  ├── pipeline.py       # Lógica para o treinamento e retreinamento do modelo LSTM.
  ├── templates/        # Arquivos HTML para renderização da interface web.
  └── requirements.txt  # Lista de dependências do projeto.
Dockerfile               # Arquivo para construção da imagem Docker.
docker-compose.yml       # Arquivo Docker Compose para orquestração de containers.
README.md                # Documento com instruções e informações sobre o projeto.

```


## Como Executar o Projeto

### Pré-requisitos

- Docker e Docker Compose instalados em sua máquina.

### Passos para Execução

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/ifferreira/m07/
    cd m07/atividade-ponderada/src
    ```

2. **Construir e iniciar os containers:**
    ```bash
    docker-compose up --build
    ```

3. **Acessar a aplicação:**
    A aplicação estará disponível em http://localhost:5000. Nela, você poderá fazer previsões com base em dados históricos e retreinar o modelo.

4. **Retreinamento do modelo:** Para retreinar o modelo com novos dados, insira o intervalo de datas desejado e clique em "Retreinar Modelo". O sistema atualizará o modelo com base nos dados históricos disponíveis para o período.

## Documentação dos Arquivos de Deployment

- **Dockerfile:** Este arquivo define a imagem base Python 3.10-slim, configura o ambiente de trabalho e instala as dependências. Ele também expõe a porta 5000, onde o Flask executa a aplicação. A escolha do python:3.10-slim foi feita para garantir um container leve e rápido, focando em simplicidade e eficiência.

- **docker-compose.yml:** Este arquivo orquestra a execução do container Flask, mapeando a porta 5000 do host para o container e permitindo o desenvolvimento contínuo com volumes sincronizados.

