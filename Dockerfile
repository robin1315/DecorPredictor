FROM python:3.6.5-stretch
ADD . /code
WORKDIR /code
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade -r requirements.txt 

# CMD ["python", "train.py"]