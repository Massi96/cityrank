import urllib   
import spotlight
from rdflib import graph,Literal,Namespace,URIRef
from rdflib.serializer import Serializer
from rdflib.namespace import RDF,RDFS,XSD
import requests
import csv  
import re
import hashlib
import docker
import time

client = docker.from_env()
container_it=client.containers.get("c9e896401036") 
container_en=client.containers.get("233d97c53c0a")

g = graph.Graph()

cro = Namespace("http://www.cityrank.org/ontology/")
geo = Namespace("https://schema.org/GeoCoordinates")
plc = Namespace("https://schema.org/Place")
schema = Namespace("https://schema.org")
owl= Namespace("http://www.w3.org/2002/07/owl")
addr=Namespace("https://schema.org/PostalAddress")
rdfs=Namespace("http://www.w3.org/2000/01/rdf-schema#")
base = "http://www.cityrank.org/resource/"
dbpediaurl = "http://dbpedia.org/resource/" 
not_found={}
g.bind("cro",cro)
g.bind("geo", geo)
g.bind("schema", schema)
g.bind("addr", addr)
g.bind("owl", owl)
g.bind("rdfs", rdfs)
g.bind("plc", plc)

province={"Roma":"Rome","Napoli":"Naples","Torino":"Turin","Palermo":"Palermo","Milano":"Milan"}

def clean_nome(nome):
    words = {
        "LUINI":" BERNARDINI LUINI ",
        "DA VINCI":" LEONARDO DA VINCI ",
        "P.MATTARELLA":" PIERSANTI MATTARELLA ",
        "CARDUCCI":" GIOSUè CARDUCCI ",
        "CALDERINI":" MARIO CALDERINI ",
        "BORSELLINO":" PAOLO BORSELLINO ",
        "FALCONE":" GIOVANNI FALCONE ",
        "V.E. II":" VITTORIO EMANUELE II ",
        "V.E. III":" VITTORIO EMANUELE III ",
        "V.EMANUELE II":" VITTORIO EMANUELE II ",
        "V.EMANUELE III":" VITTORIO EMANUELE III ",
        "EMANUELE II":" VITTORIO EMANUELE II ",
        "EMANUELE III":" VITTORIO EMANUELE III ",
        "BERNINI" : " GIAN LORENZO BERNINI ",
        "VOLTA": " ALESSANDRO VOLTA ",
        "TURRISI": " NICOLò TURRISI COLONNA ",
        "FERMI " : " ENRICO FERMI ",
        "COSTA" : " GAETANO COSTA ",
        "MARCONI" : " GUGLIELMO MARCONI ",
        "GALILEI" : " GALILEO GALILEI ",
        "FERRARA" : " FRANCESCO FERRARA ",
        "FRANCESCHINI" : " EZIO FRANCESCHINI ",
        "GRAMSCI" : " ANTONIO GRAMSCI ",
        "BESTA" : " FABIO BESTA ",
        "GALLI" : " MATTEO GALLI ",
        "MOZART" : " Wolfgang Amadeus Mozart ",
        "EINAUDI" : " LUDOVICO EINAUDI ",
        "MANZONI":" ALESSANDRO MANZONI ",
        "RAFFAELLO":" RAFFAELLO SANZIO ",
        "SVEVO":" ITALO SVEVO ",
        "LEOPARDI":" GIACOMO LEOPARDI ",
        "PASCOLI":" GIOVANNI PASCOLI ",
        "FOSCOLO":" UGO FOSCOLO ",
        "PIRANDELLO":" LUIGI PIRANDELLO ",
        "VESPUCCI":" AMERIGO VESPUCCI ",
        "NEWTON":" ISAAC NEWTON ",
        "EINSTEIN":" ALBERT EINSTEIN ",
        "INGRASSIA":" GIOVANNI FILIPPO INGRASSIA ",
        "SRL":"",
        "IRCCS":"",
        "CDC":"",
        "AZ.":"",
        "C. DI C.":"",
        "OSPEDALE":"",
        "OSP":"",
        "P.GIACCONE":" PAOLO GIACCONE ",
        "IOS":"",
        "G. Di Cristina":"GIOVANNI DI CRISTINA",
               
    }
    for key,value in words.items():
        nome = nome.replace(key,value)
    
    return re.sub("[A-Za-z]"+"\.", "", nome)

