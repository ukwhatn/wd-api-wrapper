FROM python:3.12.1-slim

# ser workdir
WORKDIR /app

RUN apt update && apt upgrade -y && apt install -y libpq-dev gcc

# copy requirements
COPY ./server/requirements.txt /temp/requirements.txt

# install requirements
RUN pip install --no-cache-dir --upgrade -r /temp/requirements.txt

# copy app
COPY ./server/app /app

# run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]