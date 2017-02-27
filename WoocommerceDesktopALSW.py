#!/usr/bin/env python

from appJar import gui
from woocommerce import API
import simplejson as json

wcapi = API(
    url="http://tienda.alsw.net",
    consumer_key="ck_xxxx",
    consumer_secret="cs_xxxx",
    wp_api=True, # Enable the WP REST API integration
    version="wc/v1" # WooCommerce WP REST API version
)
# top slice - CREATE the GUI
app = gui()
SID = 0
# function called by pressing the buttons
def press(btn):
    if btn=="salir":
        app.stop()
    elif btn == "Actualizar":
		try:
			Numero =  int(app.getEntry('ncantidad'))
			data = {
				"stock_quantity": Numero
			} 
			global SID
			app.setLabel("Cantidad","")
			palabra = "products/" + str(SID)
			r = wcapi.put(palabra,data).json()
			#print(r)
			app.setLabel("Cantidad",app.getEntry('ncantidad'))
		except:
			app.infoBox("Error", "Ingrese cantidad numero")
    else:
		try:
			if app.getEntry('sku') != "":
				app.setLabel("ID","")
				app.setLabel("precio","")
				app.setLabel("Cantidad","")
				palabra = 'products/?sku='+app.getEntry('sku')
				r = wcapi.get(palabra).json()
				SID = r[0]['id']
				##print(r)
				app.setLabel("ID","ID: " + str(r[0]['id']))
				app.setLabel("Nombre","Nombre: " + r[0]['name'])
				app.setLabel("precio","Precio: " + str(r[0]['regular_price']))
				app.setLabel("Cantidad","Cantidad: " + str(r[0]['stock_quantity']))
			else:
				app.infoBox("Error", "Ingrese SKU")
		except:
			app.infoBox("Error", "SKU incotecto")
		

app.setFont(25)
app.addLabel("title", "ALSW Actualizar", 0, 0, 2)  
app.addLabel("sku", "SKU:", 1, 0)           
app.addEntry("sku", 1, 1)                        
app.addLabel("ncantidad", "Nueva Cantidad:", 2, 0)             
app.addEntry("ncantidad", 2, 1)                          
app.addLabel("ID","-", 3 , 0 )
app.addLabel("Nombre","-", 3 , 1 )
app.addLabel("precio","-", 4 , 0 )
app.addLabel("Cantidad","-", 4 , 1 )
app.addButtons(["Buscar", "Actualizar"], press, 6, 0, 2) 
app.addButton("salir",press,7,0,3)


app.setEntryFocus("sku")
# bottom slice - START the GUI

app.go()
