FROM jin09/app_engine

MAINTAINER Gautam Jain <gautam.jain9@yahoo.com>

RUN mkdir /home/src/

COPY / /home/src/

# RUN ls -la /home/src/*

# RUN rm -f /home/src/Dockerfile

RUN pip install -r /home/src/requirements.txt

EXPOSE 8080

CMD ["python", "/home/src/main.py"]
