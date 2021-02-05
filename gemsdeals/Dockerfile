FROM python:3.8.5
ENV PYTHONUNBUFFERED 1
COPY requirements.txt requirements.txt
RUN python - m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
ADD . /gemsdeals/
WORKDIR /gemsdeals