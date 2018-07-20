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
        print ("[%s] %r" % (self.indice, self.token))
        print ("=" * 35)
        for s in self.estados:
            if completado_solo and not s.esta_completado():
                continue
            print (repr(s))
        print

class Nodo(object):
    def __init__(self, valor, hijos):
        self.valor= valor
        self.hijos = hijos
    def imprimir(self, nivel = 0):
        print ("  " * nivel + str(self.valor))
        for hijo in self.hijos:
            hijo.imprimir(nivel + 1)

def predict(columna, regla ):
    for produccion in regla.producciones:
        columna.agregar(Estado(regla.nombre, produccion, 0 , columna))

def scan(columna, estado, token):
    if token != columna.token:
        return 
    columna.agregar(Estado(estado.nombre, estado.produccion, estado.punto_indice + 1, estado.columna_de_inicio))

def complete(columna, estado ):
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
                complete(columna,estado)
            else:
                termino = estado.siguiente_termino()
                if isinstance(termino,Regla):
                    predict(columna,termino)
                elif i+1 < len(tabla):
                    scan(tabla[i+1],estado, termino)

    for st in tabla[-1]:
        if st.nombre == GAMMA_Regla and st.esta_completado():
            return st
    else:
        raise ValueError("no esta en la gramatica")


def construir_arbol(estado):
    return contruir_arbol_ayuda([],estado, len(estado.reglas)-1 ,estado.fin_de_columna)

def contruir_arbol_ayuda(hijos, estado, indice_regla, fin_columna):
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
            for nodo in contruir_arbol_ayuda([sub_arbol]+hijos,estado, indice_regla -1, st.columna_de_inicio):
                salidas.append(nodo)
    return salidas

#sustantivo
"""        
SV = Regla("SV", Produccion("cine"), Produccion("peliculas"), Produccion("ninio"),
        Produccion("personas"), Produccion("pera"), Produccion("fruta"), Produccion("pack"),Produccion("unidad"),Produccion("kilo"),Produccion("onza"),
           Produccion("dozena"),Produccion("lado"),Produccion("costado"),Produccion("postre"),
           Produccion("plata"),Produccion("comida"),Produccion("clase"),Produccion("tipo"),
           Produccion("receta"),Produccion("ingrediente"),Produccion("tiempo"))
#articulo
AT = Regla("AT", Produccion("el"), Produccion("la"), Produccion("unas"))
#verbo
V = Regla("V", Produccion("vio"), Produccion("comieron"), Produccion("encontrar")
          ,Produccion("camino"), Produccion("jugo"), Produccion("pasa"), Produccion("necesitar"),
          Produccion("resistir"),Produccion("hacer"),Produccion("cocinar"),Produccion("preparar"),
          Produccion("utilizar"),Produccion("aplicar"),Produccion("sugerir"),Produccion("recomendar"),
          Produccion("tener"),Produccion("poder"),Produccion("deber"),Produccion("caracterizar"),Produccion("identificar"),Produccion("inventar"),Produccion("ser"))
#adjetivo
ADJ=Regla("ADJ",Produccion("principal"),Produccion("tipico"),Produccion("cerca"),Produccion("proximo"))
#pronombres
pronombres=Regla("pronombres",Produccion("que"), Produccion("donde"), Produccion("cuanto"),Produccion("cual"),Produccion("quien"),
    Produccion("como"))
#
#pre
Prp = Regla("Prp", Produccion("con"), Produccion("en"), Produccion("al"),Produccion("de"),Produccion("para"),Produccion("por"))
#Conjun
Cj = Regla("cj")


#Sujeto
St = Regla("St", Produccion(AT, SV),  Produccion("gavi"), Produccion("pedro"), Produccion("andre"), Produccion("rufian"))
St.agregar(Produccion(St, Cj))
Cj.agregar(Produccion(SV, St))



#Predicado
Pr = Regla("VP", Produccion(V, St))
Pr.agregar(Produccion(Pr, Cj))
Scomo=Regla("scomo",Produccion (pronombres,V,St))
Squien=Regla("Squien",Produccion (pronombres,V,St))
Scual=Regla("Scual",Produccion (pronombres,V,))
O = Regla("O", Produccion(St, Pr), Produccion(Pr), Produccion(Scomo))
"""  


