# Use uma imagem base que inclua Python
FROM python:3.9

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=chatbot.settings

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências especificadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie todos os arquivos do diretório atual para o diretório de trabalho dentro do contêiner
COPY . .

# Defina o comando que será executado quando o contêiner for iniciado
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
