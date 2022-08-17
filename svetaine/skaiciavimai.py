def kuno_mases_indeksas(ugis, mase):
    ugis_cm = ugis / 100
    kmi = round(mase / ugis_cm / ugis_cm, 1)
    if kmi < 18.5:
        return ["Per mažas svoris", kmi]
    if 18.5 < kmi < 24.9:
        return ["Normalus svoris", kmi]
    if 25 < kmi < 29.9:
        return ["Viršsvoris", kmi]
    if 30 < kmi < 34.9:
        return ["I laipsnio nutukimas", kmi]
    if 35 < kmi < 39.9:
        return ["II laipsnio nutukimas", kmi]
    if 40 < kmi:
        return ["III laipsnio nutukimas", kmi]


def bmr(mase, ugis, amzius, lytis):
    if lytis == "Vyras":
        bmr = 66 + (13.7 * mase) + (5 * ugis) - (6.8 * amzius)
        return bmr
    if lytis == "Moteris":
        bmr = 655 + (9.6 * mase) + (1.8 * ugis) - (4.7 * amzius)
        return bmr


def intensyvumas(intensyvumas, bmr):
    if "0-1" in intensyvumas:
        suma = round(bmr * 1.15)
        return suma
    if "1-2" in intensyvumas:
        suma = round(bmr * 1.375)
        return suma
    if "2-3" in intensyvumas:
        suma = round(bmr * 1.55)
        return suma
    if "3-4" in intensyvumas:
        suma = round(bmr * 1.725)
        return suma
    if "5+" in intensyvumas:
        suma = round(bmr * 1.9)
        return suma


def tikslas(suma):
    mesti_svori = suma - 300
    islaikyti_svori = suma
    auginti_svori = suma + 300
    return [mesti_svori, islaikyti_svori, auginti_svori]


def maisto_svorio_maistingumas(svoris, listas, skaicius):
    for maistingumas in listas:
        pavadinimas = maistingumas.pavadinimas
        kalorijos = round(maistingumas.kalorijos / 100 * int(svoris), 1)
        baltymai = round(maistingumas.baltymai / 100 * int(svoris), 1)
        angliavandeniai = round(maistingumas.angliavandeniai / 100 * int(svoris), 1)
        riebalai = round(maistingumas.riebalai / 100 * int(svoris), 1)
        skaicius += 1
        rezultatas = [pavadinimas, kalorijos, baltymai, angliavandeniai, riebalai, int(svoris), skaicius]
        return rezultatas


def maistingumo_listo_suma(listas):
    baltymai = 0
    angliavandeniai = 0
    riebalai = 0
    kalorijos = 0
    for x in listas:
        baltymai += x[2]
        angliavandeniai += x[3]
        riebalai += x[4]
        kalorijos += x[1]
        print(kalorijos)
    return round(baltymai), round(angliavandeniai), round(riebalai), round(kalorijos)






