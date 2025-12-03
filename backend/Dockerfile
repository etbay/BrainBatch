FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5173
CMD ["python", "scripts/bb_quart_main.py"]
