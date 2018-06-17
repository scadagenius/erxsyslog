FROM python:3.6

RUN pip3 install requests PyYAML

ADD erx_helper.py erx_syslog.py main_erx.py /

CMD ["python", "./main_erx.py"]
