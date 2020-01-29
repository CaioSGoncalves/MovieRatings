#!/bin/bash

apt-get update -y
apt install python -y
apt-get install software-properties-common -y
apt-get install python-pip -y
export SLUGIFY_USES_TEXT_UNIDECODE=yes
pip install apache-airflow
airflow initdb
airflow webserver -p 8080