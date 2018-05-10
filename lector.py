

def comparar_articulos(palabra):
        for i in articulos:
             if(i==palabra):
                     return 1

        return 0
def comparar_verbos(palabra):
        for i in verbos:
             if(i==palabra):
                     return 1
        return 0
def comparar_sustantivos(palabra):
        for i in sustantivos:
                if(i==palabra):
                        return 1
        return 0

def diccionario(palabra):
        f=o

def leerarticu():
        contadorA=0
        contadorV=0
        contadorS=0
        f= open("libro","r")
        informacion = f.readlines()
        f.close()
        for linea in informacion:
                for palabra in linea.split(' '):
                        if(comparar_articulos(palabra)):
                                contadorA+=1
                                print (str(contadorA),palabra)
                        if(comparar_verbos(palabra)):
                                contadorV+=1
                                print (str(contadorV),palabra)
                        if(comparar_sustantivos(palabra)):
                                contadorS+=1
                                print (str(contadorS),palabra)

leerarticu()
