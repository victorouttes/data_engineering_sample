#!/bin/bash

airflow db check || airflow db init

user_exists=$(airflow users list --output json)

if [ -z "$user_exists" ]; then
  airflow users create \
    --username admin \
    --password admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com
fi
