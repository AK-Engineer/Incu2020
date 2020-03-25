import pymongo
from config import url
from read_file import interfaces_final

# Using pymongo to establish connection
with pymongo.MongoClient(url) as client:
    db = client.Device_Configuration
    collection = db.Interfaces
    print(len(interfaces_final))

#Insert in database the .txt file data
#------------------------------------! RUN ONLY ONCE TO INSERT DATA !---------------------
    for i in range(len(interfaces_final)):
        interface = interfaces_final[i]
        document_id = collection.insert_one(interface).inserted_id
        print(f'Created a document with id: {document_id}')