def clean_comune(comune):                   
    c=comune.replace(" ","_").title()
    c=c.replace("u'","ù")
    c=c.replace("e'","è")
    c=c.replace("i'","ì")
    c=c.replace("a'","à")               
    c=c.replace("o'","ò")
    c=c.replace("_Delle_","_delle_")
    c=c.replace("_Della_","_della_")
    c=c.replace("_Degli_","_degli_")                
    c=c.replace("Dè_Pecchi","de'_Pecchi")
    c=c.replace("_D'","_d'")
    c=c.replace("_Da_","_da_")
    c=c.replace("_La_","_la_")
    c=c.replace("_Con_","_con_")
    c=c.replace("_Presso_","_presso_")
    c=c.replace("_Sopra_","_sopra_")
    c=c.replace("Campiglione_Fenile","Campiglione-Fenile")
    c=c.replace("_Del_","_del_")
    c=c.replace("_Nel_","_nel_")
    c=c.replace("_Al_","_al_")
    c=c.replace("_Dei_","_dei_")
    c=c.replace("_Di_","_di_")
    c=c.replace("_Sul_","_sul_")
    c=c.replace("_Sull'","_sull'")
    c=c.replace("_Su_","_su_")
    c=c.replace("_A_","_a_")
    c=c.replace("Roma","Rome")
    c=c.replace("Milano","Milan")
    c=c.replace("Torino","Turin")
    c=c.replace("Napoli","Naples")
    

    return  c

# Province

