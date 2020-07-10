import csv

reader=csv.reader(open(""))
writer=csv.writer(open("","wt",newline=""))
writer.writerow(["DENOMINAZIONESCUOLA","DESCRIZIONEGRADOSCUOLA","PROVINCIA","DESCRIZIONECOMUNE","INDIRIZZOSCUOLA","CAPSCUOLA","CODICECOMUNESCUOLA","INDIRIZZOEMAILSCUOLA","SITOWEBSCUOLA","CODICESCUOLA","LATITUDINE","LONGITUDINE","COR_COMUNE"])


long1=6.60270
lat1=35.07638
long2=19.12499
lat2=47.10169

next(reader)
for row in reader:
    if lat1 < float(row[10]) < lat2:
        if long1 < float(row[11]) <long2:    
            writer.writerow(row)