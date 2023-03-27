import matplotlib.pyplot as plt
import chardet as chardet
import numpy as np

with open('./dane_wszystkie.csv', 'rb') as f:
    enc = chardet.detect(f.read())

with open("./dane_wszystkie.csv", 'r', encoding=enc['encoding']) as csvfile:
    dataframe = list()
    i = 0
    for line in csvfile.readlines():
        array = line.split()
        dataframe.append(array)

        i += 1


def wykresOgolny(dane_wszystkie, numer_kryterium, nazwa_kryterium, czy_logarytm):
    suma_dfs = []
    suma_bfs = []
    suma_astr = []

    bfs = [0.0] * 7
    dfs = [0.0] * 7
    astr = [0.0] * 7

    srednia_dfs = []
    srednia_bfs = []
    srednia_astr = []

    for i in range(0, 8):
        suma_astr.append(0.0)
        suma_bfs.append(0.0)
        suma_dfs.append(0.0)

    for d in dane_wszystkie:
        if d[2] == 'dfs':
            suma_dfs[int(d[0])] += float(d[numer_kryterium + 3])
            suma_dfs[0] = suma_dfs[0] + 1.0
            dfs[int(d[0]) - 1] += 1.0
        if d[2] == 'bfs':
            suma_bfs[int(d[0])] += float(d[numer_kryterium + 3])
            suma_bfs[0] = suma_bfs[0] + 1.0
            bfs[int(d[0]) - 1] += 1.0
        if d[2] == 'astr':
            suma_astr[int(d[0])] += float(d[numer_kryterium + 3])
            suma_astr[0] = suma_astr[0] + 1.0
            astr[int(d[0]) - 1] += 1.0

    for i in range(0, 7):
        srednia_astr.append(suma_astr[i + 1] / astr[i])
        srednia_bfs.append(suma_bfs[i + 1] / bfs[i])
        srednia_dfs.append(suma_dfs[i + 1] / dfs[i])

    x = [1, 2, 3, 4, 5, 6, 7]
    plt.hist([x, x, x],
             weights=[srednia_astr, srednia_bfs, srednia_dfs],
             label=['A*', 'BFS', 'DFS'],
             color=['#2DA02E', '#1E77B4', '#FF7F17'],
             align="mid", bins=np.arange(10) - 0.5)
    plt.title('Ogólne', fontsize=16)
    plt.xlabel('Głębokość rozwiazania', fontsize=12)
    plt.ylabel(nazwa_kryterium, fontsize=12)
    plt.legend(loc='upper left')
    plt.rcParams["figure.figsize"] = (9, 6)
    if czy_logarytm == "log":
        plt.yscale("log")
    plt.xticks(range(8))
    plt.xlim([0, 8])
    plt.show()


def wykresAstr(wszystkie_dane, numer_kryterium, nazwa_kryterium):
    suma_manhattan = []
    suma_hamming = []

    manhattan = [0.0] * 7
    hamming = [0.0] * 7

    srednia_manhattan = []
    srednia_hamming = []

    for i in range(0, 8):
        suma_manhattan.append(0.0)
        suma_hamming.append(0.0)

    for d in wszystkie_dane:
        if d[2] == 'astr':
            if d[3] == 'manh':
                suma_manhattan[int(d[0])] += float(d[numer_kryterium + 3])
                suma_manhattan[0] += 1
                manhattan[int(d[0]) - 1] += 1.0
            if d[3] == 'hamm':
                suma_hamming[int(d[0])] += float(d[numer_kryterium + 3])
                suma_hamming[0] += 1
                hamming[int(d[0]) - 1] += 1.0

    for i in range(0, 7):
        srednia_manhattan.append(suma_manhattan[i + 1] / manhattan[i])
        srednia_hamming.append(suma_hamming[i + 1] / hamming[i])

    x = [1, 2, 3, 4, 5, 6, 7]
    plt.hist([x, x],
             weights=[srednia_manhattan, srednia_hamming],
             label=['Manhattan', 'Hamming'],
             color=['#FF7F17', '#1E77B4'], align="mid", bins=np.arange(10) - 0.5)
    plt.title('A*', fontsize=16)
    plt.xlabel('Głębokość rozwiazania', fontsize=12)
    plt.ylabel(nazwa_kryterium, fontsize=12)
    plt.legend(loc='upper left')
    plt.rcParams["figure.figsize"] = (9, 6)
    plt.xticks(range(8))
    plt.xlim([0, 8])
    if numer_kryterium == 1:
        plt.yticks(np.arange(0, 10, 1))
    elif numer_kryterium == 2:
        plt.yticks(np.arange(0, 26, 5))
    elif numer_kryterium == 3:
        plt.yticks(np.arange(0, 11, 1))
    elif numer_kryterium == 5:
        plt.yticks(np.arange(0.0, 0.6, 0.05))
    plt.show()


