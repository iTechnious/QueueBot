import pymysql
from statics import config as conf

def change_setting(guild, setting, value):
    connection = pymysql.connect(
        host=conf.mysql["host"],
        port=conf.mysql["port"],
        user=conf.mysql["user"],
        password=conf.mysql["pass"],
        db=conf.mysql["db"]
    )

    with connection.cursor() as cursor:
        cursor.execute("UPDATE _%s SET value='%s' WHERE setting='%s'" % (str(guild), str(value), str(setting)))
        connection.commit()
    connection.close()

    return True


def get_setting(guild, setting):
    connection = pymysql.connect(
        host=conf.mysql["host"],
        port=conf.mysql["port"],
        user=conf.mysql["user"],
        password=conf.mysql["pass"],
        db=conf.mysql["db"]
    )
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM _%s WHERE setting='%s'" % (str(guild), str(setting)))
        res = cursor.fetchone()

    connection.close()

    return str(res[2])
