FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
# Pillow: converte os slides para JPEG e acerta a proporção que o Instagram aceita.
RUN pip install --no-cache-dir pillow
WORKDIR /app
COPY expedicao.py /app/expedicao.py
USER 10000:10000
CMD ["python", "/app/expedicao.py", "loop"]
