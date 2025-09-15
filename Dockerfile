FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY src/ src/
COPY README.md .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/snake/text_snake.py"]