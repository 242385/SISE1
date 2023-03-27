class Board:
    def __init__(self, w, k, tab):
        self.tab = tab
        self.depth = 1
        self.metric = "hamm"
        self.w = w
        self.k = k

    def __lt__(self, obj):
        if self.metric == "hamm":
            return (self.hamming()) > (obj.hamming())
        else:
            return (self.manhattan()) > (obj.manhattan())

    def hamming(self):
        wynik = 0
        for i in range(0, self.k * self.w):
            if self.tab[i] == i + 1 and self.tab[i] != 0:
                wynik += 1
        return wynik - self.depth

    def manhattan(self):
        wynik = 0
        for i in range(0, self.w * self.k):
            if self.tab[i] != 0:
                x1 = int(i % self.w)
                y1 = int(i / self.w)
                x2 = int((int(self.tab[i]) - 1) % self.w)
                y2 = int((int(self.tab[i]) - 1) / self.w)
                wynik = wynik + abs(x1 - x2) + abs(y1 - y2)
        return wynik - self.depth
