FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY coletor.py /app/coletor.py
# Mesmo usuario que os Hermes usam nas pastas de dados.
USER 10000:10000
CMD ["python", "/app/coletor.py", "loop"]
