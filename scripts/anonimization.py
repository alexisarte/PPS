from pymongo import MongoClient
from bson import ObjectId 
import random
import string
import spacy

def execute():
    # Conectar a la base de datos
    client = MongoClient("mongodb://localhost:27017")
    db = client["micrometrics"]
    collection = db["screencastswithevents"]

    # Pipeline de agregación para todos los screencasts
    pipeline = [
        # {
        #     '$match': { 
        #         '_id': ObjectId("5f595f9256a02beea66b3825")
        #     }
        # },
        # {
        #     "$group": {
        #         "_id": "$_id",
        #         "logs": {"$push": "$logs"},
        #     }
        # },
    ]

    # Ejecutar el pipeline y procesar todos los screencasts
    temp_col = db["screencastsewithevents"]
    anomization_col = db["anomization"]
    anomization_col.drop()  # Limpiar la colección temporal

    screencasts = list(collection.aggregate(pipeline, allowDiskUse=True))

    # Procesar cada screencast en los resultados de la consulta
    for cast in screencasts:
        if len(cast['logs']) < 2:
            continue  # Saltar si no hay suficientes eventos
        previous = cast['logs'].copy()
        previous.pop()

        next = cast['logs'].copy()
        next.pop(0)

        logs = []
        logsModificados = []
        max = -1
        input = None
        saveFirst = True
        for previousEvent, nextEvent in zip(previous, next):
            if previousEvent.get("type"):
                # input es none cuando un screencast no tiene eventos de tipo input
                if input is not None:
                    input_text = input["values"]["data"]["text"]
                    if input_text.isdigit():
                        primera_parte = input_text[0:int((len(input_text) / 2))]
                        segunda_parte = input_text[int(len(input_text) / 2):int(len(input_text))]
                        segunda_parte = "".join(["*" for _ in segunda_parte])
                        input["values"]["data"]["text"] = primera_parte + segunda_parte
                        # Copiar la anonimización a cada subinput
                        for log in logs:
                            log_text = log["values"]["data"]["text"]
                            if log_text.isdigit():
                                # Encontrar la posición del subinput en el input final
                                start_index = input_text.find(log_text)
                                if start_index != -1:
                                    end_index = start_index + len(log_text)
                                    log["values"]["data"]["text"] = input["values"]["data"]["text"][start_index:end_index]
                            logsModificados.append(log)
                    # else:
                    #     input["values"]["data"]["text"] = ''.join(random.choices(string.ascii_letters + string.digits, k=len(input_text)))
                    
                        # anomization_col.insert_one(input)
                    input = nextEvent
                    max = len(nextEvent["values"]["data"]["text"])
                    logs = []
            else:
                if len(previousEvent["values"]["data"]["text"]) > max:
                    input = previousEvent
                    max = len(previousEvent["values"]["data"]["text"])
                if previousEvent["values"]["data"]["text"].isdigit():
                    logs.append(previousEvent)
        cast['logs'] = logsModificados
        logsModificados = []
        anomization_col.insert_one(cast) 
    print("Anonimización completada para todos los screencasts")

# Ejecutar el script
execute()