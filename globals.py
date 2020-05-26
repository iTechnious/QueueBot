import pymysql
import discord

from statics import config as conf
from statics import messages


global music
music = {}
global tickets
tickets = {}
    

def change_setting(guild, setting, value):
    connection = pymysql.connect(
        host=conf.mysql["host"],
        port=conf.mysql["port"],
        user=conf.mysql["user"],
        password=conf.mysql["pass"],
        db=conf.mysql["db"]
    )

    with connection.cursor() as cursor:
        if cursor.execute("SELECT * FROM _%s WHERE setting='%s'" % (str(guild), str(setting))) > 0:
            cursor.execute("UPDATE _%s SET value='%s' WHERE setting='%s'" % (str(guild), str(value), str(setting)))
        else:
            cursor.execute("INSERT INTO _%s (setting, value) VALUES ('%s', '%s')" % (str(guild), str(setting), str(value)))
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

    if res[2] is not None:
        return str(res[2])
    else:
        return None


def language_pack(guild, use):
    lang = get_setting(str(guild), "lang")
    default_lang = "En"
    try:
        pack = getattr(messages, lang)
    except AttributeError:
        pack = getattr(messages, default_lang)

    try:
        message = getattr(pack, use)
    except AttributeError:
        try:
            message = getattr(getattr(messages, default_lang), use)
        except AttributeError as error:
            return discord.Embed(title="Internal error",
                                 description="Please send this to your admin or notify the Queue support.\n"
                                             "Technical error:\n" + str(error),
                                 color=discord.Color.red())

    return message
