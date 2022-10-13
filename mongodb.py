import json
from pymongo import MongoClient
import datetime
from flask import Flask, request, render_template
import datetime
client = MongoClient("mongodb://192.168.0.21:27000")
database = client.musicas
#mongodb://192.168.0.21:27000
print(client)


def insert_to_collection(clientdatabasecollection, json): #FUNCIONANDO

    clientdatabasecollection.insert_many(json)
    return "Created!"


def return_created_collections(database): #FUNCIONANDO

    collections = database.list_collection_names()
    result = ""

    for item in database.playlist.find({}):
      result += str(item)


    return collections, result


def check_collections_name(collection_name, database): #FUNCIONANDO

    global client
    collection_list = return_created_collections(database)

    if collection_name in collection_list:
        return "The collection exists."


def return_created_databases(): #FUNCIONANDO
    global client

    databases = client.list_database_names()
    return databases


def check_database_name(dbname): #FUNCIONANDO

    global client
    dblist = return_created_databases()

    if dbname in dblist:
        return "The database exists."

app = Flask(__name__)
@app.route('/', methods=["GET"])
def main():
    global database

    resultadodel = None
    resultadoalt = None

    collection = database.playlist #request.args.get('collection')
    musica = request.args.get('musica')
    bandaoucantor = request.args.get('bandaoucantor')
    ano = request.args.get('ano')
    categoria = request.args.get('categoria')
    listardatabases = request.args.get('listardatabases')
    listarcontainers = request.args.get('listarcontainers')



    altmusica = request.args.get('altmusica')
    altbandaoucantor = request.args.get('altbandaoucantor')
    altano = request.args.get('altano')
    altcategoria = request.args.get('altcategoria')

    altnovomusica = request.args.get('altnovomusica')
    altnovobandaoucantor = request.args.get('altnovobandaoucantor')
    altnovoano = request.args.get('altnovoano')
    altnovocategoria = request.args.get('altnovocategoria')


    delmusica = request.args.get('delmusica')
    delbandaoucantor = request.args.get('delbandaoucantor')
    delano = request.args.get('delano')
    delcategoria = request.args.get('delcategoria')

    altlist = [altmusica, altbandaoucantor, altano, altcategoria]
    dellist = [delmusica, delbandaoucantor, delano, delcategoria]


    altdict = {altmusica: "nome", altbandaoucantor: "bandaoucantor", altano: "ano", altcategoria: "categorias"}
    altnovodict = {altmusica: altnovomusica, altbandaoucantor: altnovobandaoucantor, altano: altnovoano, altcategoria: altnovocategoria}
    deldict = {delmusica: "nome", delbandaoucantor: "bandaoucantor", delano: "ano", delcategoria: "categorias"}

    for alt in altlist:

      if alt:

        collection.update_many({altdict[alt]: alt}, {'$set': {altdict[alt]: altnovodict[alt]}})
        print(altdict[alt], alt, altdict[alt], altnovodict[alt])
        resultadoalt = "Dados foram alterados"

    if resultadoalt:

        return render_template('index.html', resultadoalt = "Dados foram alterados")

    for delete in dellist:

      if delete:
        
        collection.delete_one({deldict[delete]: delete})
        resultadodel = "Dados foram deletados"

    if resultadodel:

        return render_template('index.html', resultadodel = "Dados foram deletados")

    json_content = [{
                  "nome": f"{musica}",
                  "bandaoucantor": f"{bandaoucantor}",
                  "ano": f"{ano}",
                  "categorias": f"{categoria}",
                  "registro": datetime.datetime.now()
                }]

    if musica and bandaoucantor and ano and categoria:

      print(insert_to_collection(collection, json_content))

    elif listardatabases:

        dbs = return_created_databases()
        return render_template('index.html', resultadodatabases=dbs, databaseslistados=dbs)

    elif listarcontainers:

        containers = return_created_collections(database)
        return render_template('index.html', resultadocontainers=containers, containerslistados=containers)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True, port='5001') 




"""
print(collection.find_one())
for musica_id in range(collection.estimated_document_count()+1):
        print(collection.find_one({"_id": musica_id}))
collection.delete_one({"_id": 1})
collection.delete_many()
collection.delete_many({"banda": "Iron Man"}) 
collection.update_one({'_id': 2}, {'$set': {'nome':'Powerslave'}}) 
collection.update_many({'banda': 'Iron Maiden'}, {'$set': {'banda':'Metallica'}})




"""