import requests
import json
import datetime
import time
import jsonpickle
# {"precioNeto":"25190.20","origen":{"iata":"BUE","nombre":"Buenos Aires - Argentina"},
# "destino":{"iata":"MIA","nombre":"Miami - Estados Unidos"},
# "dateD":"17-05-2019","dateR":"27-05-2019","cantDias":"10","aerolinea":"AM","airname":"Aerom\u00e9xico","precio":"25190.20"}
# https://almundo.com.ar/flights/offers/api/offers?months=5&from=BUE&to=MIA&page=2&size=100


class Lugares (object):

    def __init__(self, iata="Null", nombre="Null"):
        self.iata = iata
        self.nombre = nombre


class Datos (object):

    def __init__(self, precioNeto="Null", origen="Null", destino="Null", dateD="Null", dateR="Null", cantDias="Null", aerolinea="Null", airname="Null", precio="Null"):
        self.precioNeto = precioNeto
        self.origen = Lugares()
        self.destino = Lugares()
        self.dateD = dateD
        self.dateR = dateR
        self.cantDias = cantDias
        self.aerolinea = aerolinea
        self.airname = airname
        self.precio = precio


lista = list()

numeroMes = str(datetime.datetime.now().month+1)
iataFrom = "BUE"
iataTo = "MIA"
pageNum = 1
pageSize = 100
url = "https://almundo.com.ar/flights/offers/api/offers?months="+numeroMes + \
    "&from="+iataFrom+"&to="+iataTo+"&page=" + \
    str(pageNum)+"&size="+str(pageSize)
firstReq = requests.get(url)
print(firstReq)
y = firstReq.json()
for offer in y["offers"]:
    ingreso = Datos()
    ingreso.origen = Lugares(str(offer["from"]),str(offer["from_city_name"]+" - "+offer["from_country_name"]))
    ingreso.destino = Lugares(str(offer["to"]),str(offer["to_city_name"]+" - "+offer["to_country_name"]))
    ingreso.precioNeto = offer["total_price"]
    ingreso.dateD = offer["departure"]
    ingreso.dateR = offer["returning"]
    ingreso.cantDias = offer["stay_duration"]
    ingreso.aerolinea = offer["airline"]
    ingreso.airname = offer["airline_name"]
    ingreso.precio = offer["total_price"]
    lista.append(ingreso)
total = y["pagination"]["total"]
totalRestante = total-int(pageSize)
maxPage = total/int(pageSize)
pageNum = pageNum+1

while pageNum <= maxPage:
    requrl = "https://almundo.com.ar/flights/offers/api/offers?months="+numeroMes + "&from="+iataFrom+"&to="+iataTo+"&page="+str(pageNum)+"&size="+str(pageSize)
    print(requrl)
    req = requests.get(requrl)
    for offer in req.json()["offers"]:
        ingreso = Datos()
        ingreso.origen = Lugares(offer["from"],offer["from_city_name"]+" - "+offer["from_country_name"])
        ingreso.destino = Lugares(offer["to"],offer["to_city_name"]+" - "+offer["to_country_name"])

        ingreso.precioNeto = offer["total_price"]
        ingreso.dateD = offer["departure"]
        ingreso.dateR = offer["returning"]
        ingreso.cantDias = offer["stay_duration"]
        ingreso.aerolinea = offer["airline"]
        ingreso.airname = offer["airline_name"]
        ingreso.precio = offer["total_price"]
        lista.append(ingreso)
    pageNum = pageNum+1

    time.sleep(3)
json_string = jsonpickle.encode(lista, unpicklable=False)
with open("Resultado mes"+numeroMes+" "+iataFrom+"-"+iataTo+".json", "w") as arch:
    arch.write(json_string)
