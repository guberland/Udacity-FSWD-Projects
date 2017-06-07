#!/usr/bin/env python3
import psycopg2
import re

DBNAME = "news"


def get_top_arti():
    # returns duple of top three most popluar articles with title and views
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT articles.title,count(log.path) AS views "
              "FROM log, articles "
              "WHERE articles.slug = substring(log.path from 10) "
              "GROUP BY articles.title "
              "ORDER BY views desc "
              "LIMIT 3"

              )
    posts = c.fetchall()
    db.close()
    return posts


def get_top_author():
    # returns duple of top three most popluar author with title and views
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT authors.name,count(log.path) AS views "
              "FROM log,articles,authors "
              "WHERE articles.author = authors.id "
              "AND articles.slug = substring(log.path from 10) "
              "GROUP BY authors.name "
              "ORDER BY views desc "
              "LIMIT 3"

              )
    posts = c.fetchall()
    db.close()
    return posts


def error_day():
    # returns duple of days that contain more than 1% error
    # with date and percentage
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("CREATE VIEW normtraffic AS "
              "SELECT date(time),cast(count(status) AS float) AS norm "
              "FROM log "
              "GROUP BY date(time); "
              "CREATE VIEW badtraffic AS "
              "SELECT date(time),cast(count(status) AS float) AS faulty "
              "FROM log "
              "WHERE status LIKE '404%' "
              "GROUP BY date(time); "
              "SELECT to_char(normtraffic.date,'Month,DD,YYYY'),"
              "cast(faulty*100/norm AS decimal(4,2)) "
              "FROM normtraffic,badtraffic "
              "WHERE normtraffic.date=badtraffic.date "
              "AND faulty*100/norm >= 1")
    posts = c.fetchall()
    db.close()
    return posts


def print_view(a):
    # print Q1 and Q2 to a more readable format
    for i in a:
        print('"{}" -- {} views'.format(i[0], i[1]))


def print_error(a):
    # print Q3 to a more readable format
    for i in a:
        print('"{}" -- {}% errors'.format(re.sub(' ', '', i[0]), i[1]))
print_view(get_top_arti())
print('\n')
print_view(get_top_author())
print('\n')
print_error(error_day())
print('\n')
