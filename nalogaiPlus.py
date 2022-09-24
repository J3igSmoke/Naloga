import requests, json
from prettytable import PrettyTable
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog




def get():
    URL = "https://apica.iplus.si/api/Naloga?API_KEY=F5881DF0-4940-406E-82C8-B80DDBA88082"
    page = requests.get(URL)
    besediloStrani = page.text
    obilkaJson = json.loads(besediloStrani)
    return obilkaJson

def post(slovar):
    jsonSlovar= json.dumps(slovar["Data"], ensure_ascii=False).encode('utf8').decode()
    res = requests.post("https://apica.iplus.si/api/Naloga?API_KEY=F5881DF0-4940-406E-82C8-B80DDBA88082",json=jsonSlovar)
    print(res.text)


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
def spremebaRacuna():
    window.destroy()
    newWindow = tk.Tk()

    obilkaJson = get()
    podjetje = (obilkaJson["Data"]["a"]).split("#")
    postavkeRacuna = obilkaJson["Data"]["z"]
    seznamHrane = []
    seznamKolicine = []
    seznamCen = []

    imePodjetja = tk.StringVar(newWindow, value=podjetje[0])
    imePodjetja = tk.Entry(newWindow, textvariable=imePodjetja, width=40)
    imePodjetja.grid(row=1)
    naslovPodjetja = tk.StringVar(newWindow, value=podjetje[1])
    naslovPodjetja = tk.Entry(newWindow, textvariable=naslovPodjetja, width=40)
    naslovPodjetja.grid(row=2)
    obcinaPodjetja = tk.StringVar(newWindow, value=podjetje[2])
    obcinaPodjetja = tk.Entry(newWindow, textvariable=obcinaPodjetja, width=40)
    obcinaPodjetja.grid(row=3)
    matičnaPodjetja = tk.StringVar(newWindow, value=podjetje[3])
    matičnaPodjetja= tk.Entry(newWindow, textvariable=matičnaPodjetja, width=40)
    matičnaPodjetja.grid(row=4)
    prodajalec = tk.StringVar(newWindow, value=obilkaJson["Data"]["b"])
    prodajalec = tk.Entry(newWindow, textvariable=prodajalec, width=40)
    prodajalec.grid(row=5)
    stRacuna = tk.StringVar(newWindow, value=obilkaJson["Data"]["c"])
    stRacuna = tk.Entry(newWindow, textvariable=stRacuna, width=40)
    stRacuna.grid(row=6)
    datum = tk.StringVar(newWindow, value=obilkaJson["Data"]["d"])
    datum = tk.Entry(newWindow, textvariable=datum, width=40)
    datum.grid(row=7)
    davek = tk.DoubleVar(newWindow, value=obilkaJson["Data"]["e"])
    davek = tk.Entry(newWindow, textvariable=davek, width=40)
    davek.grid(row=8)
    ZOI = tk.StringVar(newWindow, value=obilkaJson["Data"]["f"])
    ZOI = tk.Entry(newWindow, textvariable=ZOI, width=40)
    ZOI.grid(row=9)
    EOR = tk.StringVar(newWindow, value=obilkaJson["Data"]["g"])
    EOR = tk.Entry(newWindow, textvariable=EOR, width=40)
    EOR.grid(row=10)
    # status = tk.StringVar(newWindow, value=obilkaJson["Data"]["h"])
    # status = tk.Entry(newWindow, textvariable=status, width=40)
    # status.grid(row=11)
    k=11
    for i in postavkeRacuna:
        imeHrane = tk.StringVar(newWindow, value=i["a"])
        imeHrane = tk.Entry(newWindow, textvariable=imeHrane, width=40)
        imeHrane.grid(column=0, row=k)
        kolicinaHrane = tk.IntVar(newWindow, value=str(i["b"]))
        kolicinaHrane = tk.Entry(newWindow, textvariable=kolicinaHrane, width=10)
        kolicinaHrane.grid(column=1, row=k)
        cena = tk.DoubleVar(newWindow, value=str(i["c"]))
        cena = tk.Entry(newWindow, textvariable=cena, width=10)
        cena.grid(column=2, row=k)
        seznamHrane.append(imeHrane)
        seznamKolicine.append(kolicinaHrane)
        seznamCen.append(cena)
        k+=1

    def shraniSpremebe():
        seznamBool = []
        if isfloat(davek.get()):
            obilkaJson["Data"]["a"]=imePodjetja.get()+"#"+naslovPodjetja.get()+"#"+obcinaPodjetja.get()+"#"+matičnaPodjetja.get()
            obilkaJson["Data"]["b"] = prodajalec.get()
            obilkaJson["Data"]["c"] = stRacuna.get()
            obilkaJson["Data"]["d"] = datum.get()
            obilkaJson["Data"]["e"] = float(davek.get())
            obilkaJson["Data"]["f"] = ZOI.get()
            obilkaJson["Data"]["g"] = EOR.get()
            l=0
            for i in obilkaJson["Data"]["z"]:
                if (isfloat(seznamCen[l].get())) and (seznamKolicine[l].get().isdigit()):
                    seznamBool.append(True)
                    i["a"]=seznamHrane[l].get()
                    i["b"]=int(seznamKolicine[l].get())
                    i["c"]=float(seznamCen[l].get())
                    l+=1
                else:
                    seznamBool.append(False)
            if all(seznamBool):
                shraniRacun(obilkaJson)
            else:
                messagebox.showinfo(title="Poročilo", message="Oblika računa nepravila")
        else:
            messagebox.showinfo(title="Poročilo", message="Oblika računa nepravila")

    tk.Button(newWindow,text="shrani spremebe",command=shraniSpremebe,pady=5,padx=5,bg="#ff3300").grid(row=k)

