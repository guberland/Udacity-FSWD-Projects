# P3_Logs Analysis Project

This is the third Undacity Full Stack Nanodegree project, the project 
executes queries and output the answers to the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?  

## Prerequisites

python 3 and psycopg2 to access provided postgreSQL

## What is in the project

P3_Log_Analysis.py

output.txt

README.md

## How to run the project

```
1.Download and unzip the data using the following link:
  https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

2.put the newsdata.sql extracted from downloaded zip in the same folder
as P3_Log_Analysis.py or if you are using vagrant, place it into
the vagrant directory

3.to load the data, use the command psql -d news -f newsdata.sql.

4.now the tables are created and populated with data, you can view the tables using psql -d news or run the script P3_Log_Analysis.py

```

## Project detail
 
### P3_Log_Analysis.py

```
	This file contains five functions with three of them being
query functions.

	get_top_arti() select columns from log and articles table and join them
with articles.slug and log.path to output the top three most viewed articles. 

	get_top_author() select columns from log,author,articles table and join
 them with articles.slug to log.path and articles.author to authors.id to output the 
top three most viewed authors.

	error_day() has two views created; normtraffic and badtraffic. normtraffic 
provides all traffic detail on all days in log table while badtraffic provides all
404 bad request on all days. the two table then joined to output the days that have
more than 1% of error rate.

	print_view() and print_error() are helper functions that modify the output
of the queries into more human readable result.

```


## Built With

LiClipse (python3)


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

Chao Jiang

