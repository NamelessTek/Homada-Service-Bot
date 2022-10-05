FROM python:3.10.7-buster
WORKDIR /homada_service_bot
COPY . .
RUN pip install --upgrade pip && pip3 install -r requirements.txt
CMD ["python3", "App/run.py"]
EXPOSE 5000