Vresistir = Regla("Vresistir", Produccion("resistir"),Produccion("cuesta"))
Vnecesitar = Regla("Vnecesitar", Produccion("necesitar"),Produccion("necesitan"))
Vencontrar = Regla("Vencontrar", Produccion("encontrar"))
Vproducir = Regla("Vproducir", Produccion("producir"))
Vcomprar = Regla("Vcomprar", Produccion("comprar"),Produccion("hacen"),Produccion("encuentro"),Produccion("encontrar"),Produccion("compro"),Produccion("consigo"),Produccion("preparan"))
Vtener = Regla("Vtener", Produccion("tener"))
Vutilizar = Regla("Vutilizar", Produccion("utilizar"))
Vdeber = Regla("Vdeber", Produccion("deber"), Produccion("puede"))
VerboIdentificar = Regla("VerboIdentificar",Produccion("identificar"),Produccion("caracterizar"))
Vpreparar = Regla("Vpreparar", Produccion("preparar"),Produccion("prepara"),Produccion("cocinar"),Produccion("hacer"),Produccion("hacen"),Produccion("hace"),Produccion("hornear"))
Vinventar = Regla("Vinventar", Produccion("inventar"),Produccion("inventó"),Produccion("invento"))
Vser = Regla("Vser", Produccion("ser"),Produccion("es"),Produccion("son"))
SubProcedimiento=Regla("SubProcedimiento",Produccion("procedimiento"),Produccion("forma"),Produccion("temperatura"),
        Produccion("coccion"),Produccion("manera"),Produccion("método"))
ProRel = Regla("ProRel",Produccion("que"))
AdjCerca= Regla("AdjCerca",Produccion("cerca"),Produccion("proximo"))
Adjprincipal= Regla("Adjprincipal",Produccion("principal"),Produccion("tipico"))

SubTiempo = Regla("SubTiempo",Produccion("tiempo"))
SubMedida = Regla("SubMedida",Produccion("unidad"),Produccion("kilo"),Produccion("kilos"),Produccion("calorias"),Produccion("onza"),Produccion("dozena"))
SubLado = Regla("SubLado",Produccion("lado"),Produccion("costado"))
SubTipo = Regla("SubTipo",Produccion("clase"),Produccion("tipo"))
SubComida = Regla("SubComida",Produccion("postre"),Produccion("plato"),Produccion("comida"))
SubPlato = Regla("SubPlato",Produccion("postre"),Produccion("plato"))
SubReceta = Regla("SubReceta",Produccion("receta"))
SubIngrediente = Regla("SubIngrediente",Produccion("ingredientes"),Produccion("ingrediente"))

PrepPor = Regla("Prepor",Produccion("por"))
PrepAl = Regla("PreAl",Produccion("al"))
PrepDePara = Regla("PrepDePara",Produccion("para"))
PrepPara = Regla("PrepPara",Produccion("para"))
PrepEn = Regla("PrepEn",Produccion("en"))
PrepDe = Regla("PrepDe",Produccion("de"),Produccion("del"))

EntidadIngrediente = Regla("EntidadIngrediente",Produccion("INGREDIENTE"),Produccion("papa"),Produccion("aderezo"),Produccion("arroz"),
    Produccion("ají"),Produccion("yatan"),Produccion("ocopa"),Produccion("pellejo"),Produccion("cuy"),Produccion("venado"),
    Produccion("rocoto"),Produccion("chanca_serrana"),Produccion("plátano"),Produccion("frejol"),Produccion("canela"),
    Produccion("huacatay"),Produccion("maní"),Produccion("cecina"),Produccion("chalona"),Produccion("pescado"),Produccion("lagartos"),
    Produccion("carne"),Produccion("chancho"),Produccion("ají_panca"))
