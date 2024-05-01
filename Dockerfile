# Use uma imagem base que inclua Python
FROM python:3.6

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=chatbot.settings

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências especificadas no requirements.txt
RUN pip install --upgrade pip &&
pip install --upgrade setuptools
pip install wheel
pip install --no-cache-dir -r requirements.txt

# Copie todos os arquivos do diretório atual para o diretório de trabalho dentro do contêiner
COPY . .

# Defina o comando que será executado quando o contêiner for iniciado
CMD ["python", "manage.py", "runserver", "34.72.228.16:5000"]
