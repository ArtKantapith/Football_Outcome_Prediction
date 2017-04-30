import sqlite3
import numpy
import scipy
import pandas


with sqlite3.connect("../data/database.sqlite") as db:
    Match = pandas.read_sql_query("select * from Match", db, index_col= "id")
    playerAttributes = pandas.read_sql_query("select * from Player_Attributes",db, index_col = "id")


print list(Match)
