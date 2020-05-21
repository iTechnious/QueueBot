import pymysql
from statics import config as conf

def init_db(client):
    connection = pymysql.connect(
        host=conf.mysql["host"],
        port=conf.mysql["port"],
        user=conf.mysql["user"],
        password=conf.mysql["pass"]
    )

    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS %s" % conf.mysql["db"])
        connection.commit()
        connection.close()

    connection = pymysql.connect(
        host=conf.mysql["host"],
        port=conf.mysql["port"],
        user=conf.mysql["user"],
        password=conf.mysql["pass"],
        db=conf.mysql["db"]
    )
    with connection.cursor() as cursor:
        for guild in client.guilds:
            name = int(guild.id)
            name = "_%s" % str(name)
            print("checking config for server '%s' (%s)" %(str(guild.name), int(guild.id)))
            
            cursor.execute('CREATE TABLE IF NOT EXISTS %s ('
                           "id INT(20) AUTO_INCREMENT PRIMARY KEY,"
                           "setting VARCHAR(100),"
                           "value VARCHAR(100)"
                           ")" % str(name))
            if cursor.execute("SELECT * FROM %s" % name) == 0:
                cursor.execute("INSERT INTO %s (setting, value) VALUES ('prefix', '!')" % name)

        print()
    connection.commit()
    connection.close()

    return True
