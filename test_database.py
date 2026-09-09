from database.connection import client, db


try:
    client.admin.command("ping")
    print("MongoDB connection successful")
    print("Database:", db.name)

except Exception as e:
    print("MongoDB connection failed:")
    print(e)