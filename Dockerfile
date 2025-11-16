FROM python:3-alpine 

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY app.py /app/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["python", "/app/app.py", "--transport", "http", "--host", "0.0.0.0", "--port", "8080"]
