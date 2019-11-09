FROM python:3.8.0

RUN pip install pipenv

RUN mkdir /home/app
WORKDIR /home/app
COPY Pipfile* ./

RUN pipenv install --system --dev

COPY . .

ENTRYPOINT [ "python", "__main__.py"]