from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from datetime import date

sc = SparkContext()
spark = SparkSession(sc)

movies = spark.read.format('delta').load("gs://teste-caio/movie_ratings/delta/movies")
movies.registerTempTable("movies")

ratings = spark.read.format('delta').load("gs://teste-caio/movie_ratings/delta/ratings")
ratings.registerTempTable("ratings")

most_rated_movies_query = """
SELECT m.movieId, m.title, COUNT(r.rating) as ratings_count, MEAN(r.rating) as ratings_mean
FROM ratings as r
INNER JOIN movies as m on m.movieID = r.movieID
GROUP BY m.movieID, m.title
ORDER BY ratings_count DESC
LIMIT 1000 
"""
most_rated_movies = spark.sql(most_rated_movies_query)
most_rated_movies.registerTempTable("most_rated_movies")


most_and_better_rated_movies_query = """
SELECT mrm.*, current_date() as date FROM most_rated_movies mrm
ORDER BY ratings_mean DESC
LIMIT 100
"""

most_and_better_rated_movies = spark.sql(most_and_better_rated_movies_query)

most_and_better_rated_movies.write \
    .format("jdbc") \
    .option("driver", "com.mysql.jdbc.Driver") \
    .option("url", "jdbc:mysql://terraform-instance.southamerica-east1-b.c.sincere-bongo-264115.internal:3307/test") \
    .option("dbtable", "top_movies") \
    .mode("append") \
    .option("user", "root") \
    .option("password", "12345") \
    .save()