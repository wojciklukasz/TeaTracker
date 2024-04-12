FROM python:3.10.14-slim-bookworm

EXPOSE 8000
WORKDIR /TeaTracker

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY tea ./tea
COPY TeaTracker ./TeaTracker
COPY templates ./templates
COPY static ./static
COPY entrypoint.sh .
COPY manage.py .

RUN useradd -ms /bin/bash teauser
RUN chown -R teauser:teauser /TeaTracker
RUN chmod 755 /TeaTracker

USER teauser
ENTRYPOINT [ "/TeaTracker/entrypoint.sh"]