
import random
from ai import AI
from pomocnicze import sciezka_to_str


class Gracz(object):

    BLACK = 1
    WHITE = 2

    def __init__(self, kolor=None):
        """
            Tworzy gracza
        """
        self.kolor = kolor
        self.pionki = []

    def set_pionki(self, pionki):
        self.pionki = pionki

    def get_logo(self):
        if self.kolor == self.WHITE:
            return '◇'
        elif self.kolor == self.BLACK:
            return '◆'

    def get_kolor_string(self):
        if self.kolor == self.WHITE:
            return "Bialy"
        elif self.kolor == self.BLACK:
            return "Czarny"
        else:
            return "Brak"

    def ustaw_bialy_kolor(self):
        self.kolor = self.WHITE

    def ustaw_czarny_kolor(self):
        self.kolor = self.BLACK

    def jest_koloru_bialego(self):
        return self.kolor == self.WHITE

    def jest_koloru_czarnego(self):
        return self.kolor == self.BLACK

    def get_mnoznik_punktow(self):
        if self.jest_koloru_czarnego():
            return 1
        else:
            return -1

    """
        Zwraca jeden ruch do wykonania przez danego gracza (self)
        Ruch to tablica tupli reprezentujacych ruchy.
        Pojedynczy ruch moze zawierac wiecej niz jedna tuple (bicie)
    """
    def zwroc_ruch(self, plansza):
        return None

    """
        Dla danego gracza zwraca tablice dopuszczalnych ruchow wszystkich
        Jezeli gracz ma bicie lista zawiera tylko bicia.
    """
    # def mozliwe_ruchy(self, plansza):
    #     return plansza.mozliwe_ruchy()

    def wypisz_mozliwe_ruchy(self, plansza):
        mozliwe_ruchy = plansza.mozliwe_ruchy()
        i = 0
        for sciezka in mozliwe_ruchy:
            str_sciezka = []
            # print("Ruch")
            for ruch in sciezka:
                str_sciezka.append(str(chr(ruch[1] + 65)) + str(ruch[0]))

            print('[' + str(i) + ']\t\t' + '  ->  '.join(str_sciezka))
            i += 1


class LudzkiGracz(Gracz):

    def name(self):
        return self.get_logo() + " Ludzki gracz"

    def zwroc_ruch(self, plansza):
        mozliwe_ruchy = []

        print("Dostepne ruchy " + self.get_logo())
        i = 0

        mozliwe_ruchy = plansza.mozliwe_ruchy()
        for sciezka in mozliwe_ruchy:
            print('[' + str(i) + ']\t\t' + sciezka_to_str(sciezka))
            i += 1

        while(True):
            try:
                indeks_ruchu = int(input("Wprowadz number ruchu ktory chcesz wykonac np. 1: "))
                ruch = mozliwe_ruchy[indeks_ruchu]
                return ruch
            except (IndexError, ValueError):
                print("Ups, sprobujmy jeszcze raz")
                continue


"""
  Naiwna implementacja komputerowego gracza zwracajaca pierwszy ruch z drzewa dostepnych ruchow
"""


class LosowyKomputer(Gracz):

    def name(self):
        return "Losowe Ruchy"

    def zwroc_ruch(self, plansza):
        losowy_indeks = random.randint(0, len(plansza.mozliwe_ruchy()) - 1)
        return plansza.mozliwe_ruchy()[losowy_indeks]


"""
  Implementacja madrego gracza oprata na algorytmie negamax
"""


class InteligentnyKomputer(Gracz):

    def __init__(self, kolor=None):
        super()
        self.ai = AI()

    def name(self):
        return super().get_logo() + " AI (poziom : " + str(self.ai.maksymalna_glebokosc) + " )"

    def ustaw_poziom_trudnosci(self, poziom=2):
        self.ai.set_maksymalna_glebokosc(poziom)

    def zwroc_ruch(self, plansza):
        return self.ai.zwroc_ruch(plansza)
