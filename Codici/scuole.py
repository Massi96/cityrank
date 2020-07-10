from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import csv
import socket

'''------ La funzione filtra_csv elabora il dataset dell'anagrafcia delle scuole e da quello estrae, solamente per le 5 province che ci interessano,
        una serie di attributi. Richiama al suo interno altre 2 funzioni: 
        -address_clean: elimina tutte le abbreviazioni del tipo "P.ZA o C.SO" sostituendole con le parole intere
        -risolvi coordinate: Questa funzione sfrutta il servizio Nominatim di openStreetMap per trovare le coordinate delle scuole in base all'indirizzo-------'''

def filtra_csv():
    province=["PALERMO","ROMA","NAPOLI","MILANO","TORINO"]  #Elenco delle province delle quali vogliamo estrarre i dati
    with open("","w",newline="") as f: #Creazione file output
    
        file_output=csv.writer(f)
        #-------Scrittura della riga d'intestazione
        file_output.writerow(["DENOMINAZIONESCUOLA","DESCRIZIONEGRADOSCUOLA","PROVINCIA","DESCRIZIONECOMUNE","INDIRIZZOSCUOLA","CAPSCUOLA","CODICECOMUNESCUOLA","INDIRIZZOEMAILSCUOLA","SITOWEBSCUOLA","CODICESCUOLA","LATITUDINE","LONGITUDINE","COR_COMUNE"])
        #-------------
        file_input=csv.reader(open("","r")) #apertura del dataset iniziale
        
        for row in file_input:
            #Leggo il file riga per riga e controllo che la provincia letta sia contenuta nel vettore province 
            if row[3] in province:
                ''' per ogni riga viene corretta la stringa che rappresenta la via (row[8]) e questa viene poi passata alla funzione risolvi_coordinate,
                    concatenando a questa la provincia (row[3]), il comune (row[11]) e il cap (row[9]) se questo è disponibile.'''
                indirizzo=address_clean(row[8])  
                coordinate=risolvi_coordinate(indirizzo+","+row[3]+","+row[11]+","+row[9] if row[9]!="NON Disponibile" else "")

                if coordinate: 
                    #Se abbiamo ottenuto le coordinate vado a scrivere nel file finale la riga contenente le informazioni utili
                    '''L'ultima colonna è un flag che ci indica se le coordinate ottenute sono quelle del comune in cui la scuola ha sede o meno,
                    questo è necessario poichè se non si trovano le coordinate dell'indirizzo completo andiamo a cercare quelle del comune (vedi riga 36) 
                    in maniera da evitare di avere troppe cordinate poste a (0,0)'''

                    file_output.writerow([row[3],row[13],row[7],row[11],indirizzo,row[9],row[10],row[16],row[18],row[6],coordinate[0],coordinate[1],0])
                else:
                    coordinate_comune=risolvi_coordinate("Comune di "+row[11])
                    if coordinate_comune:
                        file_output.writerow([row[3],row[13],row[7],row[11],indirizzo,row[9],row[10],row[16],row[18],row[6],coordinate_comune[0],coordinate_comune[1],1])
                    else: 
                        # Se non vengono ricavate nemmeno le coordinate del comune andiamo ad inserire (0,0)
                        file_output.writerow([row[3],row[13],row[7],row[11],indirizzo,row[9],row[10],row[16],row[18],row[6],0,0,0])


''' La funzione address_clean serve a scrivere per intero gli indirizzi, in modo da facilitare la ricerca delle coordinate con nominatim
La funzione prende in input una stringa e verifica se questa contiene delle abbreviazioni, se è così va a trovare l'indice in cui inizia 
l'abbreviazione ( questo è necessario perchè non tutti gli indirizzi nel dataset cominciano per "Via", "corso" ecc).
A qual punto rimpiazza la parola abbreviata con quella intera e a questa concatena tutta la parte successiva della stringa di partenza.
La stringa corretta viene restituita ed è usata nella funzione filtra_csv'''

def address_clean(indirizzo):
    
    if "P.ZA" in indirizzo:
        indice=indirizzo.index("P.ZA")
        indirizzo=indirizzo.replace("P.ZA","PIAZZA"+indirizzo[indice+4])
        
    if "P.ZZA" in indirizzo:
        indice=indirizzo.index("P.ZZA")
        indirizzo=indirizzo.replace("P.ZZA","PIAZZA"+indirizzo[indice+5])
        
    if "P.LE" in indirizzo:
        indice=indirizzo.index("P.LE")       
        indirizzo=indirizzo.replace("P.LE","PIAZZALE"+indirizzo[indice+4])
        
    if "C.SO" in indirizzo:
        indice=indirizzo.index("C.SO")        
        indirizzo=indirizzo.replace("C.SO","CORSO"+indirizzo[indice+4])
        
    if "V.LE" in indirizzo:
        indice=indirizzo.index("V.LE")       
        indirizzo=indirizzo.replace("V.LE","VIALE"+indirizzo[indice+4])
        
    if ("C.DA" in indirizzo) |("C\DA" in indirizzo):
        indice=indirizzo.index("C.DA" or "C\DA")        
        indirizzo=indirizzo.replace("C.DA","CONTRADA"+indirizzo[indice+4])
      
    if "B.TA" in indirizzo:
        indice=indirizzo.index("B.TA")        
        indirizzo=indirizzo.replace("B.TA","BORGATA"+indirizzo[indice+4])
   
    if "L.GO" in indirizzo:
        indice=indirizzo.index("L.GO")       
        indirizzo=indirizzo.replace("L.GO","LARGO"+indirizzo[indice+4])
    
    return indirizzo

#Questa funzione prende in input l'indirizzo già corretto e cerca di ricavarne le coordinate
def risolvi_coordinate(indirizzo):
    # Creazione del geolocator, la keyword user_agente è richiesta dalla policy di nominatim per "identificare" il tipo di utilizzatore del servizio, l'omissione di questa provoca un warning
    geolocator=Nominatim(user_agent="MyApp") 
    
    '''Eseguo la richiesta dentro un blocco try-except poichè potrebbero esserci delle eccezioni durante la sua esecuzione, 
        il server potrebbe infatti bloccare le nostre richieste causando quindi un timeOut.
        Se questo avviene blocco il programma per 30 secondi prima di tornare a fare delle richieste.
        Tra una richiesta e l'altra è presente uno sleep di 0.5 secondi'''
    try:
        c=geolocator.geocode(indirizzo)
    except GeocoderTimedOut:
        time.sleep(30)
        c=risolvi_coordinate(indirizzo)
    except socket.timeout:
        time.sleep(30)
        c=risolvi_coordinate(indirizzo)
    
    time.sleep(0.5)

    '''Verifico di aver ottenuto una risposta da nominatim,il quale ritorna una lista di due elementi, nella posizione 0 abbiamo una stringa che ci identifica l'indirizzo,
    nella posizione 1 abbiamo un'altra lista contenente latitudine e longitudine, quindi restituiamo solamente questa seconda parte.'''
    if c: 
        if len(c[1])==2: # Questo controllo è necessario perchè può capitare che non si ottengano contemporaneamente latitudine e longitudine ma solamente una di queste.
            return c[1]
        else:
            c=risolvi_coordinate(indirizzo)
    else:
        return None

if __name__ == '__main__':
    filtra_csv()
