FROM python:3.9

WORKDIR /app

COPY . .

WORKDIR /app/examples/recommender

RUN apt-get update && apt-get install -y cmake

RUN pip install --upgrade pip
RUN pip install cmake

RUN pip install pipenv

RUN pipenv lock

RUN pipenv install --system --deploy

ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

CMD ["bash", "init.sh"]