# Import, system
import sys
import re
import queue
import time
import board

sys.setrecursionlimit(10 ** 9)

# Stałe
maks_glebokosc_rekursji_dfs = 20

# Parametry uruchomienia programu
strategia = sys.argv[1]
porzadek_przeszukiwania_lub_heurystyka = sys.argv[2]
plik_poczatkowy = sys.argv[3]
plik_koncowy = sys.argv[4]
plik_informacje = sys.argv[5]

# Zmienne
w = 0
k = 0
poprzedni_uklad = tuple()
plansza = tuple()
hashset = set()
stos_ukladow = []
kolejka_ruchow = queue.Queue()
poziomy_rekursji = {plansza: 0}
sciezka = ""
najwieksza_glebokosc_na_jaka_zeszlismy = 0
stany_odwiedzone = 1
stany_przetworzone = 0
dfs_dictionary = dict()
####
plansze = list()
ruchyDict = {}


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
    plik.close()


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


def dfs_oznacz_jako_odwiedzony(tuple, aktualna_glebokosc):
    global dfs_dictionary
    dfs_dictionary[hash(tuple)] = aktualna_glebokosc


def dfs_czy_odwiedzono(tuple, aktualna_glebokosc):
    global dfs_dictionary
    if hash(tuple) not in dfs_dictionary:
        return False
    if hash(tuple) in dfs_dictionary and aktualna_glebokosc < dfs_dictionary[hash(tuple)]:
        return False
    else:
        return True


def oznacz_jako_nieodwiedzony(tuple_planszy):
    global hashset
    if czy_odwiedzono(tuple_planszy):
        hashset.remove(hash(tuple_planszy))


def czy_odwiedzono(tuple_planszy):
    if hash(tuple_planszy) in hashset:
        return 1
    else:
        return 0


def czy_sasiedzi(sasiad1, sasiad2):
    if sasiad1 in znajdz_sasiadow(sasiad2):
        return True
    else:
        return False


def dfs(porzadek):
    global stos_ukladow
    global poziomy_rekursji
    global dfs_dictionary

    def visit():
        global najwieksza_glebokosc_na_jaka_zeszlismy
        global stany_przetworzone, stany_odwiedzone, dfs_dictionary

        if not stos_ukladow:
            return tuple()

        zdjety = stos_ukladow.pop()

        if zdjety.tab == tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]):
            dfs_generuj_sciezke(zdjety.tab, float('inf'), zdjety.depth)
            return sciezka

        stany_przetworzone += 1
        # oznacz_jako_odwiedzony(zdjety)
        # aktualna_glebokosc_drzewa = dfs_dictionary[hash(zdjety)]
        if not dfs_czy_odwiedzono(zdjety.tab, zdjety.depth):
            dfs_oznacz_jako_odwiedzony(zdjety.tab, zdjety.depth)

        if zdjety.depth > najwieksza_glebokosc_na_jaka_zeszlismy:
            najwieksza_glebokosc_na_jaka_zeszlismy = zdjety.depth

        sasiedzi = ustaw_sasiadow_w_porzadku(zdjety.tab, porzadek)
        sasiedzi = sasiedzi[::-1]

        # for s in znajdz_sasiadow(zdjety):
        # oznacz_jako_odwiedzony(s)

        if zdjety.depth < maks_glebokosc_rekursji_dfs:
            for s in sasiedzi:
                if not dfs_czy_odwiedzono(s, zdjety.depth):  # and len(sasiedzi) > 1:
                    sb = board.Board(s)
                    sb.depth = zdjety.depth + 1
                    stos_ukladow.append(sb)
                    # dfs_oznacz_jako_odwiedzony(s, aktualna_glebokosc_drzewa)
                    stany_odwiedzone += 1
                    # poziomy_rekursji[s] = aktualna_glebokosc_drzewa + 1
                    # dfs_dictionary[hash(s)] = aktualna_glebokosc_drzewa + 1
        visit()

    uklad = board.Board(plansza)
    stos_ukladow.append(uklad)
    visit()


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


def dfs_generuj_sciezke(koniec, min_poziom, glebokosc):
    global sciezka

    if koniec == plansza:
        sciezka = sciezka[::-1]

    sasiedzi = znajdz_sasiadow(koniec)

    for s in sasiedzi:
        if hash(s) in dfs_dictionary and dfs_dictionary[hash(s)] < min_poziom and dfs_czy_odwiedzono(s, glebokosc):
            min_poziom = dfs_dictionary[hash(s)]
            sciezka += jaki_ruch(s, koniec)
            dfs_generuj_sciezke(s, min_poziom, glebokosc)


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


