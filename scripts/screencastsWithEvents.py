from pymongo import MongoClient
from fuzzywuzzy import fuzz

def execute():
    # Conectar a la base de datos
    client = MongoClient("mongodb://localhost:27017")
    db = client["micrometrics"]
    col = db["screencast"]

    # Pipeline de agregación para todos los screencasts
    pipeline = [
        {"$unwind": "$events"},
        {
            "$lookup": {
                "from": "screencastEvent",
                "localField": "events.__id",
                "foreignField": "_id",
                "as": "eventDetails",
            }
        },
        {"$unwind": "$eventDetails"},
        {
            "$match": {
                "eventDetails.values.data.source": 5,
            }
        },
        {"$sort": {"eventDetails.timestamp": 1}},
        {
            "$group": {
                "_id": "$_id",
                "events": {"$push": "$events"},
                "eventDetails": {"$push": "$eventDetails"},
            }
        },
    ]

    # Ejecutar el pipeline y procesar todos los screencasts
    temp_col = db["tempcols"]
    temp_col.drop()  # Limpiar la colección temporal

    screencasts = list(col.aggregate(pipeline, allowDiskUse=True))

    # Procesar cada screencast en los resultados de la consulta
    for cast in screencasts:
        previous = cast['eventDetails'].copy()
        previous.pop()

        next = cast['eventDetails'].copy()
        next.pop(0)

        newEventsDetails = []
        saveFirst = True
        for previousEvent, nextEvent in zip(previous, next):
            ratio = fuzz.ratio(previousEvent["values"]["data"]["text"], nextEvent["values"]["data"]["text"])

            if (ratio > 66):
                if (saveFirst):
                    newEventsDetails.append(previousEvent)
                    saveFirst = False
                newEventsDetails.append(nextEvent)
            else:
                if (not saveFirst):
                    saveFirst = True
                    obj = {
                        "type": "inputEnd",
                        "timestamp": previousEvent["values"]["timestamp"] + 1
                    }
                    newEventsDetails.append(obj)
            
        cast['eventDetails'] = newEventsDetails
        temp_col.insert_one(cast)

    print("Agrupación completada para todos los screencasts con coincidencias acumuladas")


# Ejecutar el script
execute()
