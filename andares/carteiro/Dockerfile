FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY carteiro.py /app/carteiro.py
USER 10000:10000
CMD ["python", "/app/carteiro.py", "loop"]
