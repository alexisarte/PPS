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

def obtener_input_anonimizado_con_espacios(texto):
    palabras = texto.split()  # Dividir por espacios
    palabras_ficticias = []
    for palabra in palabras:
        palabra_ficticia = ''.join(random.choices(string.ascii_letters, k=len(palabra)))
        palabras_ficticias.append(palabra_ficticia)
    return ' '.join(palabras_ficticias)  # Reconstruir el texto con los espacios originales

def anonimizar_subinputs(logs, input, input_text, input_anonimizado, logsModificados):
    errors = []
    for log in logs:
        start_index = 0
        end_index = len(log["values"]["data"]["text"])
        # Convertir la cadena en una lista para modificar por índice
        log_text_lista = list(log["values"]["data"]["text"])
        input_text_lista = list(input_text)
        # Reemplazar las posiciones en las que difiere el caracter de log comparado al subinput correspondiente
        for i in range(min(len(log_text_lista), len(input_text_lista))):  # Iterar hasta el mínimo de los dos
            if log_text_lista[i] != input_text_lista[i]:
                print(f"Error en la posición {i}: {log_text_lista[i]} != {input_text_lista[i]}")
                errors.append(i)
        # Convertir la lista de nuevo en una cadena
        sub_input_anonimizado = input_anonimizado[start_index:end_index]
        log["values"]["data"]["text"] = reemplazar_errores_con_michis(sub_input_anonimizado, errors)
        logsModificados.append(log)
    obj = {
        "type": "inputEnd",
        "timestamp": input["values"]["timestamp"] + 1
    }
    logsModificados.append(obj)

def reemplazar_errores_con_michis(texto, posiciones_errores):
    texto_lista = list(texto)  # Convertir a lista para modificar por índice
    for pos in posiciones_errores:
        if pos < len(texto_lista):
            texto_lista[pos] = '#'
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

        for previousEvent, nextEvent in zip(previous, next):
            if previousEvent.get("type") == "inputEnd":
                print(f"previousEvent: {previousEvent['type']}")
                if input is not None:
                    if es_nombre(input_text):
                        print(f"El texto '{input_text}' es un nombre.")
                        input_anonimizado = obtener_input_anonimizado_con_espacios(input_text)
                        anonimizar_subinputs(logs, input, input_text, input_anonimizado, logsModificados)
                        print(f"El nombre '{input_text}' ha sido anonimizado como '{input_anonimizado}'.")
                    elif input_text.isdigit():
                        primera_parte = input_text[0:int((len(input_text) / 2))]
                        segunda_parte = "".join(["*" for _ in input_text[int(len(input_text) / 2):]])
                        input_anonimizado = primera_parte + segunda_parte
                        anonimizar_subinputs(logs, input, input_text, input_anonimizado, logsModificados)

                input = nextEvent
                max_length = len(nextEvent["values"]["data"]["text"])
                input_text = nextEvent["values"]["data"]["text"]
                logs = []

            else:
                if len(previousEvent["values"]["data"]["text"]) >= max_length:
                    input = previousEvent
                    input_text = previousEvent["values"]["data"]["text"]
                    max_length = len(previousEvent["values"]["data"]["text"])
                logs.append(previousEvent)

        cast['logs'] = logsModificados
        logsModificados = []

        anonymizations_col.insert_one(cast) 

    print("Anonimización completada para todos los screencasts")

# Ejecutar el script
execute()
