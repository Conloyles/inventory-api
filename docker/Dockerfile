#Stage 1 - builder
FROM python:3.9-slim AS builder

WORKDIR /build

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --target=/install

#Stage 2 - Runtime
FROM python:3.9-slim AS runtime

#Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

#Copy only the installed packages from builder
COPY --from=builder /install /usr/local/lib/python3.9/site-packages/

#Copy application code
COPY app/ .

#Set ownership
RUN chown -R appuser:appuser /app

#Switch to non-root user
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["python", "main.py"]