Entidadlocalidad = Regla("Entidadlocalidad",Produccion("LOCALIDAD"),Produccion("lima"),Produccion("arequipa"),Produccion("cuzco"))
EntidadPlato = Regla("EntidadPlato",Produccion("pato"),Produccion("ají_de_gallina"),Produccion("cau_cau"),
    Produccion("aguadito"),Produccion("queso_helado"),Produccion("ceviche"),Produccion("lomo_saltado"),Produccion("caldo_de_chairo"),
    Produccion("arroz_con_pollo"),Produccion("suri"),Produccion("arroz_con_pato"),Produccion("papa_rellena"),Produccion("rocoto_relleno"),
    Produccion("sopa_de_menestron"),Produccion("cuy_chactado"),Produccion("pachamanca"),Produccion("arroz_zambito"),Produccion("masato"),
    Produccion("caucau"),Produccion("tiradito"),Produccion("kam_lu_wantan"),Produccion("cuy_colorado"),Produccion("anticuchos"),
    Produccion("tamales"),Produccion("queso_asado"),Produccion("carapulcra"),Produccion("pisco_sour"),Produccion("mazamorra"),Produccion("cuy")
    ,Produccion("arroz_con_leche"),Produccion("chicharron_de_calamar"),Produccion("sarza_de_patitas"),Produccion("chicha_de_jora")
    ,Produccion("chairo"),Produccion("adobo_de_chancho"),Produccion("kankacho"),Produccion("juanes"),Produccion("chaufa"),
    Produccion("pastel_de_papa"),Produccion("soltero_de_queso"),Produccion("ocopa_arequipeña"),Produccion("enmariñado"),Produccion("papa_a_la_huancaina"),Produccion("puré_de_papa"),
    Produccion("platos_agridulces"),Produccion("cecina"),Produccion("caparinas"),Produccion("lagarto"),Produccion("venado"),Produccion("sancochado"),Produccion("chicharron_de_chancho"),Produccion("caparina"),Produccion("chancho_al_horno"),Produccion("ensalada_césar"))

ProCual = Regla("ProCual",Produccion("cual"))
ProQuien = Regla("ProQuien",Produccion("quien"),Produccion("quién"))
ProDonde = Regla("ProDonde",Produccion("donde"))
ProQue = Regla("ProQue",Produccion("que"))
ProCuanto = Regla("ProCuanto",Produccion("cuanto"),Produccion("cuánto"),Produccion("cuántos"))
ProComo = Regla("ProComo",Produccion("como"),Produccion("cómo"))


vmi=Regla("vmi",Produccion())
vs=Regla("vs",Produccion())
va=Regla("va",Produccion())
nc=Regla("nc",Produccion("diferencia"))
p=Regla("p",Produccion("se"))
pp=Regla("pp",Produccion("puede"),Produccion("puedo"))
aq=Regla("aq",Produccion())
sp=Regla("sp",Produccion("entre"))
DetIndefinido=Regla("DetIndefinido",Produccion("un"),Produccion("unos"))
DetDefinido=Regla("DetDefinido",Produccion("el"),Produccion("del"),Produccion("la"),Produccion("las"),Produccion("los"))

Verbo=Regla("Verbo",Produccion(vmi),Produccion(va),Produccion(vs))
Sub=Regla("Sub",Produccion(nc))
Det= Regla("Det",Produccion(DetDefinido),Produccion(DetIndefinido))
Adj=Regla("Adj",Produccion(aq))
ProRef= Regla("ProRef",Produccion(p),Produccion(pp))
Prep=Regla("Prep",Produccion(sp))


AdjuntoLugar= Regla("AdjuntoLugar",Produccion(PrepEn),Produccion(AdjCerca,PrepDe),Produccion(PrepAl,SubLado,PrepDe))
AdjuntoLocalidad = Regla("AdjuntoLocalidad",Produccion(AdjuntoLugar,Entidadlocalidad))
VNecesitarRef=Regla("VNecesitarRef",Produccion(ProRef,Vnecesitar))
VerboAuxEncontrar = Regla("VerboAuxEncontrar",Produccion(ProRef,Vencontrar),Produccion(Vencontrar),Produccion(Vdeber,Vencontrar))
VerboAuxProducir = Regla("VerboAuxProducir",Produccion(ProRef,Vproducir),Produccion(ProRef,Vdeber,Vproducir),Produccion(Vdeber,Vproducir),Produccion(Vproducir))
VerboAuxTener = Regla("VerboAuxTener",Produccion(ProRef,Vdeber,Vtener),Produccion(Vdeber,Vtener))
VerboAuxComprar= Regla("VerboAuxComprar",Produccion(ProRef,Vcomprar),Produccion(ProRef,Vdeber,Vcomprar),Produccion(Vdeber,Vcomprar),Produccion(Vcomprar))
VerboAuxUtilizar= Regla("VerboAuxUtilizar",Produccion(ProRef,Vdeber,Vutilizar),Produccion(ProRef,Vutilizar),Produccion(Vdeber,Vutilizar),Produccion(Vutilizar))
VerboRefPreparar= Regla("VerboRefPreparar",Produccion(Vpreparar),Produccion(ProRef,Vpreparar),Produccion(Vdeber,Vpreparar))
VerboAuxPreparar= Regla("VerboAuxPreparar",Produccion(ProRef,Vdeber,Vpreparar),Produccion(Vdeber,Vpreparar))
SEntidadPlato=Regla("SEntidadPlato",Produccion(EntidadPlato),Produccion(Det,EntidadPlato),Produccion(DetIndefinido,SubPlato,PrepDe,EntidadPlato))

