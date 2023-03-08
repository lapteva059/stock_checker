FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /stock_checker

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /stock_checker

EXPOSE 8000
CMD ["python", "main.py"]
