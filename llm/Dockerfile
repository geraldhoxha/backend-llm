FROM python:3.12 AS builder

WORKDIR /backendllmmodel

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . .


FROM python:3.12-slim AS runtime

WORKDIR /appmodel

COPY --from=builder /backendllmmodel /appmodel
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

EXPOSE 81

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "81"]