SVNecesitarPrepararPlato=Regla("SVNecesitarPrepararPlato",Produccion(VNecesitarRef,PrepPara,Vpreparar,EntidadPlato),Produccion(Vnecesitar,SEntidadPlato))
SVPrepararPlato=Regla("SVPrepararPlato",Produccion(Vpreparar,SEntidadPlato))
SEntidadIngrediente=Regla("SEntidadIngrediente",Produccion(EntidadIngrediente),Produccion(Det,EntidadIngrediente))
SEntidadLocalidad=Regla("SEntidadLocalidad",Produccion(Entidadlocalidad),Produccion(Det,Entidadlocalidad))
SubordinadoPlato=Regla("SubordinadoPlato",Produccion(ProRel,VerboAuxPreparar,SEntidadPlato),Produccion(PrepEn,ProRel,VerboAuxPreparar,SEntidadPlato))
SubordinadoLocalidad=Regla("SubordinadoLocalidad",Produccion(ProRel,VerboIdentificar,SEntidadLocalidad))

UnidadesIngredientes=Regla("UnidadesIngredientes",Produccion(SubIngrediente),Produccion(SubMedida,PrepDe,EntidadIngrediente))
TargetIngrediente=Regla("TargetIngrediente",Produccion(SubIngrediente),Produccion(SubTipo,PrepDe,EntidadIngrediente))

SNComida=Regla("SNComida",Produccion(SubComida),Produccion(Det,SubComida),Produccion(SubComida,Adjprincipal),Produccion(Det,SubComida,Adjprincipal))
SNIngrediente=Regla("SNIngrediente",Produccion(SubIngrediente),Produccion(Det,SubIngrediente),Produccion(SubIngrediente,Adjprincipal),Produccion(Det,SubIngrediente,Adjprincipal))
SNReceta=Regla("SNReceta",Produccion(SubReceta),Produccion(Det,SubReceta),Produccion(Det,SubIngrediente),Produccion(SubReceta,Adjprincipal),Produccion(Det,SubReceta,Adjprincipal))
SNRecetaIngrediente=Regla("SNRecetaIngrediente",Produccion(SNReceta),Produccion(SNIngrediente),Produccion(SNIngrediente,PrepDe,SNReceta),Produccion(SNReceta,PrepDe,SNIngrediente),Produccion(SNReceta,PrepDe,SEntidadPlato))
SNProcedimiento=Regla("SNProcedimiento",Produccion(SubProcedimiento),Produccion(Det,SubProcedimiento))

SPrepEntidadLocalidad=Regla("SPrepEntidadLocalidad",Produccion(PrepDe,SEntidadLocalidad),Produccion(PrepEn,SEntidadLocalidad))
SPrepEntidadPlato=Regla("SPrepEntidadPlato",Produccion(PrepDe,SEntidadPlato),Produccion(PrepEn,SEntidadPlato))



SNominal=Regla("SNominal",Produccion(Sub),Produccion(Det,Sub),Produccion(Sub,Adj),Produccion(Det,Sub,Adj),Produccion(ProRef))
Sverbal=Regla("Sverbal",Produccion(Verbo,SNominal),Produccion(Verbo,SNominal,ProRel))

SujetoPlato=Regla("SujetoPlato",Produccion(SEntidadPlato),Produccion(SNominal,Prep,SEntidadPlato),Produccion(SPrepEntidadPlato,Prep,SNominal))
SujetoIngrediente=Regla("SujetoIngrediente",Produccion(SEntidadIngrediente),Produccion(SNominal,Prep,SEntidadPlato),Produccion(SEntidadPlato,Prep,SNominal))

SujetoEntidad=Regla("SujetoEntidad",Produccion(SujetoPlato),Produccion(SujetoIngrediente))

