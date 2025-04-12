# Use uma imagem base leve do Python
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo de dependências e instale-as
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copie o restante do código para o container
COPY . .

# Exponha a porta que o Flask usa (geralmente 5000)
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
