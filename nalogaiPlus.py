import requests, os, json
from prettytable import PrettyTable
import tkinter as tk
from tkinter import messagebox


with open("podatkiRacuna.json", "w") as outfile:
    outfile.write("")
def get():
    if os.stat("podatkiRacuna.json").st_size == 0:
        URL = "https://apica.iplus.si/api/Naloga?API_KEY=F5881DF0-4940-406E-82C8-B80DDBA88082"
        page = requests.get(URL)
        besediloStrani = page.text
        with open("podatkiRacuna.json", "w") as outfile:
            outfile.write(besediloStrani)
        datoketa = open('podatkiRacuna.json')
        obilkaJson = json.load(datoketa)
        return obilkaJson
    else:
        datoketa = open('podatkiRacuna.json')
        obilkaJson = json.load(datoketa)
        return obilkaJson

def post(slovar):
    with open("podatkiRacuna.json", "w") as outfile:
        json.dump(slovar, outfile, ensure_ascii=False)

def spremebaRacuna():
    fileName = "podatkiRacuna.json"
    messagebox.showwarning("Opozorilo","V Beležnici spremenite podatke in jih shranite")
    os.system('notepad.exe {}'.format(fileName))
    izdelajRacun(get())
    shraniRacun()

def shraniRacun():
    if get()["Data"]["h"]==5:
        messagebox.showwarning("Opozorilo","Vaš račun je že bil potrjen, če želite račun narediti ponovno poženite program")
    else:
        with open("racun"+ str(get()["Data"]["c"]) +".txt", 'w') as f:
                f.write(izdelajRacun(get()))
                f.close()
        messagebox.showinfo(title="Poročilo", message="Vaš račun je bil shranjen.")
        os.system('notepad.exe {}'.format("racun" + str(get()["Data"]["c"]) + ".txt"))
        koncnislovar = get()
        koncnislovar["Data"]["h"] = 5
        post(koncnislovar)

def odpriRacun():
    izpisDatoteke=""
    trenutnaPot = os.getcwdb()
    for file in os.listdir(trenutnaPot):
        if "racun" in str(file):
            izpisDatoteke += str(file).strip("b") + "\r"
    starRacun = messagebox.askquestion("Želite odpreti stare račune?", izpisDatoteke)
    if(starRacun=="yes"):
        os.startfile(trenutnaPot)

def izdelajRacun(imeJson):
    obilkaJson = imeJson
    podjetje = (obilkaJson["Data"]["a"]).split("#")
    postavkeRacuna = obilkaJson["Data"]["z"]
    davek = obilkaJson["Data"]["e"]
    besediloracuna=""
    for i in podjetje:
        besediloracuna+=i+"\n"
    t = PrettyTable(['Artikel', 'Količina','Vrednost',"Davčna stopnja (%)", 'Neto vrednost', 'DDV', 'Bruto vrednost'])
    kolicina=0
    cena=0
    brutocena=0
    for i in postavkeRacuna:
        t.add_row([i["a"],i["b"],i["c"],davek*100,i["c"],davek,round(i["c"]-(i["c"]*davek),2)])
        brutocena+=round(i["c"]-(i["c"]*davek),2)
        kolicina+=i["b"]
        cena+=float(i["c"])
    cena = round(cena,1)
    t.add_row(["Skupaj: ",kolicina,cena,davek*100,cena,davek, round(brutocena,2)])
    besediloracuna += "\n"+ obilkaJson["Data"]["c"] +"\n" +str(t) +"\n" +"\n" +  obilkaJson["Data"]["b"]\
                      +"\n" +  obilkaJson["Data"]["d"]+"\n" +  obilkaJson["Data"]["f"]+"\n" +  obilkaJson["Data"]["g"]
    return besediloracuna



window = tk.Tk()
window.title("Račun ")
besediloLable = tk.Label(text=izdelajRacun(get()),justify="left").grid(column=0, row=1)
gumbShrani = tk.Button(text="Shranite račun",command=shraniRacun, bg='lightblue',bd=3,  width=20).grid(column=0, row=2)
gumbSpremeni = tk.Button(text="Spremeba računa",command=spremebaRacuna, bg='red',bd=3,  width=20).grid(column=0, row=3)
gumbOgled = tk.Button(text="Ogled zgodovine računov",command=odpriRacun, bg='yellow',bd=3,  width=20).grid(column=0, row=4)
window.mainloop()









