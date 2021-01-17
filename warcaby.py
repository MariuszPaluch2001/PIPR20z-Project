from gracz import Gracz
from plansza import Plansza
from gracz import GlupiutkiKomputer
from gracz import MadryKomputer
from gracz import LudzkiGracz
from ai import AI
from pomocnicze import *
import copy


class Warcaby():


    def __init__(self, gracz1, gracz2):
        self.runda = 1
        self.wynik = None
        self.ilosc_kolejnych_rund_bez_bic = 0
        self.gracz1 = gracz1
        self.gracz2 = gracz2
        self.plansza = Plansza()
        self.plansza.set_czarny_gracz(gracz1)
        self.plansza.set_bialy_gracz(gracz2)
        self.plansza.zainicjalizuj_plansze()

    """
        Metoda rozpoczynajaca gre w Warcaby
        Zwraca numer gracza bedacego zwyciezca (1 lub 2) lub 0 gdy remis
    """
    def graj(self):
        self.plansza.rysujPlansze()
        while (self.plansza.zwyciezca() is None):
            #self.plansza.rysujPlansze()
            plansza_kopia = copy.deepcopy(self.plansza)

            ruch = self.plansza.get_gracz_wykonujacy_ruch().zwroc_ruch(plansza_kopia)
            print(sciezka_to_str(ruch))
            self.plansza.wykonaj_wskazane_ruchy(ruch)

            #if  len(ruch) <= 2 and abs(ruch[1][0] - ruch[0][0]) != 2: # w sciezce ruchu nie ma wieloktornego bicia albo pojedynczego
            #    self.ilosc_kolejnych_rund_bez_bic += 1
            #    if self.ilosc_kolejnych_rund_bez_bic >= 2*15:
            #        self.wynik = 0
            #        break
            #else:
            #    self.ilosc_kolejnych_rund_bez_bic = 0

            self.plansza.rysujPlansze()
            self.plansza.kolejka += 1

            #print(self.plansza.get_gracz_wykonujacy_ruch().get_kolor_string() + " " + str(self.plansza.kolejka) + " " + str(NegamaxAlgorytm().funkcja_oceniajaca(self.plansza)))

        self.plansza.rysujPlansze()
        if (self.plansza.wynik == Plansza.WYNIK_WYGRAL_BIALY):
            print("Zwyciezyl gracz bialy" )
        elif (self.plansza.wynik == Plansza.WYNIK_WYGRAL_CZARNY):
            print("Zwyciezyl gracz czarny")
        elif (self.plansza.wynik == Plansza.WYNIK_REMIS):
            print("Gra zakonczyla sie remisem")

       

        print("Ilosc kolejek " + str(self.plansza.kolejka))
        return self.plansza.wynik



print("*"*15 +  "Witamy w warcabach ... " + "*"*15 )
rodzaj_gracza1 = int(input("Wprowadz typ gracza1 (czarny) " + "\n".join([ "\n[1]\t Czlowiek", "[2]\t Komputer"]) + "\n"))
rodzaj_gracza2 = int(input("Wprowadz typ gracza2 (bialy) " + "\n".join([ "\n[1]\t Czlowiek", "[2]\t Komputer"])+ "\n"))

gracz1 = LudzkiGracz() if rodzaj_gracza1 == 1 else GlupiutkiKomputer()
gracz2 = LudzkiGracz() if rodzaj_gracza2 == 1 else MadryKomputer()
#gracz1 = LudzkiGracz() if rodzaj_gracza1 == 1 else MadryKomputer()
print ("Gracz1: " + gracz1.name())
print ("Gracz2: " + gracz2.name())
w = Warcaby(gracz1, gracz2)
w.graj()

