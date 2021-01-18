class WezelDrzewa(object):
    def __init__(self, wartosc):
        self.wartosc = wartosc
        self.wezly_potomne = []

    def puste(self):
        return len(self.wezly_potomne) == 0 or self.wezly_potomne is None

    def dodaj_nowy_wezel(self, node):
        self.wezly_potomne.append(node)

    def generujSciezki(self, wezel_startowy):
        wszystkie_sciezki = []
        sciezka = []
        self.generujRekursywnieSciezki(wezel_startowy, sciezka, wszystkie_sciezki, 0)
        return wszystkie_sciezki

    def generujRekursywnieSciezki(self, wezel, sciezka, sciezki, dlugosc_sciezki):

        if wezel is None:
            return

        if(len(sciezka) > dlugosc_sciezki):
            sciezka[dlugosc_sciezki] = wezel.wartosc
        else:
            sciezka.append(wezel.wartosc)

        dlugosc_sciezki += 1

        if len(wezel.wezly_potomne) == 0:
            sciezki.append(sciezka.copy())
        else:
            for wezel_potomny in wezel.wezly_potomne:
                self.generujRekursywnieSciezki(wezel_potomny, sciezka.copy(), sciezki, dlugosc_sciezki)