def shraniRacun(slovar=get()):
    if slovar["Data"]["h"]==5:
        messagebox.showwarning("Opozorilo","Vaš račun je že bil potrjen!")
    else:
        with open(slovar["Data"]["g"] + ".txt", 'w') as f:
                f.write(izdelajRacun(slovar))
                f.close()
        messagebox.showinfo(title="Poročilo", message="Vaš račun je bil shranjen.")
        koncnislovar = slovar
        koncnislovar["Data"]["h"] = 5
        post(koncnislovar)

def odpriRacun():
    file = tk.filedialog.askopenfilename()
    textFile = open(file, "r").read()
    newWindow = tk.Toplevel(window)
    newWindow.wm_transient(window)
    tk.Label(newWindow,text=textFile,justify="left").grid(column=0, row=1)
    tk.Button(newWindow,text="Želite odpreti drug račun",command=odpriRacun,bd=3,  width=20).grid(column=0, row=3)

def izdelajRacun(imeJson=get()):
    obilkaJson = imeJson
    podjetje = (obilkaJson["Data"]["a"]).split("#")
    postavkeRacuna = obilkaJson["Data"]["z"]
    davek = obilkaJson["Data"]["e"]
    besediloracuna=""
    for i in podjetje:
        besediloracuna+=i+"\n"
    t = PrettyTable(['Artikel', 'Količina','Vrednost izdelka',"Davčna stopnja (%)", 'Neto vrednost', 'DDV', 'Bruto vrednost'])
    kolicina=0
    cena=0
    brutocena=0
    for i in postavkeRacuna:
        davek = float(davek)
        kolicinaB=i["b"]
        cenaC=i["c"]
        t.add_row([i["a"],kolicinaB,cenaC,davek*100,round(cenaC*kolicinaB,2),davek,round((cenaC-(cenaC*davek))*kolicinaB,2)])
        brutocena+=round(cenaC-(cenaC*davek),2)
        kolicina+=kolicinaB
        cena+=float(cenaC)
    cena = round(cena,1)
    t.add_row(["Skupaj: ",kolicina,cena,davek*100,cena,davek, round(brutocena,2)])
    besediloracuna += "\n"+ obilkaJson["Data"]["c"] +"\n" +str(t) +"\n" +"\n" +  obilkaJson["Data"]["b"]\
                      +"\n" +  obilkaJson["Data"]["d"]+"\n" +  obilkaJson["Data"]["f"]+"\n" +  obilkaJson["Data"]["g"]
    return besediloracuna

window = tk.Tk()
window.title("Račun")
besediloLable = tk.Label(text=izdelajRacun(),justify="left").grid(column=0, row=1)
gumbShrani = tk.Button(text="Shranite račun",command=shraniRacun, bg='lightblue',bd=3,  width=20).grid(column=0, row=2)
gumbSpremeni = tk.Button(text="Spremeba računa",command=spremebaRacuna, bg='red',bd=3,  width=20).grid(column=0, row=3)
gumbOgled = tk.Button(text="Ogled zgodovine računov",command=odpriRacun, bg='yellow',bd=3,  width=20).grid(column=0, row=4)
window.mainloop()







