FROM python:3.12-slim

WORKDIR /workspace

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y cron

RUN crontab -l | { cat; echo "0 7 * * * /usr/local/bin/python /workspace/app.py >> /var/log/cron.log 2>&1"; } | crontab -

CMD ["cron", "-f"]