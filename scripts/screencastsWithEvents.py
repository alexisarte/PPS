from pymongo import MongoClient
from fuzzywuzzy import fuzz
from bson import ObjectId

def execute():
    # Conectar a la base de datos
    client = MongoClient("mongodb://localhost:27017")
    db = client["micrometrics"]
    col = db["screencast"]

    # Pipeline de agregación para todos los screencasts
    pipeline = [
        # {
        #     '$match': { 
        #         '_id': ObjectId("5f595f9256a02beea66b3825")
        #     }
        # },
        {"$unwind": "$events"},
        {
            "$lookup": {
                "from": "screencastEvent",
                "localField": "events.__id",
                "foreignField": "_id",
                "as": "logs",
            }
        },
        {"$unwind": "$logs"},
        {
            "$match": {
                "logs.values.data.source": 5,
            }
        },
        {"$sort": {"logs.timestamp": 1}},
        {
            "$group": {
                "_id": "$_id",
                "logs": {"$push": "$logs"},
            }
        },
    ]

    # Ejecutar el pipeline y procesar todos los screencasts
    temp_col = db["screencastswithevents"]
    temp_col.drop()  # Limpiar la colección temporal

    screencasts = list(col.aggregate(pipeline, allowDiskUse=True))

    # Procesar cada screencast en los resultados de la consulta
    for cast in screencasts:
        previous = cast['logs'].copy()
        previous.pop()

        next = cast['logs'].copy()
        next.pop(0)

        newLogs = []
        saveFirst = True
        for previousEvent, nextEvent in zip(previous, next):
            print("previousEvent", previousEvent["values"]["data"]["text"])
            ratio = fuzz.ratio(previousEvent["values"]["data"]["text"], nextEvent["values"]["data"]["text"])
            if (ratio > 66):
                if (saveFirst):
                    newLogs.append(previousEvent)
                    saveFirst = False
                newLogs.append(nextEvent)
            else:
                if (not saveFirst):
                    saveFirst = True
                    obj = {
                        "type": "inputEnd",
                        "timestamp": previousEvent["values"]["timestamp"] + 1
                    }
                    newLogs.append(obj)
            
        cast['logs'] = newLogs
        temp_col.insert_one(cast)

    print("Agrupación completada para todos los screencasts con coincidencias acumuladas")


# Ejecutar el script
execute()
