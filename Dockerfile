# Use official Python image
FROM python:3.12-slim

WORKDIR /app

# Copy only what's needed
COPY requirements.txt .
COPY src/ src/
COPY README.md .

# Install dependencies (if any)
RUN pip install --no-cache-dir -r requirements.txt

# Set default command to run the text-based Snake
CMD ["python", "src/snake/text_snake.py"]