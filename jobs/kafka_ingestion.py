from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import time

sc = SparkContext()
spark = SparkSession(sc)

# READING STREAMING DATA FROM KAFKA
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "terraform-instance.southamerica-east1-b.c.sincere-bongo-264115.internal:9094") \
  .option("subscribe", "movieRatings") \
  .option("failOnDataLoss", False) \
  .load()

# SETTING SCHEMA AND FORMATTING STREAMING DATA
schema = StructType([ 
                        StructField("userId", IntegerType(), True),
                        StructField("movieId", IntegerType(), True),
                        StructField("rating", DoubleType(), True),
                        StructField("timestamp", IntegerType(), True)
                    ])
                        
data = df.selectExpr("CAST(value AS STRING)")\
        .select(from_json("value", schema).alias("data")).select("data.*")

# WRITING STREAMING DATA TO DELTA LAKE
query = ( data
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "gs://teste-caio/movie_ratings/delta/ratings/_checkpoints/etl-from-kafka")
    .start("gs://teste-caio/movie_ratings/delta/ratings") )

time.sleep(30)
print(query.status)
print(query.lastProgress)

# while True:
#   time.sleep(30)
#   print(query.status)
#   print(query.lastProgress)