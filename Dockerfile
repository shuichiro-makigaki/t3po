FROM python:3

COPY *.py requirements.txt /t3po/
WORKDIR /t3po
RUN pip install -r requirements.txt
CMD ["python", "t3po.py"]

EXPOSE 5000
VOLUME ["/root/.ssh"]
