from gracz import Gracz
from plansza import Plansza
from gracz import InteligentyKomputer
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
        wynik = None
        while (wynik == None):
            plansza_kopia = copy.deepcopy(self.plansza)

            ruch = self.plansza.get_gracz_wykonujacy_ruch().zwroc_ruch(plansza_kopia)
            print("Gracz " + self.plansza.get_gracz_wykonujacy_ruch().get_kolor_string() + " : " + sciezka_to_str(ruch))
            self.plansza.wykonaj_wskazane_ruchy(ruch)

            self.plansza.kolejka += 1
            self.plansza.rysujPlansze()
            wynik = self.plansza.koniec_gry()

        self.plansza.rysujPlansze()

        if wynik == Plansza.WYNIK_REMIS:
            print("Gra zakonczyla sie remisem")
        else:
            print("Zwyciezyl gracz " + wynik.get_kolor_string())

        print("Ilosc kolejek " + str(self.plansza.kolejka))
        return self.plansza.wynik



print("*"*15 +  "Witamy w warcabach angielskich ... " + "*"*15 )
print("Zasady gry znajduja sie w pliku README")

rodzaj_gracza1 = int(input("Wprowadz typ gracza1 (czarny) " + "\n".join([ "\n[1]\t Czlowiek", "[2]\t Komputer"]) + "\n"))
rodzaj_gracza2 = int(input("Wprowadz typ gracza2 (bialy) " + "\n".join([ "\n[1]\t Czlowiek", "[2]\t Komputer"])+ "\n"))

gracz1 = LudzkiGracz() if rodzaj_gracza1 == 1 else InteligentyKomputer()
gracz2 = LudzkiGracz() if rodzaj_gracza2 == 1 else InteligentyKomputer()

if rodzaj_gracza1 == 2:
    gracz1.ustaw_poziom_trudnosci(int(input("Wybierz numer okreslajacy poziom trudnosci gracza1. Zalecany z przedzialu [1-4]\n")))

if rodzaj_gracza2 == 2:
    gracz2.ustaw_poziom_trudnosci(int(input("Wybierz numer okreslajacy poziom trudnosci gracza2. Zalecany z przedzialu [1-4]\n")))

print ("Gracz1: " + gracz1.name())
print ("Gracz2: " + gracz2.name())
w = Warcaby(gracz1, gracz2)
w.graj()