def astr_algorytm(heurystyka, badanyWezel):
    global najwieksza_glebokosc_na_jaka_zeszlismy
    global sciezka
    global stany_odwiedzone
    global stany_przetworzone
    oznacz_jako_odwiedzony(badanyWezel)

    stany_przetworzone += 1

    if badanyWezel == tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]):
        najwieksza_glebokosc_na_jaka_zeszlismy += 1
        wynik_astr = badanyWezel
        return wynik_astr

    ruchy = znajdz_mozliwe_ruchy(badanyWezel)

    for ruch in ruchy:
        nowyWezel = nastepna_plansza(badanyWezel, ruch)
        if nowyWezel != tuple():
            ruchyDict[nowyWezel] = ruch
            if hash(nowyWezel) not in hashset:
                plansze.append(nowyWezel)
                stany_odwiedzone += 1

    najwieksza_glebokosc_na_jaka_zeszlismy += 1

    if heurystyka == 'manh':
        plansze.sort(key=manhattan)
    elif heurystyka == 'hamm':
        plansze.sort(key=hamming, reverse=True)  # szukamy tego co ma najwiecej pol na odpowiednim miejscu -> odwracamy kolejnosc

    najblizszyStan = plansze.pop(0)
    print(najblizszyStan)
    sciezka += ruchyDict[najblizszyStan]
    astr_algorytm(heurystyka, najblizszyStan)
    return


def astr(heurystyka):
    astr_algorytm(heurystyka, plansza)


def podaj_rozwiazanie():
    print("test")


def dodatkowe_informacje():
    print("test")


def wyliczanieCzasuRozwiazania(czasRozpoczecia):
    wynik = time.time_ns() - czasRozpoczecia
    wynik = wynik / 1000000
    return round(wynik, 3)


def printujRuchy(sciezka):
    print(sciezka)


def ileRuchow(sciezka):
    try:
        return len(sciezka)
    except TypeError:
        return -1


def zapisz_do_plikow(pl_koncowy, pl_informacje):
    global stany_odwiedzone, stany_przetworzone, najwieksza_glebokosc_na_jaka_zeszlismy, czas_koncowy

    k1 = open(f"./rozwiazania/pliki_koncowe/{pl_koncowy}", "w")
    if sciezka == "":
        k1.write("-1")
        k1.close()
    else:
        k1.write(f"{ileRuchow(sciezka)}\n")
        k1.write(sciezka)
        k1.close()

    i1 = open(f"./rozwiazania/pliki_informacje/{pl_informacje}", "w")
    if sciezka == "":
        i1.write("-1")
        i1.close()
    else:
        i1.write(f"{ileRuchow(sciezka)}\n")
        i1.write(f"{stany_odwiedzone}\n")
        i1.write(f"{stany_przetworzone}\n")
        i1.write(f"{najwieksza_glebokosc_na_jaka_zeszlismy}\n")
        i1.write(f"{czas_koncowy}")
        i1.close()


def wylicz(parametr_1, parametr_2):
    if parametr_2 == "hamm":
        return astr("hamm")
    elif parametr_2 == "manh":
        return astr("manh")
    elif parametr_1 == "bfs":
        return bfs(parametr_2)
    elif parametr_1 == "dfs":
        return dfs(parametr_2)


### "MAIN" ###:
wczytaj_uklad_poczatkowy()

czasRozpoczecia = time.time_ns()
wylicz(strategia, porzadek_przeszukiwania_lub_heurystyka)
czas_koncowy = wyliczanieCzasuRozwiazania(czasRozpoczecia)
zapisz_do_plikow(plik_koncowy, plik_informacje)

### DEBUGGING ###

print(wyliczanieCzasuRozwiazania(czasRozpoczecia))
print(sciezka)
print(f"ilość ruchów: {ileRuchow(sciezka)}")
print(f"największa głębokość rekursji (na jaką zeszliśmy): {najwieksza_glebokosc_na_jaka_zeszlismy}")
print(f"stany odwiedzone: {stany_odwiedzone}")
print(f"stany przetworzone: {stany_przetworzone}")
