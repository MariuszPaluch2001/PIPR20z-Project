
from gracz import Gracz
from plansza import Plansza
from gracz import GlupiutkiKomputer
from gracz import LudzkiGracz
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

        while (self.plansza.sprawdz_czy_zwyciezca is not None):
            self.plansza.rysujPlansze()
            plansza_kopia = copy.deepcopy(self.plansza)

            if len(plansza_kopia.mozliwe_ruchy()) == 0:
                self.wynik = self.plansza.get_przeciwnik().kolor
                break

            #print("****Teraz gracz " + p.get_gracz_wykonujacy_ruch().get_kolor_string())
            ruch = self.plansza.get_gracz_wykonujacy_ruch().zwroc_ruch(plansza_kopia)
            self.plansza.wykonaj_wskazane_ruchy(ruch)

            if len(ruch) <= 2: # co najmniej dwa przesuniecia oznaczaja bicie
                self.ilosc_kolejnych_rund_bez_bic += 1
                if self.ilosc_kolejnych_rund_bez_bic >= 2*15:
                    self.wynik = 0
                    break
            else:
                self.ilosc_kolejnych_rund_bez_bic = 0

            #p.rysujPlansze()
            self.plansza.kolejka += 1

        if (self.wynik == 0):
            print("Gra zakonczyla sie REMISEM")
        else:
              if (self.wynik == Gracz.WHITE):
                  print("Zwyciezyl gracz bialy" )
              elif (self.wynik == Gracz.BLACK):
                print("Zwyciezyl gracz czarny" )

        print("Ilosc kolejek " + str(self.plansza.kolejka))
        return self.wynik


print("*"*15 +  "Witamy w warcabach ... " + "*"*15 )
rodzaj_gracza1 = int(input("Wprowadz typ gracza1 (czarny) " + "\n".join([ "\n[1]\t Czlowiek", "[2]\t Komputer"]) + "\n"))
rodzaj_gracza2 = int(input("Wprowadz typ gracza2 (bialy) " + "\n".join([ "\n[1]\t Czlowiek", "[2]\t Komputer"])+ "\n"))

gracz1 = LudzkiGracz() if rodzaj_gracza1 == 1 else GlupiutkiKomputer()
gracz2 = LudzkiGracz() if rodzaj_gracza2 == 1 else GlupiutkiKomputer()
print (gracz1.name())
print (gracz2.name())
w = Warcaby(gracz1, gracz2)
w.graj()

