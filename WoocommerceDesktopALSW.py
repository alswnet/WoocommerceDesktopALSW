#!/usr/bin/env python

from appJar import gui
from woocommerce import API
import simplejson as json
import barcode
from xhtml2pdf import pisa

wcapi = API(
    url="http://tienda.alsw.net",
    consumer_key="ck_55ab20bcb15ba99296c43b1dcaadfb4ad42728d2",
    consumer_secret="cs_4a8aa6fb2d5b7595f0b3cf08ab62562bf1ba745b",
    wp_api=True, # Enable the WP REST API integration
    version="wc/v1" # WooCommerce WP REST API version
)
# top slice - CREATE the GUI
app = gui()
SID = 0

BARCODE = barcode.get_barcode_class('code39')


app.startTabbedFrame("Cuadros")
app.setTabbedFrameTabExpand("Cuadros", expand=True)
app.startTab("Actualizar")


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
	elif btn == "Buscar":
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
	elif btn == "Crear":
		app.infoBox("Casi","Creando ")
	else:
		app.infoBox("Error","Aun No impletado")

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

app.stopTab()

app.startTab("Barcode")
app.addLabel("l2", "Tab 2 Label")
app.addLabel("title2", "Generador Barcode", 0, 0, 2)  
app.addLabel("Categoria", "Categoria:", 1, 0)           
app.addEntry("Categoria", 1, 1)    
app.addButton("Crear",press,6,0,3)                    
app.addButton("salir2",press,7,0,3)


app.stopTab()

app.startTab("Tab3")
app.addLabel("l3", "Aun no :p ")
app.stopTab()

app.stopTabbedFrame()

app.go()
