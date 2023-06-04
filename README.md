# Data Engineering Sample
Data engineering project sample.

## Requirements
* Docker
* Docker compose

## Usage
The services must be started in that order:

1 - Minio
```
cd minio
docker-compose -f .\minio.yml up
```
2 - Airflow
```
cd airflow
docker-compose -f .\airflow.yml up
```
3 - Dremio
```
cd dremio
docker-compose -f .\dremio.yml up
```

## Service Access
1 - Minio
* http://127.0.0.1:9001/
* login: minio
* password: minio123

2 - Airflow
* http://localhost:8080/
* login: admin
* password: admin

3- Dremio
* http://localhost:9047/
* You must create the credentials on first access
* login: admin
* password: admin123


## Other Configuration
Airflow connection to Minio:

* Go to Admin > Connections.
* In connection type, put S3.
* In extra field, put: 
```
{"aws_access_key_id": "<minio_access>", "aws_secret_access_key": "<minio_secret>", "host": "http://172.24.0.2:9000"}
```
* the 172.24.0.2 is the IP informed by minio when it starts! It may change in your environment. Run `docker logs <minio_container>` to see the true IP.

Dremio connection to Minio:

* Add a Amazon S3 Source.
* In General menu, select AWS Access Key and put the keys from Minio. Also, uncheck the encryption option.
* In Advanced Options menu, check "Enable compatibility mode" and add these 2 connection properties:
```
fs.s3a.path.style.access = true
fs.s3a.endpoint = 172.24.0.2:9000
```
* Once again, this IP 172.24.0.2 is informed by minio when it starts and may vary.

