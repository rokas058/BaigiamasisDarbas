import datetime as DT


def atnaujinti():
    atnaujinta = DT.datetime(2022, 7, 31).date()
    return atnaujinta


def issukis1(data):
    antra_diena = data + DT.timedelta(days=1)
    trecia_diena = data + DT.timedelta(days=2)
    ketvirta_diena = data + DT.timedelta(days=3)
    penkta_diena = data + DT.timedelta(days=4)
    sesta_diena = data + DT.timedelta(days=5)
    septinta_diena = data + DT.timedelta(days=6)
    with open("issukis1", "w") as f:
        f.write(f'''
{data}
1. 20 atsispaudimu
2. 20 atsilenkimu
3. 3 km begimas

{antra_diena}
1. 25 atsispaudimu
2. 25 atsilenkimu
3. 3 km begimas

{trecia_diena}
1. 30 atsispaudimu
2. 30 atsilenkimu
3. 3 km begimas

{ketvirta_diena}
1. 35 atsispaudimu
2. 35 atsilenkimu
3. 3 km begimas

{penkta_diena}
1. 40 atsispaudimu
2. 40 atsilenkimu
3. 4 km begimas

{sesta_diena}
1. 45 atsispaudimu
2. 45 atsilenkimu
3. 4 km begimas

{septinta_diena}
1. 50 atsispaudimu
2. 50 atsilenkimu
3. 4 km begimas''')
        f.close()



def issukis2(data):
    antra_diena = data + DT.timedelta(days=1)
    trecia_diena = data + DT.timedelta(days=2)
    ketvirta_diena = data + DT.timedelta(days=3)
    penkta_diena = data + DT.timedelta(days=4)
    sesta_diena = data + DT.timedelta(days=5)
    septinta_diena = data + DT.timedelta(days=6)
    with open("issukis2", "w") as f:
        f.write(f'''
{data}
1. 40 atsispaudimu
2. 40 atsilenkimu
3. 4 km begimas

{antra_diena}
1. 45 atsispaudimu
2. 45 atsilenkimu
3. 4 km begimas

{trecia_diena}
1. 50 atsispaudimu
2. 50 atsilenkimu
3. 4 km begimas

{ketvirta_diena}
1. 55 atsispaudimu
2. 55 atsilenkimu
3. 4 km begimas

{penkta_diena}
1. 60 atsispaudimu
2. 60 atsilenkimu
3. 5 km begimas

{sesta_diena}
1. 65 atsispaudimu
2. 65 atsilenkimu
3. 5 km begimas

{septinta_diena}
1. 70 atsispaudimu
2. 70 atsilenkimu
3. 5 km begimas''')
        f.close()


def issukis3(data):
    antra_diena = data + DT.timedelta(days=1)
    trecia_diena = data + DT.timedelta(days=2)
    ketvirta_diena = data + DT.timedelta(days=3)
    penkta_diena = data + DT.timedelta(days=4)
    sesta_diena = data + DT.timedelta(days=5)
    septinta_diena = data + DT.timedelta(days=6)
    with open("issukis3", "w") as f:
        f.write(f'''
{data}
1. 60 atsispaudimu
2. 60 atsilenkimu
3. 5 km begimas

{antra_diena}
1. 65 atsispaudimu
2. 65 atsilenkimu
3. 5 km begimas

{trecia_diena}
1. 70 atsispaudimu
2. 70 atsilenkimu
3. 5 km begimas

{ketvirta_diena}
1. 75 atsispaudimu
2. 75 atsilenkimu
3. 5 km begimas

{penkta_diena}
1. 80 atsispaudimu
2. 80 atsilenkimu
3. 6 km begimas

{sesta_diena}
1. 85 atsispaudimu
2. 85 atsilenkimu
3. 6 km begimas

{septinta_diena}
1. 90 atsispaudimu
2. 90 atsilenkimu
3. 6 km begimas''')
        f.close()