def wykresDFS(dane_wszystkie, numer_kryterium, nazwa_kryterium, czy_logarytm):
    suma_RDUL = []
    suma_RDLU = []
    suma_DRUL = []
    suma_DRLU = []
    suma_LUDR = []
    suma_LURD = []
    suma_ULDR = []
    suma_ULRD = []

    srednia_RDUL = []
    srednia_RDLU = []
    srednia_DRUL = []
    srednia_DRLU = []
    srednia_LUDR = []
    srednia_LURD = []
    srednia_ULDR = []
    srednia_ULRD = []

    rdul = [0.0] * 7
    rdlu = [0.0] * 7
    drul = [0.0] * 7
    drlu = [0.0] * 7
    ludr = [0.0] * 7
    lurd = [0.0] * 7
    uldr = [0.0] * 7
    ulrd = [0.0] * 7

    for i in range(0, 8):
        suma_RDUL.append(0.0)
        suma_RDLU.append(0.0)
        suma_DRUL.append(0.0)
        suma_DRLU.append(0.0)
        suma_LUDR.append(0.0)
        suma_LURD.append(0.0)
        suma_ULDR.append(0.0)
        suma_ULRD.append(0.0)

    for d in dane_wszystkie:
        if d[2] == 'dfs':
            if d[3] == 'rdul':
                suma_RDUL[int(d[0])] += float(d[numer_kryterium + 3])
                suma_RDUL[0] += 1
                rdul[int(d[0]) - 1] += 1
            if d[3] == 'rdlu':
                suma_RDLU[int(d[0])] += float(d[numer_kryterium + 3])
                suma_RDLU[0] += 1
                rdlu[int(d[0]) - 1] += 1
            if d[3] == 'drul':
                suma_DRUL[int(d[0])] += float(d[numer_kryterium + 3])
                suma_DRUL[0] += 1
                drul[int(d[0]) - 1] += 1
            if d[3] == 'drlu':
                suma_DRLU[int(d[0])] += float(d[numer_kryterium + 3])
                suma_DRLU[0] += 1
                drlu[int(d[0]) - 1] += 1
            if d[3] == 'ludr':
                suma_LUDR[int(d[0])] += float(d[numer_kryterium + 3])
                suma_LUDR[0] += 1
                ludr[int(d[0]) - 1] += 1
            if d[3] == 'ludr':
                suma_LURD[int(d[0])] += float(d[numer_kryterium + 3])
                suma_LURD[0] += 1
                lurd[int(d[0]) - 1] += 1
            if d[3] == 'uldr':
                suma_ULDR[int(d[0])] += float(d[numer_kryterium + 3])
                suma_ULDR[0] += 1
                uldr[int(d[0]) - 1] += 1
            if d[3] == 'ulrd':
                suma_ULRD[int(d[0])] += float(d[numer_kryterium + 3])
                suma_ULRD[0] += 1
                ulrd[int(d[0]) - 1] += 1

    for i in range(0, 7):
        srednia_RDUL.append(suma_RDUL[i + 1] / rdul[i])
        srednia_RDLU.append(suma_RDLU[i + 1] / rdlu[i])
        srednia_DRUL.append(suma_DRUL[i + 1] / drul[i])
        srednia_DRLU.append(suma_DRLU[i + 1] / drlu[i])
        srednia_LUDR.append(suma_LUDR[i + 1] / ludr[i])
        srednia_LURD.append(suma_LURD[i + 1] / lurd[i])
        srednia_ULDR.append(suma_ULDR[i + 1] / uldr[i])
        srednia_ULRD.append(suma_ULRD[i + 1] / ulrd[i])

    x = [1, 2, 3, 4, 5, 6, 7]
    plt.hist([x, x, x, x, x, x, x, x],
             weights=[srednia_RDLU, srednia_RDUL, srednia_DRUL, srednia_DRLU,
                      srednia_LUDR, srednia_LURD, srednia_ULDR, srednia_ULRD],
             label=['RDLU', 'RDUL', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD'],
             color=['#FF7F17', '#1E77B4', '#2DA02E', '#D62728', '#8C564B', '#9467BD', '#E277C1', '#7F7F7F'],
             align="mid", bins=np.arange(10) - 0.5)
    plt.title('DFS', fontsize=16)
    plt.xlabel('Głębokość rozwiazania', fontsize=12)
    plt.ylabel(nazwa_kryterium, fontsize=12)
    plt.rcParams["figure.figsize"] = (9, 6)
    plt.legend(loc='lower right')
    plt.xticks(range(8))
    plt.xlim([0, 8])
    if numer_kryterium == 1:
        plt.yticks(np.arange(0, 19, 2))
    elif numer_kryterium == 4:
        plt.yticks(np.arange(0, 21, 2))
    if czy_logarytm == "log":
        plt.yscale("log")
    plt.show()


def wykresBFS(dane_wszystkie, numer_kryterium, nazwa_kryterium, czy_logarytm):
    suma_RDUL = []
    suma_RDLU = []
    suma_DRUL = []
    suma_DRLU = []
    suma_LUDR = []
    suma_LURD = []
    suma_ULDR = []
    suma_ULRD = []

    srednia_RDUL = []
    srednia_RDLU = []
    srednia_DRUL = []
    srednia_DRLU = []
    srednia_LUDR = []
    srednia_LURD = []
    srednia_ULDR = []
    srednia_ULRD = []

    rdul = [0.0] * 7
    rdlu = [0.0] * 7
    drul = [0.0] * 7
    drlu = [0.0] * 7
    ludr = [0.0] * 7
    lurd = [0.0] * 7
    uldr = [0.0] * 7
    ulrd = [0.0] * 7

    for i in range(0, 8):
        suma_RDUL.append(0.0)
        suma_RDLU.append(0.0)
        suma_DRUL.append(0.0)
        suma_DRLU.append(0.0)
        suma_LUDR.append(0.0)
        suma_LURD.append(0.0)
        suma_ULDR.append(0.0)
        suma_ULRD.append(0.0)

    for d in dane_wszystkie:
        if d[2] == 'bfs':

            if d[3] == 'rdul':
                suma_RDUL[int(d[0])] += float(d[numer_kryterium + 3])
                suma_RDUL[0] += 1
                rdul[int(d[0]) - 1] += 1
            if d[3] == 'rdlu':
                suma_RDLU[int(d[0])] += float(d[numer_kryterium + 3])
                suma_RDLU[0] += 1
                rdlu[int(d[0]) - 1] += 1
            if d[3] == 'drul':
                suma_DRUL[int(d[0])] += float(d[numer_kryterium + 3])
                suma_DRUL[0] += 1
                drul[int(d[0]) - 1] += 1
            if d[3] == 'drlu':
                suma_DRLU[int(d[0])] += float(d[numer_kryterium + 3])
                suma_DRLU[0] += 1
                drlu[int(d[0]) - 1] += 1
            if d[3] == 'ludr':
                suma_LUDR[int(d[0])] += float(d[numer_kryterium + 3])
                suma_LUDR[0] += 1
                ludr[int(d[0]) - 1] += 1
            if d[3] == 'ludr':
                suma_LURD[int(d[0])] += float(d[numer_kryterium + 3])
                suma_LURD[0] += 1
                lurd[int(d[0]) - 1] += 1
            if d[3] == 'uldr':
                suma_ULDR[int(d[0])] += float(d[numer_kryterium + 3])
                suma_ULDR[0] += 1
                uldr[int(d[0]) - 1] += 1
            if d[3] == 'ulrd':
                suma_ULRD[int(d[0])] += float(d[numer_kryterium + 3])
                suma_ULRD[0] += 1
                ulrd[int(d[0]) - 1] += 1

    for i in range(0, 7):
        srednia_RDUL.append(suma_RDUL[i + 1] / rdul[i])
        srednia_RDLU.append(suma_RDLU[i + 1] / rdlu[i])
        srednia_DRUL.append(suma_DRUL[i + 1] / drul[i])
        srednia_DRLU.append(suma_DRLU[i + 1] / drlu[i])
        srednia_LUDR.append(suma_LUDR[i + 1] / ludr[i])
        srednia_LURD.append(suma_LURD[i + 1] / lurd[i])
        srednia_ULDR.append(suma_ULDR[i + 1] / uldr[i])
        srednia_ULRD.append(suma_ULRD[i + 1] / ulrd[i])

    x = [1, 2, 3, 4, 5, 6, 7]
    plt.hist([x, x, x, x, x, x, x, x],
             weights=[srednia_RDLU, srednia_RDUL, srednia_DRUL, srednia_DRLU,
                      srednia_LUDR, srednia_LURD, srednia_ULDR, srednia_ULRD],
             label=['RDLU', 'RDUL', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD'],
             color=['#1E77B4', '#FF7F17', '#2DA02E', '#D62728', '#8C564B', '#9467BD', '#E277C1', '#7F7F7F'],
             align="mid", bins=np.arange(10) - 0.5)
    plt.title('BFS', fontsize=16)
    plt.xlabel('Głębokość rozwiazania', fontsize=12)
    plt.ylabel(nazwa_kryterium, fontsize=12)
    plt.rcParams["figure.figsize"] = (9, 6)
    plt.legend(loc='upper left')
    plt.xticks(range(8))
    plt.xlim([0, 8])
    if czy_logarytm == "log":
        plt.yscale("log")
    plt.show()


def test():
    data = np.random.randint(0, 10, 1000)
    bins = np.arange(11) - 0.5
    plt.hist(data, bins)
    plt.rcParams["figure.figsize"] = (9, 6)
    plt.show()


test()
wykresOgolny(dataframe, 1, "Długość rozwiązania", "nie")
wykresAstr(dataframe, 1, "Długość rozwiązania")
wykresBFS(dataframe, 1, "Długość rozwiązania", "nie")
wykresDFS(dataframe, 1, "Długość rozwiązania", "nie")

wykresOgolny(dataframe, 2, "Liczba stanów odwiedzonych", "log")
wykresAstr(dataframe, 2, "Liczba stanów odwiedzonych")
wykresBFS(dataframe, 2, "Liczba stanów odwiedzonych", "log")
wykresDFS(dataframe, 2, "Liczba stanów odwiedzonych", "log")

wykresOgolny(dataframe, 3, "Liczba stanów przetworzonych", "log")
wykresAstr(dataframe, 3, "Liczba stanów przetworzonych")
wykresBFS(dataframe, 3, "Liczba stanów przetworzonych", "nie")
wykresDFS(dataframe, 3, "Liczba stanów przetworzonych", "log")

wykresOgolny(dataframe, 4, "Maksymalna osiągnięta głębokość rekursji", "nie")
wykresAstr(dataframe, 4, "Maksymalna osiągnięta głębokość rekursji")
wykresBFS(dataframe, 4, "Maksymalna osiągnięta głębokość rekursji", "nie")
wykresDFS(dataframe, 4, "Maksymalna osiągnięta głębokość rekursji", "nie")

wykresOgolny(dataframe, 5, "Czas trwania procesu obliczeniowego (ms)", "log")
wykresAstr(dataframe, 5, "Czas trwania procesu obliczeniowego (ms)")
wykresBFS(dataframe, 5, "Czas trwania procesu obliczeniowego (ms)", "nie")
wykresDFS(dataframe, 5, "Czas trwania procesu obliczeniowego (ms)", "nie")
