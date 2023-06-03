import csv
from datetime import datetime


def yazdir(skor, sure):
    tarih = datetime.now().date()
    with open('skorlar.csv', mode='a', newline='') as dosya:
        skor_yazici = csv.writer(dosya, delimiter=',')
        skor_yazici.writerow([skor, sure, tarih])


def oku():
    veri_listesi = []
    with open('skorlar.csv', mode='r') as dosya:
        veri_okuyucu = csv.reader(dosya, delimiter=',')
        veriler = []
        for satir in veri_okuyucu:
            skor = int(satir[0])
            sure = int(satir[1])
            tarih = satir[2]
            veriler.append((skor, sure, tarih))
        veriler.sort(key=lambda x: (x[0], -x[1], x[2]), reverse=True)
        for veri in veriler[:10]:
            skor = veri[0]
            sure = veri[1]
            tarih = veri[2]
            veri_listesi.append(f"Skor: {skor}, Süre: {sure}, Tarih: {tarih}")
    dosya.close()
    return veri_listesi
