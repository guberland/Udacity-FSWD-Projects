#!/usr/bin/env python3
import psycopg2
import re

DBNAME = "news"


def executeQuery(query):
    """execute the input SQL query and return """
    """the result as a list of tuples """
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute(query)
        posts = c.fetchall()
        db.close()
        return posts
    except(Exception, psycopg2.Databaseerror) as error:
        print(error)
    finally:
        if c is not None:
            c.close()


def printView(a):
    """ print Q1 and Q2 to a more readable format """
    for i in a:
        print(' - "{}" -- {} views'.format(i[0], i[1]))


def printError(a):
    """ print Q3 to a more readable format """
    for i in a:
        print(' - "{}" -- {}% errors'.format(re.sub(' ', '', i[0]), i[1]))


topArticle = ("SELECT articles.title,count(log.path) AS views "
              "FROM log, articles "
              "WHERE articles.slug = substring(log.path from 10) "
              "GROUP BY articles.title "
              "ORDER BY views desc "
              "LIMIT 3")


topAuthor = ("SELECT authors.name,count(log.path) AS views "
             "FROM log,articles,authors "
             "WHERE articles.author = authors.id "
             "AND articles.slug = substring(log.path from 10) "
             "GROUP BY authors.name "
             "ORDER BY views desc ")


errorDay = ("CREATE VIEW normtraffic AS "
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
if __name__ == '__main__':
    print("1. What are the most popular three articles of all time? ")
    printView(executeQuery(topArticle))
    print('\n')
    print("2. Who are the most popular article authors of all time? ")
    printView(executeQuery(topAuthor))
    print('\n')
    print("3. On which days did more than 1% of requests lead to errors? ")
    printError(executeQuery(errorDay))
print('\n')
