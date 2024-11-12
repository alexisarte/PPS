from pymongo import MongoClient
from bson import ObjectId 
import random
import string
import spacy
import requests

# Cargar el modelo de spaCy para español
nlp = spacy.load("es_core_news_sm")

def es_nombre(texto):
    doc = nlp(texto)
    for entidad in doc.ents:
        if entidad.label_ == "PER":
            return True
    return False

def obtener_nombre_ficticio(longitud):
    while True:
        response = requests.get('https://randomuser.me/api/?nat=es')
        if response.status_code == 200:
            data = response.json()
            nombre = data['results'][0]['name']['first']
            if len(nombre) == longitud:
                return nombre
            else:
                print(f"El nombre '{nombre}' no tiene la longitud correcta.")
                # return ''.join(random.choices(string.ascii_letters, k=longitud))
        else:
            # Si la API falla, generar un nombre aleatorio
            return ''.join(random.choices(string.ascii_letters, k=longitud))

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
    anonymizations_col = db["anonymizations"]
    anonymizations_col.drop()  # Limpiar la colección temporal

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
        max_length = -1
        input = None
        input_text = ''
        for previousEvent, nextEvent in zip(previous, next):
            if previousEvent.get("type"):
                # input es none cuando un screencast no tiene eventos de tipo input
                if input is not None:
                    if es_nombre(input_text):
                        print(f"El texto '{input_text}' es un nombre.")
                        nombre_ficticio = obtener_nombre_ficticio(len(input_text))
                        input["values"]["data"]["text"] = nombre_ficticio
                        print(f"El nombre '{input_text}' ha sido anonimizado como '{nombre_ficticio}'.")
                        logsModificados.append(input)
                    if input_text.isdigit():
                        primera_parte = input_text[0:int((len(input_text) / 2))]
                        segunda_parte = input_text[int(len(input_text) / 2):int(len(input_text))]
                        segunda_parte = "".join(["*" for _ in segunda_parte])
                        if "values" in input:
                            input["values"]["data"]["text"] = primera_parte + segunda_parte
                        else:
                            print('input', input)
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
                input = nextEvent

                if "values" in nextEvent and "data" in nextEvent["values"] and "text" in nextEvent["values"]["data"]:
                    max_length = len(nextEvent["values"]["data"]["text"])
                logs = []
            else:
                if "values" in previousEvent and "data" in previousEvent["values"] and "text" in previousEvent["values"]["data"]:
                    if len(previousEvent["values"]["data"]["text"]) > max_length:
                        input = previousEvent
                        input_text = previousEvent["values"]["data"]["text"]
                        max_length = len(previousEvent["values"]["data"]["text"])
                if "values" in previousEvent and "data" in previousEvent["values"] and "text" in previousEvent["values"]["data"]:
                    logs.append(previousEvent)
        cast['logs'] = logsModificados
        logsModificados = []
        anonymizations_col.insert_one(cast) 
    print("Anonimización completada para todos los screencasts")

# Ejecutar el script
execute()