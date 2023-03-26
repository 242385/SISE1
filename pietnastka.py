# Import, system
import sys
import re
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
glebokosc_rekursji = 1
stany_odwiedzone = 0
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
    print("test")


def generuj_kroki():
    print("test")


def dfs(porzadek):
    global stos_ruchow
    wynik = tuple()
    poziomy_rekursji = {plansza: 1}

    def visit():
        global glebokosc_rekursji
        if not stos_ruchow:
            return tuple()
        zdjety = stos_ruchow.pop()
        oznacz_jako_odwiedzony(zdjety)
        glebokosc_rekursji = poziomy_rekursji[zdjety] + 1
        if glebokosc_rekursji >= maks_glebokosc_rekursji_dfs:
            for s in znajdz_sasiadow(zdjety):
                oznacz_jako_odwiedzony(s)
        for s in znajdz_sasiadow(zdjety):
            if not czy_odwiedzono(s) and len(znajdz_sasiadow(zdjety)) > 1:
                stos_ruchow.append(s)
                poziomy_rekursji[s] = glebokosc_rekursji
        # print(f"{zdjety} | {glebokosc_rekursji}")
        if zdjety == tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]):
            nonlocal wynik
            wynik = zdjety
        visit()

    stos_ruchow.append(plansza)
    visit()
    return wynik


def hamming(board):
    wynik = 0
    for i in range(0, k * w):
        if board[i] == str(i + 1) and board[i] != 0:
            wynik = wynik + 1
    return wynik + glebokosc_rekursji


def manhattan(board):
    wynik = 0
    for i in range(0, w * k):
        if board[i] != 0:
            x1 = i % board[i]
            y1 = i / board[i]
            x2 = board[i] - 1 % board[i]
            y2 = board[i] - 1 / board[i]
            wynik = wynik + abs(x1 - x2) + abs(y1 - y2)
    return wynik + glebokosc_rekursji


def astr_algorytm(heurystyka, tempPlansza):
    global glebokosc_rekursji
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

    glebokosc_rekursji += 1

    if heurystyka == 'manh':
        plansze.sort(key=manhattan)
    elif heurystyka == 'hamm':
        plansze.sort(key=hamming)

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
    return len(ciag_ruchow)


def glebokoscRekursji(glebokosc_rekursji):
    return glebokosc_rekursji - 1  # do logiki startowe jest 1, do naszych danych wyjsciowych -> 0


def iloscStanowPrzetworzonych(stany_przetworzone):
    return stany_przetworzone


def iloscStanowOdwiedzonych(plansze):
    return len(plansze)


### "MAIN" ###:
wczytaj_uklad_poczatkowy()
# print(dfs("URDL"))

czasRozpoczecia = time.time_ns()
astr("hamm")
print("")
czas_rozwiazania(czasRozpoczecia)
printujRuchy(ciag_ruchow)
print(ileRuchow(ciag_ruchow))
print(glebokoscRekursji(glebokosc_rekursji))
print(iloscStanowPrzetworzonych(stany_przetworzone))
print(iloscStanowOdwiedzonych(plansze))
