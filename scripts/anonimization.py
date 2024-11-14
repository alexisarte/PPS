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

def anonimizar_subinputs(logs, input, input_text, logsModificados):
    for log in logs:
        log_text = log["values"]["data"]["text"]
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

def reemplazar_errores_con_asteriscos(texto, posiciones_errores):
    texto_lista = list(texto)  # Convertir a lista para modificar por índice
    for pos in posiciones_errores:
        if pos < len(texto_lista):
            texto_lista[pos] = '*'
    return ''.join(texto_lista)

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
        error_positions = []  # Lista para almacenar posiciones de errores

        for previousEvent, nextEvent in zip(previous, next):
            if previousEvent.get("type"):
                if input is not None:
                    if es_nombre(input_text):
                        print(f"El texto '{input_text}' es un nombre.")
                        nombre_ficticio = obtener_nombre_ficticio_con_espacios(input_text)
                        input["values"]["data"]["text"] = nombre_ficticio
                        input["values"]["data"]["text"] = reemplazar_errores_con_asteriscos(input["values"]["data"]["text"], error_positions)
                        print(f"El nombre '{input_text}' ha sido anonimizado como '{input["values"]["data"]["text"]}'.")
                        error_positions = []  # Resetear posiciones de errores
                        anonimizar_subinputs(logs, input, input_text, logsModificados)
                    # elif input_text.isdigit():
                    #     primera_parte = input_text[0:int((len(input_text) / 2))]
                    #     segunda_parte = "".join(["*" for _ in input_text[int(len(input_text) / 2):]])
                    #     if "values" in input:
                    #         input["values"]["data"]["text"] = primera_parte + segunda_parte
                    #     anonimizar_subinputs(logs, input, input_text, logsModificados)

                    # Reemplazar caracteres en las posiciones de errores con asteriscos

                input = nextEvent

                if "values" in nextEvent and "data" in nextEvent["values"] and "text" in nextEvent["values"]["data"]:
                    max_length = len(nextEvent["values"]["data"]["text"])
                logs = []

            else:
                print("previousEvent", previousEvent["values"]["data"]["text"])
                if "values" in previousEvent and "data" in previousEvent["values"] and "text" in previousEvent["values"]["data"]:
                    if len(previousEvent["values"]["data"]["text"]) > max_length:
                        input = previousEvent
                        input_text = previousEvent["values"]["data"]["text"]
                        max_length = len(previousEvent["values"]["data"]["text"])

                    # Detectar errores en la escritura y agregar posición
                    if "values" in nextEvent and "data" in nextEvent["values"] and "text" in nextEvent["values"]["data"]:
                        if (len(previousEvent["values"]["data"]["text"]) > len(nextEvent["values"]["data"]["text"])):
                            error_positions.append(len(previousEvent["values"]["data"]["text"]) - 1)

                if "values" in previousEvent and "data" in previousEvent["values"] and "text" in previousEvent["values"]["data"]:
                    logs.append(previousEvent)

        cast['logs'] = logsModificados
        logsModificados = []

        anonymizations_col.insert_one(cast) 

    print("Anonimización completada para todos los screencasts")

# Ejecutar el script
execute()
