# Use uma imagem base do Python
FROM python:3.9

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos necessários para o contêiner
COPY requirements.txt /app
COPY app.py /app

# Instale as dependências da aplicação
RUN pip install --upgrade pip setuptools && \
    pip install wheel && \
    pip install --no-cache-dir -r requirements.txt

# Exponha a porta em que a aplicação Flask está sendo executada
EXPOSE 5000

# Comando para iniciar a aplicação Flask
CMD ["python", "-m", "flask", "run", "--host=34.72.228.16"]
