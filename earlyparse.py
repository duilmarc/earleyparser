class Produccion(object):
	def __init__(self, *terminos):
		self.terminos= terminos
	def __len__(self):
		return len(self.terminos)
	def __getitem__(self,index):
		return self.terminos[index]
	def __iter__(self):
		return iter(self .terminos)
	def __repr__(self):
		return " ".join(str(t) for t in self.terminos)
	def __eq__(self,otro):
		if not isinstance(otro,Produccion):
			return False
		return self.terminos == otro.terminos
	def __ne__(self,otro):
		return not( self==otro )
	def __hash__(self):
		return hash(self.terminos)

class Regla(object):
	def __init__(self, nombre, *producciones):
		self.nombre=nombre
		self.producciones= list(producciones)
	def __str__(self):
		return self.nombre
	def __repr__(self):
		return "%s -> %s" % (self.nombre," | ".join(repr(p) for p in self.producciones))
	def agregar(self, *producciones):
		self.producciones.extend(producciones)
		
		
class Estado(object):
	def __init__(self, nombre,produccion,punto_indice,columna_de_inicio):
		self.nombre=nombre
		self.produccion=produccion
		self.columna_de_inicio=columna_de_inicio
		self.fin_de_columna= None
		self.punto_indice=punto_indice
		self.reglas = [t for t in produccion if isinstance(t,Regla)]

	def __repr__(self):
		terminos= [str(p) for p in self.produccion]
		terminos.insert(self.punto_indice,u".")
		return "%-5s --> %-16s [%s-%s]" % (self.nombre," ".join(terminos), self.columna_de_inicio, self.fin_de_columna)

	def __eq__(self,otro):
		return (self.nombre, self.produccion,self.punto_indice,self.columna_de_inicio) == \
			(otro.nombre, otro.produccion, otro.punto_indice, otro.columna_de_inicio)

	def __ne__(self,otro):
		return not (self == otro)

	def __hash__(self):
		return hash((self.nombre,self.produccion))

	def esta_completado(self):
		return self.punto_indice >= len(self.produccion)

	def siguiente_termino(self):
		if self.esta_completado():
			return None
		return self.produccion[self.punto_indice]

class Columna(object):
	def __init__(self, indice,token):
		self.indice=indice
		self.token=token
		self.estados=[]
		self._unique= set()
	def __str__(self):
		return str(self.indice)
	def __len__(self):
		return len(self.estados)
	def __iter__(self):
		return iter(self.estados)
	def __getitem__(self,index):
		return self.estados[indice]
	def enumerardesde(self,indice):
		for i in range(indice, len(self.estados)):
			yield i, self.estados[i]
	def agregar(self,estado):
		if estado not in self._unique:
			self._unique.add(estado)
			estado.fin_de_columna= self
			self.estados.append(estado)
			return True
		return False

	def imprimir(self,completado_solo= False):
		print "[%s] %r" % (self.indice, self.token)
		print "=" * 35
		for s in self.estados:
			if completado_solo and not s.esta_completado():
				continue
			print repr(s)
		print

class Nodo(object)
	def __init__(self, valor, hijos):
		self.valor= valor
		self.hijos = hijos
	def imprimir(self, nivel = 0):
		print "  " * nivel + str(self.valor)
		for hijo in self.hijos:
			hijo.imprimir(nivel + 1)

def predecir(columna, regla ):
	for produccion in regla.producciones:
		columna.agregar(Estado(regla.nombre, produccion, 0 , columna))

def escanear(columna, estado, token):
	if token != columna.token:
		return 
	columna.agregar(Estado(estado.nombre, estado.produccion, estado.punto_indice + 1, estado.columna_de_inicio))

def completar(columna, estado ):
	if not estado.esta_completado():
		return 
	for st in estado.columna_de_inicio:
		termino= st.siguiente_termino()
		if not isinstance(termino,Regla):
			continue
		if termino.nombre == estado.nombre:
			columna.agregar(Estado(st.nombre,st.produccion,st.punto_indice+1 ,st.columna_de_inicio))

GAMMA_Regla = u"Gramatica"

def parseador(regla, texto):
	tabla = [Columna(i,tok) for i,tok in enumerate([None]+ texto.lower().split())]
	tabla[0].agregar(Estado(GAMMA_Regla,Produccion(regla),0,tabla[0]))

	for i,columna in enumerate(tabla):
		for estado in columna:
			if estado.esta_completado():
				completar(columna,estado)
			else:
				termino = estado.siguiente_termino()
				if isinstance(termino,Regla):
					predecir(columna,termino)
				elif i+1 < len(tabla):
					escanear(tabla[i+1],estado, termino)
    

	for st in tabla[-1]:
		if st.nombre == GAMMA_Regla and st.esta_completado():
			return st
 	else:
 		raise ValueError("no esta en la gramatica")

def construir_arbol(estado):
	return contruir_arbole_ayuda([],estado, len(estado.reglas)-1 ,estado.fin_de_columna)

def contruir_arbole_ayuda(hijos, estado, indice_regla, fin_columna):
	if indice_regla < 0 :
		return [Nodo(estado,hijos)]
	elif indice_regla == 0:
		inicio_columna= estado.columna_de_inicio
	else:
		inicio_columna= None

	regla = estado.reglas[indice_regla]
	salidas= []
	for st in fin_columna:
		if st is estado:
			break
		if st is estado or not st.esta_completado() or st.nombre != regla.nombre:
			continue
		if inicio_columna is not None and st.columna_de_inicio != inicio_columna:
			continue
		for sub_arbol in construir_arbol(st):
			for nodo in contruir_arbole_ayuda([sub_arbol]+hijos,estado, indice_regla -1, st.columna_de_inicio):
				salidas.append(nodo)
	return salidas

#sustantivo
SV = Regla("SV", Produccion("cine"), Produccion("peliculas"), Produccion("ninio"),
	    Produccion("personas"), Produccion("pera"), Produccion("fruta"), Produccion("pack"))
#articulo
AT = Regla("AT", Produccion("el"), Produccion("la"), Produccion("unas"))
#verbo
V = Regla("V", Produccion("vio"), Produccion("comieron"), Produccion("camino"), Produccion("jugo"), Produccion("pasa"))
#pre
Prp = Regla("Prp", Produccion("con"), Produccion("en"), Produccion("al"))
#Conjun
Cj = Regla("cj")
#Sujeto
St = Regla("St", Produccion(AT, SV),  Produccion("gavi"), Produccion("pedro"), Produccion("andre"), Produccion("rufian"))
St.agregar(Produccion(St, Cj))
Cj.agregar(Produccion(SV, St))
 
#Predicado
Pr = Regla("VP", Produccion(V, St))
Pr.agregar(Produccion(Pr, Cj))
O = Regla("O", Produccion(St, Pr), Produccion(Pr))

for arbol in construir_arbol(parseador(O, "rufian pasa el pack")):
    print "--------------------------"
    arbol.imprimir()

