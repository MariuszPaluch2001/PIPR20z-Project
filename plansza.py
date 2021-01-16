#from copy import deepcopy
#from gracz import Gracz
#from drzewo import WezelDrzewa 
#from pionek import Pionek


from drzewo import WezelDrzewa
from gracz import Gracz
from pionek import Pionek
import logging
import copy


import logging
#root_logger.basicConfig(filename='warcaby.log', level=root_logger.DEBUG)

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) # or whatever
handler = logging.FileHandler('warcaby-utf8.log', 'w', 'utf-8') # or whatever
handler.setFormatter(logging.Formatter('%(name)s %(message)s')) # or whatever
root_logger.addHandler(handler)

class Plansza(object):
    WYNIK_WYGRAL_CZARNY = 1
    WYNIK_WYGRAL_BIALY = 2
    WYNIK_REMIS = 0

    def __init__(self, wysokosc=8, szerokosc=8, bialy_gracz = Gracz() , czarny_gracz = Gracz(), kolejka = 1):
        """
            Tworzy plansze
        """
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc

        # Lista z pionkami obu graczy
        self.czarne_pionki = []
        self.biale_pionki = []
        self.pionki = []

        self.pionki = [self.biale_pionki, self.czarne_pionki]

        # aktualna plansza ze znakami do odrysowania
        self.stanPlanszy = [[' '] * self.szerokosc for x in range(self.wysokosc)]
        self.slownikPozycji= {}

        self.set_bialy_gracz(bialy_gracz)
        self.set_czarny_gracz(czarny_gracz)
        self.kolejka = kolejka
        self.wynik = None

    def get_gracz_wykonujacy_ruch(self):
        if self.kolejka % 2 != 0 :
            #print("Kolejka .... " + str(self.kolejka) + " " + self.czarny_gracz.get_kolor_string())
            return self.czarny_gracz
        else:
            #print("Kolejka .... " + str(self.kolejka) + " " + self.bialy_gracz.get_kolor_string())
            return self.bialy_gracz

    def get_przeciwnik(self):
        if self.kolejka % 2 == 0 :
            return self.czarny_gracz
        else:
            return self.bialy_gracz

    def set_bialy_gracz(self, gracz):
        self.bialy_gracz = gracz
        self.bialy_gracz.ustaw_bialy_kolor()
        self.bialy_gracz.pionki = self.biale_pionki

    def set_czarny_gracz(self, gracz):
        self.czarny_gracz = gracz
        self.czarny_gracz.ustaw_czarny_kolor()
        self.czarny_gracz.pionki = self.czarne_pionki

    def get_biale_pionki(self):
        return self.biale_pionki

    def zwyciezca(self):
        gracz = self.get_gracz_wykonujacy_ruch()
        if len(gracz.pionki) == 0 or self.mozliwe_ruchy() == 0:
           self.wynik = (Plansza.WYNIK_WYGRAL_CZARNY if gracz.jest_koloru_bialego() else Plansza.WYNIK_WYGRAL_BIALY)
           return self.get_przeciwnik() 

        #if len(self.biale_pionki) == 0:
        #    return Plansza.WYNIK_WYGRAL_CZARNY
        #elif len(self.czarne_pionki) == 0:
        #    return Plansza.WYNIK_WYGRAL_BIALY

        #plansza_kopia = copy.deepcopy(self)
        #gracz_wykonujacy_ruch = plansza_kopia.get_gracz_wykonujacy_ruch()
        #if len(plansza_kopia.mozliwe_ruchy()) == 0: 
        #    plansza_kopia.kolejka += 1
        #    if len(plansza_kopia.mozliwe_ruchy()) != 0:
        #        self.wynik = (Plansza.WYNIK_WYGRAL_CZARNY if gracz_wykonujacy_ruch.jest_koloru_bialego() else Plansza.WYNIK_WYGRAL_BIALY)
        #    else:
        #        self.wynik = Plansza.WYNIK_REMIS
       # 
        #return self.wynik

    #do inicjalizacji
    def wstaw_pionek_na_plansze(self, pionek):
        if pionek.gracz.jest_koloru_bialego():
            self.biale_pionki.append(pionek)
            self.slownikPozycji[pionek.get_pozycja()] = pionek
        elif pionek.gracz.jest_koloru_czarnego():
            self.czarne_pionki.append(pionek)
            self.slownikPozycji[pionek.get_pozycja()] = pionek

    def usun_pionek_z_planszy(self, pionek):
        root_logger.debug("Usuwam pionek na pozycji " + self.pozycja_to_str(pionek.pozycja))
        del self.slownikPozycji[pionek.get_pozycja()]
        if pionek.gracz.jest_koloru_bialego():
            self.biale_pionki.remove(pionek)
        elif pionek.gracz.jest_koloru_czarnego():
            self.czarne_pionki.remove(pionek)

    """
       Przesun pionek na pozycje docelowa. Zwroc True jesli ruch jest promocja i konczy dalszy ruch
    """
    def przesun_pionek_na_dana_pozycje(self, pionek, pozycja_docelowa):
        #print("Przesuwam pionek na planszy " + str(pionek.pozycja) + " do " + str(pozycja_docelowa))
        del self.slownikPozycji[pionek.get_pozycja()]
        self.slownikPozycji[pozycja_docelowa] = pionek
        pionek.set_pozycja(pozycja_docelowa)
        if (pozycja_docelowa[1] == self.wysokosc-1 and pionek.gracz.jest_koloru_bialego()) or  (pozycja_docelowa[1] == 0 and pionek.gracz.jest_koloru_czarnego()):

            # Watpliwosc, promocja damki do pionka konczy ruch. A co jesli jest juz damka ?
            # Zakladam ze ograniczenia promocji nie obowiazuja gdy pionek jest juz damka
            if pionek.jest_damka == False:
                pionek.jest_damka = True
                return True





    def zainicjalizuj_plansze(self):

        for i in range(self.szerokosc):
            self.wstaw_pionek_na_plansze(Pionek(self.bialy_gracz, (i, (i+1)%2)))
            self.wstaw_pionek_na_plansze(Pionek(self.czarny_gracz, (i, self.wysokosc - (i%2) - 1)))

        for i in range(4):
            self.wstaw_pionek_na_plansze(Pionek(self.czarny_gracz, (i*2, self.wysokosc - 3)))
            self.wstaw_pionek_na_plansze(Pionek(self.bialy_gracz, (i*2+1, 2)))

        # self.bialy_gracz.set_pionki(self.biale_pionki)
        # self.czarny_gracz.set_pionki(self.czarne_pionki)


    """
        Aktualizuj stanPlanszy uwzgledniajac pozycje bialych i czarnych pinkow
    """
    def zaktualizujStanPlanszy(self):

        for i in range(self.szerokosc):
            for j in range(self.wysokosc):
                self.stanPlanszy[i][j] = " "

        for pionek in  [item for sublist in self.pionki for item in sublist]: #iteruj po splaszczonej liscie z wszystkimi pionkami
            self.stanPlanszy[pionek.get_pozycja()[1]][pionek.get_pozycja()[0]] = pionek.get_znak_pionka()

    """ funkcja pomocznicza """
    def pozycja_to_str(self, pozycja):
        return (str(chr(pozycja[1]+65)) +  str(pozycja[0]))

    """ funkcja pomocznicza """
    def stan_ilosciowy_planszy(self):
        return "Czarne: " + str(len(self.czarne_pionki)) + ',' + str(len(self.czarny_gracz.pionki)) + ", Biale: " + str(len(self.biale_pionki)) + ',' + str(len(self.bialy_gracz.pionki)) + " slownik pozycji " + str(len(self.slownikPozycji))

    #dodatkowa walidacja, ( kiedy kiedy bedzie dzielic moduly )
    def wykonaj_pojedynczy_ruch(self, ruch_z, ruch_do):
        pionek = self.slownikPozycji[ruch_z]
        #print("Wykonaj pojedynczy ruch " + str(ruch_z) + " do " + str(ruch_do) + " pionkiem o kolorze " +  pionek.gracz.get_kolor_string() )


        if (abs(ruch_z[0] - ruch_do[0]) == 2 and abs(ruch_z[1] - ruch_do[1]) == 2):
            poz_pomiedzy = (min(ruch_z[0], ruch_do[0]) + 1, min(ruch_z[1], ruch_do[1]) + 1)
            pionek_na_pozycji_pomiedzy = self.slownikPozycji.get(poz_pomiedzy)
            if pionek_na_pozycji_pomiedzy.gracz.get_kolor_string() == pionek.gracz.get_kolor_string(): # jesli ten sam gracz
                raise ValueError("Tu, na pozycji " + str(poz_pomiedzy) + " stoi pionek gracza o kolorze " + pionek_na_pozycji_pomiedzy.gracz.get_kolor_string())
            else:
                self.usun_pionek_z_planszy(pionek_na_pozycji_pomiedzy)
        #        return self.przesun_pionek_na_dana_pozycje(pionek,ruch_do)
        #else:

        return self.przesun_pionek_na_dana_pozycje(pionek,ruch_do)


    def wykonaj_wskazane_ruchy(self, sciezka_ruchu):
        for i in range(len(sciezka_ruchu)-1):
            self.wykonaj_pojedynczy_ruch(sciezka_ruchu[i], sciezka_ruchu[i+1])
        return

    #sprawdza czy podana pozycja istnieje na planszy
    def sprwadz_czy_pozycja_na_planszy(self, pozycja):
        if pozycja[0] < 0 or pozycja[0] >= self.szerokosc or pozycja[1] < 0 or pozycja[1]  >= self.wysokosc:
                return False
        return True


    """
    Ta metoda na potrzeby generowania mozliwych ruchow modyfikuje stan planszy
    """
    def generuj_mozliwe_ruchy(self, pozycja_startowa, czy_poprzedni_ruch_byl_biciem, drzewo_obowiazkowych_bic, lista_mozliwych_ruchow):
        root_logger.debug("generuj_mozliwe_ruchy z " + str(pozycja_startowa))
        root_logger.debug("GENERUJ z " + str(self.pozycja_to_str(pozycja_startowa)))
        pionek = self.slownikPozycji.get(pozycja_startowa)
        #nie uzywac pionek get.get_pozycja() tylko pozycja_startowa, bo inaczej bedzie caly czas taka sama
        for ruch in pionek.get_wektory_ruchu():
            root_logger.debug("Przetwarzam sciezke od " + self.pozycja_to_str(pozycja_startowa) + " i ruch o wektor " + str(ruch) + ", stan planszy " + self.stan_ilosciowy_planszy())

            pozycja_do = (pozycja_startowa[0] + ruch[0], pozycja_startowa[1] + ruch[1])

            if not self.sprwadz_czy_pozycja_na_planszy(pozycja_do): # nie uwzgledniaj ruchow wychodzacych poz plansze
                root_logger.debug("     Ruch poza plansza")
                continue

            # sprwadz czy na danej pozycji stoi pionek i kto jest wlascicelem
            if self.slownikPozycji.get(pozycja_do) is not None:
                pionek_na_pozycji_do = self.slownikPozycji[pozycja_do]
                if pionek_na_pozycji_do.gracz == self.get_gracz_wykonujacy_ruch(): # jesli gracz to pomic
                    root_logger.debug("     Tu stoi pionek gracza")
                    continue

                # mamy potencjalne bicie, sprawdzamy czy pole za pionkiem jest wolne
                pozycja_po_biciu = (pozycja_do[0] + ruch[0], pozycja_do[1] + ruch[1])


                # if poprzednia_pozycja == pozycja_po_biciu:
                #     root_logger.debug("Byłem już na tej pozycji")
                #     continue

                if not self.sprwadz_czy_pozycja_na_planszy(pozycja_po_biciu): # nie uwzgledniaj ruchow wychodzacych poz plansze
                    root_logger.debug("     Bicie wychodzi poza plansze")
                    continue

                if self.slownikPozycji.get(pozycja_po_biciu) is not None:
                    root_logger.debug("     Za bitym pionkiem stoi inny pionek")
                    continue


                root_logger.debug("Mamy bicie, a nastepna mozliwa pozycja to " + self.pozycja_to_str(pozycja_po_biciu) )

                # tworzymy drzewo bic z danj pozycji i dodajemy ja jako wierzcholek
                if czy_poprzedni_ruch_byl_biciem is False and drzewo_obowiazkowych_bic is None:
                    root_logger.debug("Tworze korzen drzewa z wartoscia " + str(pozycja_startowa))
                    drzewo_obowiazkowych_bic = WezelDrzewa(pozycja_startowa)

                nowy_wezel_drzewa = WezelDrzewa(pozycja_po_biciu)
                drzewo_obowiazkowych_bic.dodaj_nowy_wezel(nowy_wezel_drzewa)

                self_copy = copy.deepcopy(self)
                #teraz wykonujemy ruch ( modifukujemy stan planszy !)
                #musimy to zrobic aby uniknac scenariusza zapetlenia damki
                ruch_zakonczony_promocja = self_copy.wykonaj_pojedynczy_ruch(pozycja_startowa, pozycja_po_biciu)
                
                if ruch_zakonczony_promocja != True:
                    #musimy rekurencyjnie zbudowac drzewo dalszych mozliwych bic
                    #oczywiscie na kopii zeby 'wyluskac' wszystkie sciezki bic
                    #self_copy = copy.deepcopy(self)
                    self_copy.generuj_mozliwe_ruchy(pozycja_po_biciu, True, nowy_wezel_drzewa, [])


            else: # nie ma tam innego pionka na pozycji_do
                if czy_poprzedni_ruch_byl_biciem is True:
                    root_logger.debug("     To pole jest wolne ale bylo juz bicie")

                if czy_poprzedni_ruch_byl_biciem is not True:
                   root_logger.debug("      Pole jest wolne, ruch bez bicia")
                   lista_mozliwych_ruchow.append([pozycja_startowa, pozycja_do])

        # print("Zwracam drzezwo obowizakowych bic o rozmiarze dzieci " + str(len(drzewo_obowiazkowych_bic.wezly_potomne)))
        # # for node in drzewo_obowiazkowych_bic.wezly_potomne:
        # #     print(str(node.wartosc))
        # # print(drzewo_obowiazkowych_bic.generujSciezki(drzewo_obowiazkowych_bic))
        return drzewo_obowiazkowych_bic


    def mozliwe_ruchy(self, gracz = None):

        if gracz is None:
            gracz = self.get_gracz_wykonujacy_ruch()

        # Trzewa stworzyc kopie planszy, bo inaczej nie mozna generowac ruchow
        sciezki_obowiazkowych_bic = []
        mozliwe_ruchy = []
        #print("---Teraz gracz " + self.get_gracz_wykonujacy_ruch().get_kolor_string())
        for pionek in gracz.pionki:
            self_copy = copy.deepcopy(self)
            pozycja_startowa = pionek.get_pozycja()
            drzewo_obowiazkowych_bic = None

            drzewo_obowiazkowych_bic = self_copy.generuj_mozliwe_ruchy(pozycja_startowa, False,  drzewo_obowiazkowych_bic, mozliwe_ruchy)

            if drzewo_obowiazkowych_bic is not None and drzewo_obowiazkowych_bic.puste() == False: # jesli obowizkowe bicia

                sciezki_bic_z_pozycji_startowej = drzewo_obowiazkowych_bic.generujSciezki(drzewo_obowiazkowych_bic)
                sciezki_obowiazkowych_bic.extend(sciezki_bic_z_pozycji_startowej)

        if len(sciezki_obowiazkowych_bic) != 0:
            return sciezki_obowiazkowych_bic
        else :
            return mozliwe_ruchy


    def rysujPlansze(self):
        """
            Narysuj plansze w UTF-8
        """

        # Updates Game board
        self.zaktualizujStanPlanszy()
        lines = []
        lines.append('  ')
        # This prints the numbers at the top of the Game Board
        lines.append('      ' + '   '.join(map(str, list(range(self.szerokosc)))))
        # Prints the top of the gameboard in unicode
        lines.append('    ╭' + ('───┬' * (self.szerokosc-1)) + '───╮')

        # Print the boards rows
        for num, row in enumerate(self.stanPlanszy[:-1]):
            lines.append(chr(num+65) + '  ' + ' │ ' + ' │ '.join(row) + ' │') #+  str(num )
            lines.append('    ├' + ('───┼' * (self.szerokosc-1)) + '───┤')

        #Print the last row
        lines.append(chr(self.wysokosc+64) + '  ' + ' │ ' + ' │ '.join(self.stanPlanszy[-1]) + ' │') #+ str(num + 1) +

        # Prints the final line in the board
        lines.append('    ╰' + ('───┴' * (self.szerokosc-1)) + '───╯')
        root_logger.debug('\n'.join(lines))
        print('\n'.join(lines))
