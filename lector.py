

def comparar_articulos(palabra):
 	if(palabra=="la" or palabra=="el" or palabra == "las" or palabra == "los" or palabra =="lo" or palabra == "un" or palabra == "unos" or palabra == "una" or palabra == "unas"):
 		return 1
 	else :
 		return 0
def diccionario(palabra):
	f=o

def leerarticu():
	contador=0
	f= open("libro","r")
	informacion = f.readlines()
 	f.close()
	for linea in informacion:
		for palabra in linea.split(' '):
			if(comparar_articulos(palabra)):
				contador+=1
				print '%s) %s'%(str(contador),palabra)

			
		


leerarticu()