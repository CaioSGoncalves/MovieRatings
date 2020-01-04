import numpy as np
import pandas as pd

movies = pd.read_csv("movies.csv")
print("len(movies)", len(movies))

ratings = pd.read_csv("ratings.csv")
print("len(ratings)", len(ratings))


grouped_movies = ratings.groupby("movieId").agg(ratings_count=('rating', 'count'), ratings_mean=('rating', 'mean'))
most_rated_movies = grouped_movies.sort_values("ratings_count", ascending=False).head(1000)

# print(most_rated_movies.head())


highest_rated_movies = most_rated_movies.sort_values("ratings_mean", ascending=False).head(100)
# print(highest_rated_movies.head())

highest_rated_movies_with_name = pd.merge(highest_rated_movies, movies, on="movieId")[["movieId", "title", "ratings_mean"]]
print(highest_rated_movies_with_name.head())