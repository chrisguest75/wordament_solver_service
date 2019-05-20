FROM python:3.7.2-stretch

RUN pip install pipenv

ARG USERID=1000
ARG GROUPID=1000
RUN addgroup --system --gid $GROUPID appuser
RUN adduser --system --uid $USERID --gid $GROUPID appuser


RUN mkdir -p /workbench/test_data

WORKDIR /workbench
COPY ./Pipfile /workbench/Pipfile
COPY ./Pipfile.lock /workbench/Pipfile.lock 

RUN pipenv install --deploy --system --dev

COPY ./main.py /workbench/main.py
COPY ./test_data/words_alpha.txt /workbench/test_data/words_alpha.txt

# set to no debugger.
ENV SERVER_URL="http://0.0.0.0:8000/api"
ENV DEBUGGER=False
ENV WAIT=False

USER appuser
EXPOSE 8080
CMD ["python3", "-u", "./main.py"]