with open("") as prov:
    print("Adding properties for province")
    reader = csv.reader(prov)
    next(reader)
    
    for row in reader:
        uri_prov = base + row[0].lower()
        uri_coordinate=base+"loc-"+ row[0].lower()
        # Per l'iserimento nella classe 
        g.add([URIRef(uri_prov),RDF.type,cro.Provincia])

        #Creazione istanza geoCoordinates
        g.add([URIRef(uri_coordinate),RDF.type,schema.GeoCoordinates])
        g.add([URIRef(uri_coordinate),geo.latitude,Literal(row[45],datatype=XSD.string)])
        g.add([URIRef(uri_coordinate),geo.longitude,Literal(row[46],datatype=XSD.string)])
        g.add([URIRef(uri_prov),plc.geo,URIRef(uri_coordinate)])
       
        
        
        # Data properties
        g.add([URIRef(uri_prov),rdfs.label,Literal(row[0])])
        g.add([URIRef(uri_prov),cro.reddito,Literal(row[1],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.retribuzione,Literal(row[3],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.pensioni,Literal(row[5],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.rifiuti,Literal(row[7],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.differenziata,Literal(row[9],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.incidenti,Literal(row[11],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.furtiAuto,Literal(row[13],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.furtiCase,Literal(row[15],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.furti,Literal(((float(row[13])+float(row[15]))),datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.tassodis,Literal(row[17],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.tassodisg,Literal(row[19],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.difftasso,Literal(row[21],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.tassonata,Literal(row[23],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.tassomorte,Literal(row[25],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.indiceVecchiaia,Literal(row[27],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.postiletto,Literal(row[29],datatype=XSD.int)])
        g.add([URIRef(uri_prov),cro.banda,Literal(row[31],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.abitanti,Literal(row[33],datatype=XSD.int)])
        g.add([URIRef(uri_prov),cro.area,Literal(row[34],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.Nospedali,Literal(row[35],datatype=XSD.int)])
        g.add([URIRef(uri_prov),cro.Nscuole,Literal(row[36],datatype=XSD.int)])
        g.add([URIRef(uri_prov),cro.Nbiblioteche,Literal(row[37],datatype=XSD.int)])
        g.add([URIRef(uri_prov),cro.rapportoOspedali,Literal(row[38],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.rapportoScuole,Literal(row[40],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.rapportoBiblioteche,Literal(row[42],datatype=XSD.string)])
        g.add([URIRef(uri_prov),cro.indiceVivibilita,Literal(row[44],datatype=XSD.string)])        
        
        # Interlinking Provincia  
        g.add([URIRef(uri_prov),owl.sameAs,URIRef(dbpediaurl + province[row[0]])]) # Poichè siamo sicuri dell'esistenza della provincia non abbiamo bisogno di nessun controllo

        
# Comuni e Scuole
with open("") as prov:
    reader = csv.reader(prov)
    next(reader) 
    print("Adding properties for Scuole")
    only_person_filter = {'types': "DBpedia:Person"}
    
    print("Starting italian container...")
    container_it.start() 
    time.sleep(30)
    i=1
    for row in reader:
       
        
        uri_com=base+row[6]
        uri_scu = base  + row[9].lower()
        uri_coordinate= base+"loc-"+row[9].lower()
        uri_addr=base+"addr-"+row[9].lower()
        uri_prov=base+row[2].lower()

        # Creazione istanza PostalAddress
        g.add([URIRef(uri_addr),RDF.type,schema.PostalAddress])
        g.add([URIRef(uri_addr),addr.addressCountry,Literal("Italia",datatype=XSD.string)])
        g.add([URIRef(uri_addr),addr.addressLocality,Literal(row[3],datatype=XSD.string)])
        g.add([URIRef(uri_addr),addr.addressRegion,Literal(row[2],datatype=XSD.string)])
        g.add([URIRef(uri_addr),addr.postalCode,Literal(row[5],datatype=XSD.string)])
        g.add([URIRef(uri_addr),addr.streetAddress,Literal(row[4],datatype=XSD.string)])

        # Creazione istanza geoCoordinates
        g.add([URIRef(uri_coordinate),RDF.type,schema.GeoCoordinates])
        g.add([URIRef(uri_coordinate),geo.latitude,Literal(row[10],datatype=XSD.string)])
        g.add([URIRef(uri_coordinate),geo.longitude,Literal(row[11],datatype=XSD.string)])
        g.add([URIRef(uri_coordinate),geo.address,URIRef(uri_addr)])

        # Per l'inserimento nelle classi
        g.add([URIRef(uri_com),RDF.type,cro.Comune]) 
        g.add([URIRef(uri_scu),RDF.type,cro.Scuole])
        
        # Object property
        g.add([URIRef(uri_com),cro.haProvincia,URIRef(base+row[2].lower())]) 
        g.add([URIRef(uri_com),cro.haIstituto,URIRef(uri_scu)])
        g.add([URIRef(uri_scu),plc.geo,URIRef(uri_coordinate)])
        
        # Data property
        g.add([URIRef(uri_scu),cro.descrizioneStruttura,Literal(row[1],datatype=XSD.string)])
        g.add([URIRef(uri_scu),cro.email,Literal(row[7],datatype=XSD.string)])
        g.add([URIRef(uri_scu),cro.sitoWeb,Literal(row[8],datatype=XSD.anyURI)])
        g.add([URIRef(uri_com),rdfs.label,Literal(row[3])])
        g.add([URIRef(uri_scu),rdfs.label,Literal(row[0])])
        
        # Interlinking comune
        while 1:
            try:
                richiesta = requests.get(dbpediaurl+clean_comune(row[3]))
                if(richiesta.status_code == 200):
                    g.add([URIRef(uri_com),owl.sameAs,URIRef(dbpediaurl+ clean_comune(row[3]))])
                break
            except(requests.exceptions.ConnectionError):
                time.sleep(10)

        #Interlinking Scuola   
        while 1:
            try:
                intitolato=spotlight.annotate("http://localhost:2230/rest/annotate",clean_nome(row[0]),confidence=0.1,filters=only_person_filter)  
                g.add([URIRef(uri_scu),cro.intitolatoA,URIRef(intitolato[0]["URI"])])
                break
            except (spotlight.SpotlightException):
                not_found[clean_nome(row[0])]=uri_scu
                
                break
            except(requests.exceptions.ConnectionError):
                time.sleep(10)
                
    print("Stopping italian container...")
    container_it.stop()    
    
   
    if not_found:
        
        print("Starting english container...")               
        container_en.start()                            
        print("started")
        time.sleep(30)
        
        for item in not_found: 
            while 1:
                try:
                    intitolato=spotlight.annotate("http://localhost:2222/rest/annotate",item,confidence=0.1,filters=only_person_filter)  
                    g.add([URIRef(not_found[item]),cro.intitolatoA,URIRef(intitolato[0]["URI"])])
                    i+=1
                    print(i)
                    break
                except(spotlight.SpotlightException):
                    print("Resource "+item+" not found")
                    break
                except(requests.exceptions.ConnectionError):
                    time.sleep(10)
        container_en.stop()
            
# Ospedali     
with open("") as osp:
    print("Adding properties for Ospedali")
    reader = csv.reader(osp)
    next(reader) 
    
    only_person_filter = {'types': "DBpedia:Person"}
    m = hashlib.new('ripemd160')
    h=[]
    
    
    print("Starting italian container...")       
    container_it.start()
    time.sleep(20)

    #Creazione uri ospedale tramite hashing
    for row in reader:
        m.update(row[1].encode())
        digest=m.hexdigest()
        while digest in h:
            digest=digest+"2"
    
        uri_osp = base  + digest
        uri_coordinate= base+"loc-"+digest
        uri_addr=base+"addr-"+digest
        h.append(digest)
        
        uri_com=base + row[11]
        uri_prov=base + row[0]
        
        #Creazione istanza PostalAddress
        g.add([URIRef(uri_addr),RDF.type,schema.PostalAddress])
        g.add([URIRef(uri_addr),addr.addressCountry,Literal("Italia",datatype=XSD.string)])
        g.add([URIRef(uri_addr),addr.addressLocality,Literal(row[4],datatype=XSD.string)])
        g.add([URIRef(uri_addr),addr.addressRegion,Literal(row[0],datatype=XSD.string)])
        g.add([URIRef(uri_addr),addr.postalCode,Literal(row[3],datatype=XSD.string)])
        g.add([URIRef(uri_addr),addr.streetAddress,Literal(row[2],datatype=XSD.string)])

        #Creazione istanza geoCoordinates
        g.add([URIRef(uri_coordinate),RDF.type,schema.GeoCoordinates])
        g.add([URIRef(uri_coordinate),geo.latitude,Literal(row[8],datatype=XSD.string)])
        g.add([URIRef(uri_coordinate),geo.longitude,Literal(row[9],datatype=XSD.string)])
        g.add([URIRef(uri_coordinate),geo.address,URIRef(uri_addr)])

        # Per l'inserimento nella classe
        g.add([URIRef(uri_osp),RDF.type,cro.Ospedali])

        # Interlinking Ospedali
        while 1:
            try:
                intitolato=spotlight.annotate("http://localhost:2230/rest/annotate",clean_nome(row[1]),confidence=0.1,filters=only_person_filter)  
                g.add([URIRef(uri_osp),cro.intitolatoA,URIRef(intitolato[0]["URI"])])
                break
            except (spotlight.SpotlightException):
                print("Resource " + clean_nome(row[1])  + " not found")
                break
            except(requests.exceptions.ConnectionError):
                time.sleep(10)
         
        # Object property
        
        g.add([URIRef(uri_com),cro.haIstituto,URIRef(uri_osp)])      
        g.add([URIRef(uri_osp),plc.geo,URIRef(uri_coordinate)])      

        # Data property
        g.add([URIRef(uri_osp),cro.descrizioneStruttura,Literal(row[5],datatype=XSD.string)])
        g.add([URIRef(uri_osp),cro.email,Literal(row[5],datatype=XSD.string)])
        g.add([URIRef(uri_osp),cro.strada,Literal(row[2],datatype=XSD.string)])        
        g.add([URIRef(uri_osp),rdfs.label,Literal(row[1])])
        g.add([URIRef(uri_osp),cro.sitoWeb,Literal(row[7],datatype=XSD.anyURI)])
    container_it.stop()


# Biblioteche
with open("")as bib:        
    reader = csv.reader(bib)
    print("Adding properties for Biblioteche")
    next(reader)  

    for row in reader:
        uri_b = base + row[2][-9:]
        uri_coordinate=base+"loc-"+row[2][-9:]
        uri_addr=base+"addr-"+row[2][-9:]

        #Creazione istanza PostalAddress
        g.add([URIRef(uri_addr),RDF.type,schema.PostalAddress])
        g.add([URIRef(uri_addr),addr.addressCountry,Literal("Italia",datatype=XSD.string)])
        g.add([URIRef(uri_addr),addr.addressLocality,Literal(row[8],datatype=XSD.string)])
        g.add([URIRef(uri_addr),addr.addressRegion,Literal(row[0].lower(),datatype=XSD.string)])
        g.add([URIRef(uri_addr),addr.postalCode,Literal(row[4],datatype=XSD.string)])
        g.add([URIRef(uri_addr),addr.streetAddress,Literal(row[3],datatype=XSD.string)])

        #Creazione istanza geoCoordinates
        g.add([URIRef(uri_coordinate),RDF.type,schema.GeoCoordinates])
        g.add([URIRef(uri_coordinate),geo.latitude,Literal(row[6],datatype=XSD.string)])
        g.add([URIRef(uri_coordinate),geo.longitude,Literal(row[7],datatype=XSD.string)])
        g.add([URIRef(uri_coordinate),geo.address,URIRef(uri_addr)])

        # Per l'inserimento nella classe
        g.add([URIRef(uri_com),RDF.type,cro.Comune])
        g.add([URIRef(uri_b),RDF.type,cro.Biblioteche])
        
        # Object property
        g.add([URIRef(uri_com),cro.haIstituto,URIRef(uri_b)])
        g.add([URIRef(uri_b),plc.geo,URIRef(uri_coordinate)])
        # Data property
        
        g.add([URIRef(uri_b),rdfs.label,Literal(row[1])])
        
        # Interlinking comune
        while 1:
            try:
                richiesta = requests.get(dbpediaurl+clean_comune(row[3]))
                if(richiesta.status_code == 200):
                    g.add([URIRef(uri_com),owl.sameAs,URIRef(dbpediaurl+ clean_comune(row[5]))])
                break
            except(requests.exceptions.ConnectionError):
                time.sleep(10)

        # Interlinking Biblioteche
        g.add([URIRef(uri_b),owl.sameAs,URIRef(row[2])])
        
# Creazione ttl
g.serialize(destination="CityRank.ttl",format="turtle")         

