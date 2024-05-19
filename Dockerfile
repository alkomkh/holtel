FROM python:3.11
COPY . /app
WORKDIR /app
EXPOSE 80
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
