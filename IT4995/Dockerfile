FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip uninstall django
RUN pip install -r requirements.txt
COPY . /app/

#RUN python manage.py collectstatic --noinput

CMD gunicorn IT4995.wsgi:application





