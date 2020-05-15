from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.types import *

sc = SparkContext()
spark = SparkSession(sc)

# READING STREAMING DATA FROM KAFKA
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "instance-1.southamerica-east1-a.c.sincere-bongo-264115.internal:9092") \
  .option("subscribe", "movieRatings") \
  .load()

# SETTING SCHEMA AND FORMATTING STREAMING DATA
schema = StructType([ 
                        StructField("userId", IntegerType(), True),
                        StructField("movieId", StringType(), True),
                        StructField("rating", FloatType(), True),
                        StructField("timestamp", FloatType(), True)
                    ])
                        
data = df.selectExpr("CAST(value AS STRING)")\
        .select(from_json("value", schema).alias("data")).select("data.*")

# WRITING STREAMING DATA TO DELTA LAKE
( data
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "gs://teste-caio/movie_ratings/delta/ratings/_checkpoints/etl-from-kafka")
    .start("gs://teste-caio/movie_ratings/delta/ratings") )