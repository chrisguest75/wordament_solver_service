FROM python:3.7.2-stretch

RUN pip install pipenv

ARG USERID=1000
ARG GROUPID=1000
RUN addgroup --system --gid $GROUPID appuser
RUN adduser --system --uid $USERID --gid $GROUPID appuser


RUN mkdir -p /workbench/openapi

WORKDIR /workbench
COPY ./Pipfile /workbench/Pipfile
COPY ./Pipfile.lock /workbench/Pipfile.lock 

RUN pipenv install --deploy --system --dev

COPY ./service.py /workbench/service.py
COPY ./health.py /workbench/health.py
COPY ./puzzle.py /workbench/puzzle.py
COPY ./dictionary.py /workbench/dictionary.py
COPY ./state_manager.py /workbench/state_manager.py
COPY ./openapi/service_api.yaml /workbench/openapi/service_api.yaml
COPY ./logging_config.yaml /workbench/logging_config.yaml
#COPY ./words_alpha.txt /workbench/words_alpha.txt

# set to no debugger.
ENV DEBUGGER=False
ENV WAIT=False

USER appuser
EXPOSE 8080
CMD ["python3", "-u", "./service.py"]