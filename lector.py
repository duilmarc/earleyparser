
class Grammar:

    def __init__(self, produccion):
        self.producciones=produccion


class Produccion:
    def __init__(self,lexema,lenma,clase_gramatical)
        self.clase_gramatical=clase_gramatical

    def motrar_producciones():
        print("< "+lexema+" , "+lenma+" , "+clase_gramatical+" >")


class lenma:
    def __init__(self,conjunto_lexema,lenma)
        self.conjunto_lexema[]=conjunto_lexema
        self.nombre=lenma

    def añadir(lexema):
        conjunto_lexema=conjunto_lexema.append(lexema)

    def imprimir():
        print(self.nombre+" : ")
        for i in conjunto_de_lenma
            print(i+", ")
    def buscar(lexema):
        for i in conjunto_lexema:
            if(i==lexema):
                return 1
            else:
                return 0

class clase_gramatical:
    def __init__(self,conjunto_de_lenma,clase_gramatical)
        self.conjunto_de_lenma=conjunto_de_lenma
        self.nombre=clase_gramatical

    def añadir(lenma):
        conjunto_de_lenma=conjunto_de_lenma.append(lexema)
    
    def imprimir():
        print(self.nombre+" : ")
        for i in conjunto_de_lenma
            print(i+", ")

    def buscar(lexema):
        for i in conjunto_lenma:
            if(i==lexema):
                return 1
            else:
                return 0


def early_parser(gramatica,oracion)
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
                                print (str(contadorA)+')'+palabra)
                        if(comparar_verbos(palabra)):
                                contadorV+=1
                                print (str(contadorV)+')'palabra)
                        if(comparar_sustantivos(palabra)):
                                contadorS+=1
                                print (str(contadorS)+')'+palabra)

#leerarticu()

def leeroracion():

        oracion="me lleva que valga verga todo"
        for i in oracion.split(' '):
                if(comparar_verbos(i-1)&comparar_verbos(i+1)&(i=='que')):
                        print ('nicolas se la come')
                else:
                        print ('nicolas se la sigue comiendo')



leeroracion()
