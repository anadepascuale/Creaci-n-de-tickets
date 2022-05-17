#!/usr/bin/env python

"""panda.py: Lee datos de un csv, carga tickets y guarda los id de ticket asociados 
a cada línea. En caso de que la fila ya tenga un ticket no vuelve a solicitarlo"""

__author__      = "Javier Jorge"
__copyright__   = "Copyright 2009, Planet Earth"
__license__ = "GPL"
__version__ = "0.0.0"
__maintainer__ = "Javier Jorge"
__email__ = "jjorge@unc.edu.ar"
__status__ = "test"

"Modificaciones para su uso, por parte de Ana Julieta De Pascuale, mail : ana.de.pascuale@mi.unc.edu.ar, github/anadepascuale"

import pandas as pd
import urllib.parse
import requests
import json

df = pd.read_csv(
    "Rtas de forms x UA - FCEFyN.csv",
    #dtype={"nombre" : str,"email": str,"telefono": str,"ticketAsginado": str}
    dtype={"Marca temporal" : str,"Dirección de correo electrónico" : str,"Apellido/s": str,"Nombre/s": str,"Teléfono de contacto ": str,"Legajo": str,"Tipo de computadora": str,"El equipo está actualmente en funcionamiento ": str,"Marca": str,"Modelo": str,"Año estimado de compra": str,"¿Cuánta memoria RAM tiene ?": str,"¿De qué tamaño es el disco rígido?": str,"¿Tiene webcam funcionando?": str,"¿Tiene kit auricular/micrófono?": str,"Foto": str,"Estoy de acuerdo con todas las reglas": str,"Aclaraciones o Comentarios": str,"Recepción de la computadora": str,"TICKET ASOCIADO": str,"Entregado": str},
    encoding= 'utf-8'
    )

for index, row in df.iterrows():
    #print(index,row)
    
    try:
        print(df['TICKET ASOCIADO'][index]) 
        if(pd.isna(df['TICKET ASOCIADO'][index])): 
            # Verifica si la celda está vacía : isna
            jsonticketrow = {'autorespond':"false", 'source': "API", 'name': str(row["Apellido/s"]).upper()+" "+ str(row["Nombre/s"]), 'email':str(row["Dirección de correo electrónico"]), "phone":str(row["Teléfono de contacto"]),'subject':str (df["Marca temporal"][0])+" "+str (row["Marca"])+" "+str(row["Modelo"])+" "+str(row["Año estimado de compra"]), 'message': str(row["Marca"])+" "+str(row["Modelo"])+" "+ str(row["Año estimado de compra"])+" "+ str(row["¿Cuánta memoria RAM tiene ?"])+"/"+ str(row["Que tipo de disco tiene su equipo?"])+" "+str(row["Aclaraciones o Comentarios"])+" webcam: "+str(row["¿Tiene webcam funcionando?"])+" auris: "+str(row["¿Tiene kit auricular/micrófono?"])}
            print(json.dumps(jsonticketrow))
            resp = requests.post("https://tickets.ram.unc.edu.ar//api/tickets.json", data=json.dumps(jsonticketrow), headers={"X-API-Key":"87CA97F4F8A10467BA0BCFEE5C7AF4D2"})
            print(resp.text)
            df['TICKET ASOCIADO'][index]=resp.text
    except Exception as inst:
        print(inst)
        df['TICKET ASOCIADO'][index]="error"
    print(df['TICKET ASOCIADO'][index])

    

df.to_csv("Rtas de forms x UA - FCEFyN.csv", index=False)