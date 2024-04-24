FROM python:3.11.2-slim-bullseye

RUN apt-get update \
	&& apt-get install -y --no-install-recommends --no-install-suggests \
	&& pip install --no-cache-dir --upgrade pip

WORKDIR /backEnd
COPY ./requirements.txt /backEnd
RUN pip install --no-cache-dir --requirement /backEnd/requirements.txt
COPY . /backEnd

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
