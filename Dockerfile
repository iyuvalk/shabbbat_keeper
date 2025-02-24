FROM python:3
LABEL authors="yuval"
EXPOSE 80/tcp

COPY src/requirements.txt /
COPY src/shabbat_keeper.py /
RUN /usr/local/bin/pip3 install -r /requirements.txt
ENTRYPOINT ["/shabbat_keeper.py"]