FROM python:3.7.3
WORKDIR /project
ADD . /project
RUN pip install -r requirements.txt
RUN python --version
CMD ["python","app.py"]