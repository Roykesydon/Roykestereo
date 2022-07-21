FROM python:3.9.12

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80
EXPOSE 3000

CMD python app.py
# CMD waitress-serve --listen=*:5000 app:app