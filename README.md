# MovieRatings
Processing MovieLens latest data: https://grouplens.org/datasets/movielens/latest/


Data:
  - movie.csv: Movie data
  - rating.csv: Rating data

 Job:
  - Select TOP 1000 most rated movies
  - Then Select TOP 10 highest rated movies

Batch:
  - Daily Job
  - Delta Lake -> Spark -> json (Datetime -> Result)

Streaming:
  - 1 hour window
  - Apache Kafka -> Spark -> Delta Lake

Tech-Stack:
  - Apache Spark: used as processing framework
  - Apache Zeppelin: used as playground and data visualzations
  - Apache Airflow: used as scheduler
  - GCP Pub/Sub or Apache Kakfa: used as message queue event
  - GCP Storage: used as Data Lake
  - Delta Lake: layer that brings ACID and Schema Validation for Data Lakes