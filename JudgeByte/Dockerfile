FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /judgebyte
WORKDIR /judgebyte
COPY requirements.txt /judgebyte
RUN pip install -r requirements.txt
COPY . /judgebyte
RUN mkdir /var/jail
RUN mkdir /var/jail/ubuntu
RUN mkdir /var/jail/ubuntu/judgedir
CMD ["python3","test2.py"]
#CMD /bin/bash
