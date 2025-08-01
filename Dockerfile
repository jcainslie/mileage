FROM python:3.10-slim

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

RUN mkdir -p /app/instance
VOLUME ["/app/instance"]

EXPOSE 5000
CMD ["python", "app.py"]
