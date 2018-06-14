FROM python:3

COPY requirements.txt /t3po/
WORKDIR /t3po
RUN pip install -r requirements.txt
COPY *.py /t3po/
COPY entrypoint.sh /t3po/
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]

EXPOSE 5000
