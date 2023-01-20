FROM python:3.8-slim
# Python pa
WORKDIR /usr/local/bin

RUN apt-get update
RUN apt install xvfb -y
RUN apt -f install -y
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y

ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scripts/chromedriver chromedriver
RUN chmod +x chromedriver

COPY scripts/news_scrap_template.py news_scrap_template
RUN chmod +x news_scrap_template
ENV PATH="/usr/local/bin:${PATH}"