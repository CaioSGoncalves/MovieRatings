FROM python:3.6

COPY requirements.txt ./requirements.txt
WORKDIR ./
RUN pip install -r requirements.txt
COPY . .
# EXPOSE 5000

CMD ["python3", "main.py"]