# Use uma imagem base do Python 10
FROM python:3.10-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo requirements.txt e instale as dependências
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copie o restante da aplicação
COPY app app

# Defina a variável de ambiente para que o Flask saiba onde encontrar a aplicação
ENV FLASK_APP=app/app.py

# Exponha a porta que o Flask usará
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["flask", "run", "--host=0.0.0.0"]
