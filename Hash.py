class map:
    def __init__(self):
        self.tamano = 11
        self.ranuras = [None] * self.tamano
        self.datos = [None] * self.tamano
        
    def funcionHash(self,clave,tamano):
        return clave%self.tamano
    
    def rehash(self,hashViejo,tamano):
        return (hashViejo+1)%tamano
    
    def agregar(self,clave,dato):
        valorHash = self.funcionHash(clave,len(self.ranuras))
        if self.ranuras[valorHash] == None:
            self.ranuras[valorHash] = clave
            self.datos[valorHash] = dato
        else:
            if self.ranuras[valorHash] == clave:
                self.datos[valorHash] = dato  #reemplazo
            else:
                proximaRanura = self.rehash(valorHash,len(self.ranuras))
                while self.ranuras[proximaRanura] != None and self.ranuras[proximaRanura] != clave:
                    proximaRanura = self.rehash(proximaRanura,len(self.ranuras))
                if self.ranuras[proximaRanura] == None:
                    self.ranuras[proximaRanura]=clave
                    self.datos[proximaRanura]=dato
                else:
                    self.datos[proximaRanura] = dato #reemplazo

		
    def obtener(self,clave):
        ranuraInicio = self.funcionHash(clave,len(self.ranuras))
        dato = None
        parar = False
        encontrado = False
        posicion = ranuraInicio
        while self.ranuras[posicion] != None and not encontrado and not parar:
            if self.ranuras[posicion] == clave:
                encontrado = True
                dato = self.datos[posicion]
            else:
                posicion=self.rehash(posicion,len(self.ranuras))
            if posicion == ranuraInicio:
                parar = True
        return dato

    def __getitem__(self,clave):
        return self.obtener(clave)

    def __setitem__(self,clave,dato):
        self.agregar(clave,dato)

class Hash:
    def __init__(self):
        self.tamano=4
        self.tamano2=3
        self.ha=[None]*self.tamano
        for i in range(self.tamano):
            self.ha[i]=[None]*self.tamano2

    def pri(self):
        print(self.ha)

    def funHash(self,clave,tamano):
        return clave%self.tamano

    def agregar(self,clave,dato):
        posi=0
        valorHash = self.funHash(clave,self.tamano)
        if self.ha[valorHash][posi] == None:
            self.ha[valorHash][posi] = dato
        else:
            posi=+1
            while self.ha[valorHash][posi]!=None and posi<self.tamano2:
                posi=+1
            self.ha[valorHash][posi]=dato

   

h=Hash()
h.agregar(15,"perro")
h.agregar(20,"gato")
h.agregar(13,"correr")
h.agregar(14,"nana")
h.agregar(100,"gallo")
h.pri()



















            
