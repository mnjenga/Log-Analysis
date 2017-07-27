#!/usr/bin/python3.6
#
# Web site Log analysis
#

import psycopg2

# connect to db and print if successful or not
try:
    conn = psycopg2.connect("dbname='news' ")
    print ("Connected to database")
except:
    print ("Unable to connect to the database")

# Querry Database for 3 most popular articles
cur = conn.cursor()

# create a view from log editing path to match slug
cur.execute("""
CREATE VIEW view_count AS
SELECT split_part( path, '/', 3) AS path,
       count(*) AS total
FROM log
WHERE path SIMILAR TO '/article/%'
AND status = '200 OK'
GROUP BY path
ORDER BY total DESC;

""")

# make a join query from count_view and articles to get the most read articles

cur.execute("""
SELECT articles.title,
  total
FROM articles
INNER JOIN view_count ON articles.slug = view_count.path
ORDER BY total DESC
LIMIT 3;

""")
rows = cur.fetchall()
f1 = "\n Most popular three articles of all time:\n"
print f1
for row in rows:
    f1 += "\n" + "  " + str(row[0]) + " - " + str(row[1]) + " views" + "\n"
    print "  ", row[0], "-", row[1], "views"

# Querry Database for most Popular Authors

cur.execute("""
SELECT authors.name as name,
       sum(total) as total
FROM articles
INNER JOIN view_count ON view_count.path  = articles.slug
INNER JOIN authors ON articles.author = authors.id
GROUP BY authors.name
ORDER BY total DESC;

""")
rows = cur.fetchall()
f2 = "\n Most popular article authors of all time:\n"
print f2
for row in rows:
    f2 += "\n" + "  " + str(row[0]) + " - " + str(row[1]) + " views" + "\n"
    print "  ", row[0], "-", row[1], "views"

# Create views to facilitate comparison errors agains total requests
cur = conn.cursor()

cur.execute("""
CREATE VIEW daily_errors AS
SELECT date(TIME) AS date,
       count(*) AS num
FROM log
WHERE status = '404 NOT FOUND'
GROUP BY date(log.time);

""")

cur.execute("""
CREATE VIEW daily_requests AS
SELECT date(TIME) AS date,
       count(*) AS total
FROM log
GROUP BY date(log.time);

""")

# Querry the views to get error percentage

cur.execute("""
SELECT daily_errors.date,
  round(num * 100.00 / total,2) AS per
FROM daily_errors
INNER JOIN daily_requests ON daily_errors.date = daily_requests.date
ORDER BY per DESC;

""")
rows = cur.fetchall()
f3 = "\n Days with more than 1% Errors on requests:\n"
print f3
for row in rows:
    if row[1] > 1:
        f3 += "\n" + "  " + str(row[0]) + " - " + str(row[1]) + "%" + "\n"
        print "  ", row[0], "-", row[1], "%"

fo = open("log_report.txt", "w")
fo.write("%s \n\n %s \n\n %s" % (str(f1), str(f2), str(f3)))
fo.close()
