# Import, system
import sys
import re
import queue
import time

sys.setrecursionlimit(10 ** 9)

# Stałe
maks_glebokosc_rekursji_dfs = 25

# Parametry uruchomienia programu
strategia = sys.argv[1]
porzadek_przeszukiwania = sys.argv[2]
wybrana_heurystyka = sys.argv[3]
plik_poczatkowy = sys.argv[4]
plik_koncowy = sys.argv[5]
plik_informacje = sys.argv[6]

# Zmienne
w = 0
k = 0
poprzedni_uklad = tuple()
plansza = tuple()
hashset = set()
stos_ruchow = []
kolejka_ruchow = queue.Queue()
poziomy_rekursji = {plansza: 0}
sciezka = ""
najwieksza_glebokosc_na_jaka_zeszlismy = 0
stany_odwiedzone = 1
stany_przetworzone = 0
####
plansze = list()
ruchyDict = {}
ciag_ruchow = ''


def wczytaj_uklad_poczatkowy():
    plik = open(plik_poczatkowy)
    linia = plik.readline()
    tab = re.findall(r'\d+', linia)
    global w, k
    w = int(tab[0])
    k = int(tab[1])
    print(f"x = {w}, y = {k}")

    kontener_string = []
    for i in range(0, k):
        linia = plik.readline()
        kontener_string.append(re.findall(r'\d+', linia))
        tab_jeden_wymiar = []
        for row in kontener_string:
            for item in row:
                tab_jeden_wymiar.append(str(item))
    global plansza
    plansza = tuple([int(i) for i in tab_jeden_wymiar])


def znajdz_mozliwe_ruchy(wezel):
    global w, k
    rows = w
    cols = k
    zero_index = wezel.index(0)
    row, col = zero_index // cols, zero_index % cols
    moves = ''
    if col > 0 and row in range(rows):
        moves += 'L'
    if col < cols - 1 and row in range(rows):
        moves += 'R'
    if row > 0 and col in range(cols):
        moves += 'U'
    if row < rows - 1 and col in range(cols):
        moves += 'D'
    return moves


def nastepna_plansza(wezel, porzadek):
    poczatkowe_ruchy = znajdz_mozliwe_ruchy(wezel)
    mapowanie = {}
    for w, wezel in enumerate(znajdz_sasiadow(wezel)):
        mapowanie[poczatkowe_ruchy[w]] = wezel

    for m in dict(mapowanie):
        if czy_odwiedzono(mapowanie[m]):
            del mapowanie[m]

    nastepny_ruch = ""
    for ruch in porzadek:
        if ruch in poczatkowe_ruchy and ruch in mapowanie:
            nastepny_ruch = ruch
            break

    if nastepny_ruch == "":
        return tuple()
    else:
        return tuple(mapowanie[nastepny_ruch])


def znajdz_sasiadow(wezel):
    global w
    sasiednie_uklady = []
    nowy_uklad = list(wezel)
    pozycja_0 = wezel.index(0)
    for r, c in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        new_r, new_c = (pozycja_0 // w) + r, (pozycja_0 % w) + c
        if 0 <= new_r < w and 0 <= new_c < w:
            nowy_uklad[pozycja_0], nowy_uklad[new_r * w + new_c] = nowy_uklad[new_r * w + new_c], nowy_uklad[pozycja_0]
            sasiednie_uklady.append(tuple(nowy_uklad))
            nowy_uklad[pozycja_0], nowy_uklad[new_r * w + new_c] = nowy_uklad[new_r * w + new_c], nowy_uklad[pozycja_0]
    # print(f"Węzeł: {wezel} i jego sąsiedzi: {tuple(sasiednie_uklady)}\n\n")
    return tuple(sasiednie_uklady)


def oznacz_jako_odwiedzony(tuple_planszy):
    global hashset
    hashset.add(hash(tuple_planszy))


def oznacz_jako_nieodwiedzony(tuple_planszy):
    global hashset
    if czy_odwiedzono(tuple_planszy):
        hashset.remove(hash(tuple_planszy))


def czy_odwiedzono(tuple_planszy):
    if hash(tuple_planszy) in hashset:
        return 1
    else:
        return 0


def bfs(porzadek):
    global kolejka_ruchow
    global najwieksza_glebokosc_na_jaka_zeszlismy
    global poziomy_rekursji
    global stany_odwiedzone, stany_przetworzone

    poziomy_rekursji = {plansza: 1}

    kolejka_ruchow.put(plansza)

    while not kolejka_ruchow.empty():
        pobrany = kolejka_ruchow.get()
        stany_przetworzone += 1

        if pobrany == tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]):
            generuj_sciezke(pobrany, float('inf'))
            return sciezka

        oznacz_jako_odwiedzony(pobrany)
        aktualna_glebokosc_drzewa = poziomy_rekursji[pobrany]

        if aktualna_glebokosc_drzewa > najwieksza_glebokosc_na_jaka_zeszlismy:
            najwieksza_glebokosc_na_jaka_zeszlismy = aktualna_glebokosc_drzewa

        sasiedzi = ustaw_sasiadow_w_porzadku(pobrany, porzadek)

        for s in sasiedzi:
            if not czy_odwiedzono(s):
                oznacz_jako_odwiedzony(s)
                kolejka_ruchow.put(s)
                stany_odwiedzone += 1
                poziomy_rekursji[s] = aktualna_glebokosc_drzewa + 1

    if sciezka != "":
        return sciezka
    else:
        return -1


def jaki_ruch(plansza_od, plansza_do):
    od_0 = plansza_od.index(0)
    do_0 = plansza_do.index(0)
    global w

    if do_0 - od_0 == -1:
        return "L"
    elif do_0 - od_0 == 1:
        return "R"
    elif do_0 - od_0 == -w:
        return "U"
    elif do_0 - od_0 == w:
        return "D"
    else:
        return None


