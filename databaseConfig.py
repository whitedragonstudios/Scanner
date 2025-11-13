#Default setitng for the Postgre Database
def databaseSettings():
    return {"user" :"marcus",
        "password" : "stoic",
        "db_name" : "scanner",
        "port" : 5000,
        "host" : "localhost"}

def databseAdmin(database = "postgres"):
    return {"user" :"postgres",
        "password" : "stoic",
        "db_name" : database or "postgres",
        "port" : 5000,
        "host" : "localhost"}