Motivo=Regla("Motivo",Produccion(SujetoEntidad,Sverbal),Produccion(Sverbal,SujetoEntidad))
MotivoMenor=Regla("MotivoMenor",Produccion(SNominal,Sverbal))


SentenciaComo=Regla("SentenciaComo",Produccion(ProComo,VerboRefPreparar,SEntidadPlato))
SentenciaPorque=Regla("SentenciaPorque",Produccion(PrepPor,ProQue,Motivo))

SentenciaCuantoTiempo=Regla("SentenciaCuantoTiempo",Produccion(ProCuanto,SubTiempo,Vresistir,SEntidadPlato))
SentenciaCuantoResiste=Regla("SentenciaCuantoResiste",Produccion(ProCuanto,Vresistir,SEntidadPlato))
SentenciaCuantoUnidades=Regla("SentenciaCuantoUnidades",Produccion(ProCuanto,UnidadesIngredientes,SVNecesitarPrepararPlato))
SentenciaCuanto=Regla("SentenciaCuanto",Produccion(SentenciaCuantoUnidades),Produccion(SentenciaCuantoResiste),Produccion(SentenciaCuantoTiempo))

SentenciaDondeEsHecho=Regla("SentenciaDondeEsHecho",Produccion(ProDonde,VerboAuxProducir,SEntidadPlato),Produccion(ProDonde,VerboAuxEncontrar,SEntidadPlato))
SentenciaDondeConseguir=Regla("SentenciaDondeConseguir",Produccion(ProDonde,VerboAuxComprar,SEntidadPlato),Produccion(ProDonde,VerboAuxComprar,EntidadIngrediente),Produccion(ProDonde,VerboAuxComprar,SEntidadPlato,SPrepEntidadLocalidad))
SentenciaDonde=Regla("SentenciaDonde",Produccion(SentenciaDondeConseguir),Produccion(SentenciaDondeEsHecho))

SentenciaQueDefinicion=Regla("SentenciaQueDefinicion",Produccion(ProQue,Vser,SEntidadPlato),Produccion(ProQue,Vser,SEntidadIngrediente))
SentenciaQueIngrediente=Regla("SentenciaQueIngrediente",Produccion(ProQue,TargetIngrediente,VerboAuxUtilizar,PrepPara,SVPrepararPlato),Produccion(ProQue,TargetIngrediente,Vtener,SEntidadPlato),Produccion(ProQue,TargetIngrediente,VerboAuxTener,SEntidadPlato))
SentenciaQueProcedimiento=Regla("SentenciaQueProcedimiento",Produccion(ProQue,SubProcedimiento,VerboAuxPreparar,SEntidadPlato),Produccion(ProQue,SubProcedimiento,VerboAuxUtilizar,PrepPara,SVPrepararPlato))
SentenciaQue=Regla("SentenciaQue",Produccion(SentenciaQueProcedimiento),Produccion(SentenciaQueIngrediente),Produccion(SentenciaQueDefinicion))
SentenciaQuien=Regla("SentenciaQuien",Produccion(ProQuien,Vinventar,SEntidadPlato))

SentenciaCualProcedimiento=Regla("SentenciaCualProcedimiento",Produccion(ProCual,Vser,SNProcedimiento,PrepDePara,SVPrepararPlato),Produccion(ProCual,Vser,SNProcedimiento,SubordinadoPlato))
SentenciaCualPlatoTipico=Regla("SentenciaCualPlatoTipico",Produccion(ProCual,Vser,SNComida,SPrepEntidadLocalidad),Produccion(ProCual,Vser,SNComida,SubordinadoLocalidad))
SentenciaCualTarget=Regla("SentenciaCualTarget",Produccion(ProCual,Vser,SNRecetaIngrediente,SPrepEntidadPlato))
SentenciaCual=Regla("SentenciaCual",Produccion(SentenciaCualTarget),Produccion(SentenciaCualProcedimiento),Produccion(SentenciaCualPlatoTipico))

S=Regla("S",Produccion(SentenciaDonde),Produccion(SentenciaCual),Produccion(SentenciaQue),Produccion(SentenciaQuien),Produccion(SentenciaCuanto),Produccion(SentenciaComo),Produccion(SentenciaPorque))




for arbol in construir_arbol(parseador(S, "como se prepara la ensalada_césar")):
    print ("--------------------------")
    arbol.imprimir()

