"""
This file contains methods that contain more complex SQL queries than the basic
"""


def query_sql(date_from, date_to):
    query = f"""SELECT count(likes.like) FILTER (WHERE likes.like = true) as likes,  \
                    count(likes.like) FILTER (WHERE likes.like = false) as unlikes,  \
                    DATE(likes.date)  \
                    FROM likes  \
                    WHERE DATE(likes.date) BETWEEN {date_from!r} AND {date_to!r}  \
                    GROUP BY DATE(likes.date)  \
                    ORDER BY DATE(likes.date)"""
    return query
