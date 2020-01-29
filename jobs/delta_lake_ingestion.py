from pyspark import SparkContext
from pyspark.sql.session import SparkSession

sc = SparkContext()
spark = SparkSession(sc)

# Ingest MOVIES data to Delta Lake
movies = spark.read.format('csv').options(header='true', inferSchema='true').load("gs://teste-caio/movies.csv")
movies.write.format("delta").save("gs://teste-caio/delta/movies")

# Ingest RATINGS data to Delta Lake
ratings = spark.read.format('csv').options(header='true', inferSchema='true').load("gs://teste-caio/ratings.csv")
ratings.write.format("delta").save("gs://teste-caio/delta/ratings")