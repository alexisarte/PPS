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

def obtener_nombre_ficticio_con_espacios(texto):
    palabras = texto.split()  # Dividir por espacios
    palabras_ficticias = []
    for palabra in palabras:
        palabra_ficticia = ''.join(random.choices(string.ascii_letters, k=len(palabra)))
        palabras_ficticias.append(palabra_ficticia)
    return ' '.join(palabras_ficticias)  # Reconstruir el texto con los espacios originales

def execute():
    # Conectar a la base de datos
    client = MongoClient("mongodb://localhost:27017")
    db = client["micrometrics"]
    collection = db["screencastswithevents"]

    # Pipeline de agregación para todos los screencasts
    pipeline = []

    # Ejecutar el pipeline y procesar todos los screencasts
    anonymizations_col = db["anonymizations"]
    anonymizations_col.drop()  # Limpiar la colección temporal

    screencasts = list(collection.aggregate(pipeline, allowDiskUse=True))

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
            borrados = []
            error_positions = []
            if previousEvent.get("type"):
                if input is not None:
                    if es_nombre(input_text):
                        print(f"El texto '{input_text}' es un nombre.")
                        # ver si hubo errores mientras se escribia el nombre, es decir recorres los subinputs y ver si se borró un caracter y se modifico
                        # previousLogs = logs.copy()
                        # nextLogs = logs.copy()
                        # previousLogs.pop()
                        # nextLogs.pop(0)
                        # for previousLog, nextLog in zip(previousLogs, nextLogs):
                        #     if len(previousLog["values"]["data"]["text"]) > len(nextLog["values"]["data"]["text"]):
                        #         borrados.append()

                        nombre_ficticio = obtener_nombre_ficticio_con_espacios(input_text)
                        input["values"]["data"]["text"] = nombre_ficticio
                        print(f"El nombre '{input_text}' ha sido anonimizado como '{nombre_ficticio}'.")
                        logsModificados.append(input)
                    if input_text.isdigit():
                        primera_parte = input_text[0:int((len(input_text) / 2))]
                        segunda_parte = "".join(["*" for _ in input_text[int(len(input_text) / 2):]])
                        if "values" in input:
                            input["values"]["data"]["text"] = primera_parte + segunda_parte
                        for log in logs:
                            log_text = log["values"]["data"]["text"]
                            if log_text.isdigit():
                                start_index = input_text.find(log_text)
                                if start_index != -1:
                                    end_index = start_index + len(log_text)
                                    log["values"]["data"]["text"] = input["values"]["data"]["text"][start_index:end_index]
                            logsModificados.append(log)
                        obj = {
                            "type": "inputEnd",
                            "timestamp": input["values"]["timestamp"] + 1
                        }
                        logsModificados.append(obj)
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
