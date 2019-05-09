import requests
import json
import datetime
import time
import argparse
import jsonpickle
from dateutil.relativedelta import relativedelta


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

parser = argparse.ArgumentParser()
parser.add_argument("-m","--Mes",  type=str, help="Número del mes, por defecto toma mes actual + 1",default=0)
parser.add_argument("-if","--IataFrom",  type=str, help="Iata Desde, default BUE",default="BUE")
parser.add_argument("-it","--IataTo",  type=str, help="Iata hasta, default MIA",default="MIA")
parser.add_argument("-n","--Numero",  type=int, help="Numero de página, default 1",default=0)
args = parser.parse_args()
def executeScrap( ):
    lista = list()
    paramMes = str(datetime.datetime.now().month+1)
    if int(args.Mes)<13 and int(args.Mes)>0:
        paramMes=args.Mes

    iataFrom = args.IataFrom
    iataTo = args.IataTo
    
    pageSize = 100
    fechaInicio=datetime.date(datetime.datetime.today().year,int(paramMes),1)
    fechaFin=fechaInicio + relativedelta(months=+12)
    fechaActual=fechaInicio
    while fechaActual<=fechaFin:
        pageNum = args.Numero
        numeroMes=str(fechaActual.month)
        url = "https://almundo.com.ar/flights/offers/api/offers?months="+numeroMes + \
            "&from="+iataFrom+"&to="+iataTo+"&page=" + \
            str(pageNum)+"&size="+str(pageSize)
        firstReq = requests.get(url)
        print(url)
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
        fechaActual=fechaActual + relativedelta(months=+1)
    json_string = jsonpickle.encode(lista, unpicklable=False)
    with open("Resultado mes"+numeroMes+" "+iataFrom+"-"+iataTo+".json", "w") as arch:
        arch.write(json_string)

if __name__ == '__main__':
	executeScrap()