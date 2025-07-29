FROM python:3-alpine

RUN apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers python3-dev && \
    apk add --no-cache aws-cli git openssh gpg

RUN adduser -D -h /techlens techlens
WORKDIR /techlens

COPY --chown=techlens:techlens requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf requirements.txt && \
    apk del .build-deps

COPY --chown=techlens:techlens src/techlens_agent /techlens/techlens_agent
RUN mv /techlens/techlens_agent/agent.py /techlens/agent.py

USER techlens

ENTRYPOINT ["python", "/techlens/agent.py"]
CMD []
