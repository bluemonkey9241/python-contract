FROM python:3.6.5

WORKDIR /code

RUN pip install flask numpy scipy matplotlib==3.2.1 mpld3==0.5.5

CMD ["python", "app.py"]
