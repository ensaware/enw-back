FROM python:3.11-slim

ENV PYTHONUNBUFFERED True

RUN apt-get update && \
    apt-get install -y libgl1 libzbar-dev

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]