def ustaw_sasiadow_w_porzadku(wezel, porzadek):
    sasiedzi = znajdz_sasiadow(wezel)
    ruchy = {}
    for s in sasiedzi:
        ruchy[jaki_ruch(wezel, s)] = s

    posortowane_ruchy = {litera: ruchy[litera] for litera in porzadek if litera in ruchy}
    return tuple(posortowane_ruchy.values())


def generuj_sciezke(koniec, min_poziom):
    global sciezka

    if koniec == plansza:
        sciezka = sciezka[::-1]

    sasiedzi = znajdz_sasiadow(koniec)

    for s in sasiedzi:
        if s in poziomy_rekursji and poziomy_rekursji[s] < min_poziom and czy_odwiedzono(s):
            min_poziom = poziomy_rekursji[s]
            sciezka += jaki_ruch(s, koniec)
            generuj_sciezke(s, min_poziom)


def dfs(porzadek):
    global stos_ruchow
    global poziomy_rekursji
    poziomy_rekursji = {plansza: 1}

    def visit():
        global najwieksza_glebokosc_na_jaka_zeszlismy
        global stany_przetworzone, stany_odwiedzone
        aktualna_glebokosc_drzewa = 0

        if not stos_ruchow:
            return tuple()

        zdjety = stos_ruchow.pop()
        stany_przetworzone += 1
        oznacz_jako_odwiedzony(zdjety)
        aktualna_glebokosc_drzewa = poziomy_rekursji[zdjety]

        if aktualna_glebokosc_drzewa > najwieksza_glebokosc_na_jaka_zeszlismy:
            najwieksza_glebokosc_na_jaka_zeszlismy = aktualna_glebokosc_drzewa

        if aktualna_glebokosc_drzewa >= maks_glebokosc_rekursji_dfs:
            for s in znajdz_sasiadow(zdjety):
                oznacz_jako_odwiedzony(s)

        sasiedzi = ustaw_sasiadow_w_porzadku(zdjety, porzadek)
        sasiedzi = sasiedzi[::-1]

        for s in sasiedzi:
            if not czy_odwiedzono(s) and len(sasiedzi) > 1:
                stos_ruchow.append(s)
                stany_odwiedzone += 1
                poziomy_rekursji[s] = aktualna_glebokosc_drzewa + 1

        if zdjety == tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]):
            generuj_sciezke(zdjety, float('inf'))
        visit()

    stos_ruchow.append(plansza)
    visit()
    if sciezka != "":
        return sciezka
    else:
        return -1


def hamming(board):
    wynik = 0
    for i in range(0, k * w):
        if board[i] == i + 1 and board[i] != 0:
            wynik = wynik + 1
    return wynik + najwieksza_glebokosc_na_jaka_zeszlismy


def manhattan(board):
    wynik = 0
    for i in range(0, w * k):
        if board[i] != 0:
            x1 = int(i % w)
            y1 = int(i / w)
            x2 = int((int(board[i]) - 1) % w)
            y2 = int((int(board[i]) - 1) / w)
            wynik = wynik + abs(x1 - x2) + abs(y1 - y2)
    return wynik + najwieksza_glebokosc_na_jaka_zeszlismy


def astr_algorytm(heurystyka, tempPlansza):
    global najwieksza_glebokosc_na_jaka_zeszlismy
    global ciag_ruchow
    global stany_odwiedzone
    global stany_przetworzone
    oznacz_jako_odwiedzony(tempPlansza)

    stany_przetworzone += 1

    if tempPlansza == tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]):
        wynik_astr = tempPlansza
        return wynik_astr

    ruchy = znajdz_mozliwe_ruchy(tempPlansza)

    for ruch in ruchy:
        nowyStan = nastepna_plansza(tempPlansza, ruch)
        if nowyStan != tuple():
            ruchyDict[nowyStan] = ruch
            if hash(nowyStan) not in hashset:
                plansze.append(nowyStan)

    najwieksza_glebokosc_na_jaka_zeszlismy += 1

    if heurystyka == 'manh':
        plansze.sort(key=manhattan)
    elif heurystyka == 'hamm':
        plansze.sort(key=hamming, reverse=True)

    najlepszyStan = plansze.pop(0)
    print(najlepszyStan)
    ciag_ruchow += ruchyDict[najlepszyStan]
    astr_algorytm(heurystyka, najlepszyStan)
    return


def astr(heurystyka):
    astr_algorytm(heurystyka, plansza)


def podaj_rozwiazanie():
    print("test")


def dodatkowe_informacje():
    print("test")


def czas_rozwiazania(czasRozpoczecia):
    czasRozwiazywania = time.time_ns() - czasRozpoczecia
    czasRozwiazywania = czasRozwiazywania / 1000000
    print(round(czasRozwiazywania, 3))


def printujRuchy(ciag_ruchow):
    print(ciag_ruchow)


def ileRuchow(ciag_ruchow):
    try:
        return len(ciag_ruchow)
    except TypeError:
        return -1


### "MAIN" ###:
wczytaj_uklad_poczatkowy()
# print(dfs("URDL"))

czasRozpoczecia = time.time_ns()
# astr("manh")
ruchy = dfs("DRUL")
print("")
czas_rozwiazania(czasRozpoczecia)
print(sciezka)
print(f"ilość ruchów: {ileRuchow(ruchy)}")
print(f"głębokość rekursji: {najwieksza_glebokosc_na_jaka_zeszlismy}")
print(f"stany odwiedzone: {stany_odwiedzone}")
print(f"stany przetworzone: {stany_przetworzone}")
