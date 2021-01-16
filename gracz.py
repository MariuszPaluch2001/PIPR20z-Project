
import random
#from copy import deepcopy
import copy
from ai import AI
from pomocnicze import *

#klasa gracz nie powinna przechowywac informacji o pionkach
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
        i=0
        for sciezka in mozliwe_ruchy:
            str_sciezka = []
            # print("Ruch")
            for ruch in sciezka:
                    str_sciezka.append(str(chr(ruch[1]+65)) +  str(ruch[0]))

            print( '[' + str(i)  + ']\t\t' + '  ->  '.join(str_sciezka))
            i += 1


class LudzkiGracz(Gracz):

    def name(self):
        return "Ludzki gracz"

    def zwroc_ruch(self, plansza):
        # obowiazkowe_bicia = []
        mozliwe_ruchy = []

        print("Dostepne ruchy")
        i = 0

        mozliwe_ruchy = plansza.mozliwe_ruchy()
        for sciezka in mozliwe_ruchy:
            str_sciezka = []
            # print("Ruch")
            for ruch in sciezka:
                    str_sciezka.append(str(chr(ruch[1]+65)) +  str(ruch[0]))

            print( '[' + str(i)  + ']\t\t' + '  ->  '.join(str_sciezka))
            i += 1

        indeks_ruchu = int(input("Wprowadz number ruchu ktory chcesz wykonac np. 1: "))
        return mozliwe_ruchy[indeks_ruchu]

# Trzeba zaimplementowac algorytm minikasowy
class GlupiutkiKomputer(Gracz):

    def name(self):
        return "Glupioutki komp"


    def zwroc_ruch(self, plansza):
        # glupiutki, bo zawsze wybierze pierwszy ruch
        indeks_ruchu = random.randint(0, len(plansza.mozliwe_ruchy())-1)
        return plansza.mozliwe_ruchy()[indeks_ruchu]
        #return plansza.mozliwe_ruchy(self)[len(plansza.mozliwe_ruchy(self))-1]

class MadryKomputer(Gracz):
    def name(self):
        return "Madry komputer (negamax)"

    def zwroc_ruch(self, plansza):
        # glupiutki, bo zawsze wybierze pierwszy ruch

        ai = AI(plansza, 4)
        #kopia = copy.deepcopy(plansza)
        kopia = plansza
        (najlepsza_plansza, najlepsza_ocena, najlepsza_sciezka) = ai.negamax(ai.startowa_plansza, ai.maksymalna_glebokosc)

        print(najlepsza_sciezka) 
        #print("Gracz " + self.name + " wykonuje ruch: ")
        #for ruch in najlepsza_sciezka:
        print("Najsciezka " + sciezka_to_str(najlepsza_sciezka))
        return najlepsza_sciezka

