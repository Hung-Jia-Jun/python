FROM django
COPY pos-bot /django
WORKDIR /django
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 
#CMD python manage.py runserver 0.0.0.0:8000
EXPOSE 8000
