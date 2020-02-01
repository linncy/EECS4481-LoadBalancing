FROM python:3.7-alpine
ADD . /flask_web
WORKDIR /flask_web
RUN pip3 install -r requirements.txt
CMD ["python3", "webapp.py"]