import csv 

reader=csv.reader(open(""))
province=["TO","MI","PA","RM","NA"]
writer=csv.writer(open("Elenco_codici_comuni.csv","wt",newline=""))
writer.writerow(["PROVINCIA","DENOMINAZIONE_COMUNE","CODICE_COMUNE"])
next(reader)
for row in reader:
    if row[13] in province:
        writer.writerow([row[13],row[6],row[18]])
        

