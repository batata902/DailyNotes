FROM python:3.12-slim

RUN useradd -m -s /bin/bash challenger


WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R challenger:challenger /app

USER challenger
EXPOSE 5000

CMD ["python3", "main.py"]
