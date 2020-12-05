import os

import json
from bson.json_util import dumps, loads
import pandas as pd

import sqlite3
import pymongo
from pymongo import MongoClient

try:
    USERPASS = os.environ["MONGODBUSERPASS"]
except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
    USERPASS = os.environ.get("MONGODBUSERPASS")


def get_data(database_name=None, collection_name=None):
    cluster = MongoClient(URI)

    try:
        if database_name is None:
            return cluster
        elif collection_name is None:
            return cluster[database_name]
        else:
            return cluster[database_name][collection_name]
    except ValueError:
        return None


URI = f"mongodb+srv://hamood:{USERPASS}@hamoodrest.2kacm.mongodb.net/hamoodrest?retryWrites=true&w=majority"


class DiscordSQL:
    def __init__(self):

        self.sql_loc = (
            f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/sql"
        )

        self.discord_connection = sqlite3.connect(f"{self.sql_loc}/discord.db")
        self.cursor = self.discord_connection.cursor()

        self.create_db()
        self.clear_db()
        self.sql_download_database()

    def create_db(self):
        try:
            self.cursor.execute("""CREATE TABLE prefixes (_id, prefix)""")
            self.cursor.execute("""CREATE TABLE servers (_id, categories)""")
        except sqlite3.OperationalError:
            return

    def clear_db(self):
        try:
            self.cursor.execute("""DELETE from prefixes""")
        except sqlite3.OperationalError:
            pass

    def sql_download_database(self):
        prefix_data = get_data("discord", "prefixes")
        prefix_data = [(i["_id"], i["prefix"]) for i in list(prefix_data.find({}))]
        self.cursor.executemany("INSERT INTO prefixes VALUES (?,?)", prefix_data)
        self.discord_connection.commit()

        server_data = get_data("discord", "servers")
        server_data = [(i["_id"], i["categories"]) for i in list(server_data.find({}))]
        self.cursor.executemany("INSERT INTO servers VALUES (?,?)", server_data)
        self.discord_connection.commit()

    def print_db(self):
        for row in self.cursor.execute("SELECT * FROM prefixes ORDER BY _id"):
            print(row)


MONGOSQL = DiscordSQL()
MONGOSQL.print_db()

# clear_db()
# def sql_download_database()
# conn = sqlite3.connect(f"{sql_loc}prefixes.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE prefixes
#              (_id, prefix)"""
# )

# cluster = MongoClient(URI)
# data = cluster["discord"]["prefixes"]
#

# c.executemany("INSERT INTO prefixes VALUES (?,?)", data)


# print(data)
# for post in data:
#     c.execute(f"INSERT INTO stocks VALUES ({post})")

# Insert a row of data
#

# Save (commit) the changes
# conn_prefixes.commit()
# for row in cp.execute("SELECT * FROM prefixes ORDER BY _id"):
#     print(row)
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
# conn_prefixes.close()


# def search(mongo_dict, key):
#     df = pd.DataFrame(mongo_dict)
#     try:
#         df2 = df[df["_id"] == key]
#     except KeyError:
#         return None
#     item = df2.to_dict("records")
#     if item == [] or item is None:
#         return None

#     return item[0]


# def download_database(database_name=None, collection_name=None, file_name=None):
#     cluster = MongoClient(URI)

#     try:
#         data = cluster[database_name][collection_name]
#         data = list(data.find({}))
#         data = dumps(data, indent=2)
#     except ValueError:
#         return False

#     name = collection_name if file_name is None else file_name

#     with open(name, "w") as file:
#         file.write(data)

#     return True


def update_prefix_post(guild_id=None, prefix="."):
    collection = get_data("discord", "prefixes")
    collection.update_one({"_id": guild_id}, {"$set": {"prefix": prefix}})

    return True


def update_server_post(guild_id=None, name=None, value=None):
    collection = get_data("discord", "servers")

    collection.update_one({"_id": guild_id}, {"$set": {name: value}})
    # collection.update_one(
    #     {"_id": guild_id}, {"$set": {f"categories.{category}": value}}
    # )

    return True


def insert_prefix_post(guild_id):
    post = {"_id": guild_id, "prefix": "."}

    collection_name = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/prefixes.json"
    collection = json.load(open(collection_name)).append(post)

    with open(collection_name, "w") as fp:
        json.dump(collection, fp)

    get_data(database_name="discord", collection_name="prefixes").insert_one(post)

    return True


def insert_server_post(guild_id):
    post = {
        "_id": guild_id,
        "categories": {
            "About": True,
            "Avatarmemes": True,
            "Chance": True,
            "Chemistry": True,
            "Events": True,
            "Fonts": True,
            "Fun": True,
            "Games": True,
            "General": True,
            "Images": True,
            "Math": True,
            "Memes": True,
            "Mod": True,
            "Pokemon": True,
            "Reddit": True,
            "User": True,
            "Web": True,
        },
    }

    collection_name = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/prefixes.json"
    collection = json.load(open(collection_name)).append(post)

    with open(collection_name, "w") as fp:
        json.dump(collection, fp)

    get_data(database_name="discord", collection_name="servers").insert_one(post)

    return True


# def insert_prefix_post(guild_id, collection=None):
#     post = {"_id": guild_id, "prefix": "."}

#     if collection is None:
#         collection = get_data(database="discord", collection="prefixes")
#     collection


# def insert_server_post(guild_id, collection=None):
#     post = {
#         "_id": guild_id,
#         "categories": {
#             "About": True,
#             "Avatarmemes": True,
#             "Chance": True,
#             "Chemistry": True,
#             "Events": True,
#             "Fonts": True,
#             "Fun": True,
#             "Games": True,
#             "General": True,
#             "Images": True,
#             "Math": True,
#             "Memes": True,
#             "Mod": True,
#             "Pokemon": True,
#             "Reddit": True,
#             "User": True,
#             "Web": True,
#         },
#     }

#     if collection is None:
#         collection = get_data(database="discord", collection="servers")
#     collection.insert_one(post)

#     return True

