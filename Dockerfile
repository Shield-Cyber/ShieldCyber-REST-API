FROM python:3.11.2
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install "uvicorn[standard]"
CMD uvicorn rest:app --host 0.0.0.0