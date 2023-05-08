FROM python:3.10.7


ENV PYTHONUNBUFFERED 1
# ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/backend

COPY requirements.txt /app/backend/

# RUN pip3 install -r requirements.txt
RUN pip install django django-cors-headers
RUN  pip install -r requirements.txt 

COPY . /api/backend/


CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]