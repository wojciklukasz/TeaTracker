FROM python:3.10.14-slim-bookworm

EXPOSE 8000
WORKDIR /TeaTracker

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT [ "/TeaTracker/entrypoint.sh"]