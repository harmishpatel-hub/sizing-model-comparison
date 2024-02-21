# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11.7

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN git clone https://github.com/harmishpatel21/sizing-model-comparison.git . 
COPY . /app/
# Install pip requirements
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

EXPOSE 8501

# # Creates a non-root user with an explicit UID and adds permission to access the /app folder
# # For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT [ "streamlit" , "run", "app.py", "--server.port=8501", "--server.address=192.168.11.109"]

# # During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["python", "app.py"]
