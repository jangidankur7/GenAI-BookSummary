FROM python:3.10-slim

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./  /app/

# RUN pip3 install -r /app/requirements.txt

# COPY ./app /code/app
# CMD ["fastapi", "dev", "main.py", "--port", "8000"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]