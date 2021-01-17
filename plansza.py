from drzewo import WezelDrzewa
from gracz import Gracz
from pionek import Pionek
from pomocnicze import pozycja_to_str
import logging
import copy


log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler('warcaby-utf8.log', 'w', 'utf-8') 
handler.setFormatter(logging.Formatter('%(name)s %(message)s'))
log.addHandler(handler)


class Plansza(object):

    WYNIK_REMIS = 0

    """
        Tworzy plansze
    """
    def __init__(self, wysokosc=8, szerokosc=8, bialy_gracz=Gracz(), czarny_gracz=Gracz(), kolejka=1):

        self.szerokosc = szerokosc
        self.wysokosc = wysokosc

        # Listy z pionkami obu graczy
        self.czarne_pionki = []
        self.biale_pionki = []
        self.pionki = []

        self.pionki = [self.biale_pionki, self.czarne_pionki]

        # aktualna plansza ze znakami do odrysowania
        self.stanPlanszy = [[' '] * self.szerokosc for x in range(self.wysokosc)]
        # slownik pozycji z pionkami
        self.slownikPozycji = {}

        # gracze
        self.set_bialy_gracz(bialy_gracz)
        self.set_czarny_gracz(czarny_gracz)

        self.kolejka = kolejka
        self.ostatni_ruch_pionkiem = kolejka
        self.wynik = None

    def get_gracz_wykonujacy_ruch(self):
        if self.kolejka % 2 != 0:
            return self.czarny_gracz
        else:
            return self.bialy_gracz

    def get_przeciwnik(self):
        if self.kolejka % 2 == 0:
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

    """
        Funkcja sprawdza czy gra zakonczona zwyciestwem (zwraca zwycieskiego gracza) lub remisem
    """
    def koniec_gry(self):
        gracz = self.get_gracz_wykonujacy_ruch()
        if len(gracz.pionki) == 0 or len(self.mozliwe_ruchy()) == 0:
            return self.get_przeciwnik()
        if self.kolejka - self.ostatni_ruch_pionkiem > 2 * 20:
            return Plansza.WYNIK_REMIS

    """
        Bezwarunkowo usuwa pionek z planszy
    """
    def usun_pionek_z_planszy(self, pionek):
        log.debug("Usuwam pionek na pozycji " + pozycja_to_str(pionek.pozycja))
        del self.slownikPozycji[pionek.get_pozycja()]
        if pionek.gracz.jest_koloru_bialego():
            self.biale_pionki.remove(pionek)
        elif pionek.gracz.jest_koloru_czarnego():
            self.czarne_pionki.remove(pionek)

    """
       Przesun pionek na pozycje docelowa.
       Aktualizuje slownik i koordynaty pionka.
       Dodatkowa dokunje promocji pionka (jesli dotyczy)
       Zwraca True jesli ruch jest promocja (uniemozliwia dalsze ruchy)
    """
    def przesun_pionek_na_dana_pozycje(self, pionek, pozycja_docelowa):
        del self.slownikPozycji[pionek.get_pozycja()]
        self.slownikPozycji[pozycja_docelowa] = pionek
        pionek.set_pozycja(pozycja_docelowa)
        if (pozycja_docelowa[1] == self.wysokosc - 1 and pionek.gracz.jest_koloru_bialego()) or (pozycja_docelowa[1] == 0 and pionek.gracz.jest_koloru_czarnego()):

            # Watpliwosc, promocja damki do pionka konczy ruch.
            # Zakladam ze ograniczenia promocji nie obowiazuja gdy pionek jest juz damka
            if pionek.jest_damka is False:
                pionek.jest_damka = True
                return True

    """
    Metoda przesuwa pionek z polozenia "z" do polozenia "do"
    Dodatkowo wspoldzedne i jesli bicie usuwa pionek pomiedzy
    """
    def wykonaj_pojedynczy_ruch(self, ruch_z, ruch_do):
        pionek = self.slownikPozycji[ruch_z]
        if pionek.jest_damka is False:
            self.ostatni_ruch_pionkiem = self.kolejka

        if (abs(ruch_z[0] - ruch_do[0]) == 2 and abs(ruch_z[1] - ruch_do[1]) == 2):  # ruch jest biciem

            poz_pomiedzy = (min(ruch_z[0], ruch_do[0]) + 1, min(ruch_z[1], ruch_do[1]) + 1)
            pionek_na_pozycji_pomiedzy = self.slownikPozycji.get(poz_pomiedzy)

            if pionek_na_pozycji_pomiedzy.gracz.get_kolor_string() == pionek.gracz.get_kolor_string():  # jesli ten sam gracz
                raise ValueError("Upss, co jest nie tak, na pozycji " + str(poz_pomiedzy) + " stoi pionek gracza o kolorze " + pionek_na_pozycji_pomiedzy.gracz.get_kolor_string())
            else:
                self.usun_pionek_z_planszy(pionek_na_pozycji_pomiedzy)

        return self.przesun_pionek_na_dana_pozycje(pionek, ruch_do)

    """
        Wykonuje sekwencyjnie kolejne ruchy podane w tablicy sciezka_ruchu
    """
    def wykonaj_wskazane_ruchy(self, sciezka_ruchu):

        for i in range(len(sciezka_ruchu) - 1):
            self.wykonaj_pojedynczy_ruch(sciezka_ruchu[i], sciezka_ruchu[i + 1])
        return

    """
        Zwraca True jesli dana pozycja jest na planszy
    """
    def sprawdz_czy_pozycja_na_planszy(self, pozycja):
        if pozycja[0] < 0 or pozycja[0] >= self.szerokosc or pozycja[1] < 0 or pozycja[1] >= self.wysokosc:
            return False
        return True

    """
    Ta metoda na potrzeby generowania mozliwych ruchow
    Parametry
    pozycja_startowa- tupla z indeksem pola z ktorego generujemy ruch
    czy_poprzeni_ruch_byl_biciem - flaga zeby wiedziec kiedy mozna kontynuowac / zakonczyc generowanie sciezki
    drzewo_obowiazkowych_bic - drzewo kolejnych pozycji budowane w celu generacji dopuszczalnych sciezkek bic
    lista_mozliwych_ruchow - lista z dopuszczalnymi pozycjami ktore nie sa biciami
    """
    def generuj_mozliwe_ruchy(self, pozycja_startowa, czy_poprzedni_ruch_byl_biciem, drzewo_obowiazkowych_bic, lista_mozliwych_ruchow):
        pionek = self.slownikPozycji.get(pozycja_startowa)
        for ruch in pionek.get_wektory_ruchu():
            log.debug("Przetwarzam sciezke od " + pozycja_to_str(pozycja_startowa) + " i ruch o wektor " + str(ruch))

            pozycja_do = (pozycja_startowa[0] + ruch[0], pozycja_startowa[1] + ruch[1])

            # nie uwzgledniaj ruchow wychodzacych poza plansze
            if not self.sprawdz_czy_pozycja_na_planszy(pozycja_do):
                log.debug("     Ruch poza plansza")
                continue

            # sprawdz czy na danej pozycji stoi pionek i czy jest to pionek gracza
            if self.slownikPozycji.get(pozycja_do) is not None:
                pionek_na_pozycji_do = self.slownikPozycji[pozycja_do]
                if pionek_na_pozycji_do.gracz == self.get_gracz_wykonujacy_ruch():  # jesli gracz to pomic
                    log.debug("     Tu stoi pionek gracza")
                    continue

                # mamy potencjalne bicie, sprawdzamy czy pole za pionkiem jest wolne
                pozycja_po_biciu = (pozycja_do[0] + ruch[0], pozycja_do[1] + ruch[1])

                if not self.sprawdz_czy_pozycja_na_planszy(pozycja_po_biciu):  # nie uwzgledniaj ruchow wychodzacych poz plansze
                    log.debug("     Bicie wychodzi poza plansze")
                    continue

                if self.slownikPozycji.get(pozycja_po_biciu) is not None:
                    log.debug("     Za bitym pionkiem stoi inny pionek")
                    continue

                log.debug("Mamy bicie, a nastepna mozliwa pozycja to " + pozycja_to_str(pozycja_po_biciu))

                # jesli pierwsze bicie tworzymy drzewo bic z danj pozycji i dodajemy ja jako wezel glowny
                if czy_poprzedni_ruch_byl_biciem is False and drzewo_obowiazkowych_bic is None:
                    log.debug("Tworze korzen drzewa z wartoscia " + str(pozycja_startowa))
                    drzewo_obowiazkowych_bic = WezelDrzewa(pozycja_startowa)

                # w przciwnym wypadku dodajemy jako wezel_potomny
                nowy_wezel_drzewa = WezelDrzewa(pozycja_po_biciu)
                drzewo_obowiazkowych_bic.dodaj_nowy_wezel(nowy_wezel_drzewa)

                # teraz wykonujemy ruch ( modifukujemy stan planszy !)
                # musimy to zrobic aby uniknac scenariusza zapetlenia damki
                self_copy = copy.deepcopy(self)
                ruch_zakonczony_promocja = self_copy.wykonaj_pojedynczy_ruch(pozycja_startowa, pozycja_po_biciu)

                if ruch_zakonczony_promocja is not True:
                    self_copy.generuj_mozliwe_ruchy(pozycja_po_biciu, True, nowy_wezel_drzewa, [])

            else:  # nie ma innego pionka na pozycji_do
                if czy_poprzedni_ruch_byl_biciem is True:
                    log.debug("     To pole jest wolne ale bylo juz bicie")

                if czy_poprzedni_ruch_byl_biciem is not True:
                    log.debug("      Pole jest wolne, mozloiwy ruch, ale bez bicia")
                    lista_mozliwych_ruchow.append([pozycja_startowa, pozycja_do])

        return drzewo_obowiazkowych_bic

    def mozliwe_ruchy(self, gracz=None):

        if gracz is None:
            gracz = self.get_gracz_wykonujacy_ruch()

        sciezki_obowiazkowych_bic = []
        mozliwe_ruchy = []
        for pionek in gracz.pionki:
            self_copy = copy.deepcopy(self)
            pozycja_startowa = pionek.get_pozycja()
            drzewo_obowiazkowych_bic = None

            drzewo_obowiazkowych_bic = self_copy.generuj_mozliwe_ruchy(pozycja_startowa, False, drzewo_obowiazkowych_bic, mozliwe_ruchy)
            if drzewo_obowiazkowych_bic is not None and drzewo_obowiazkowych_bic.puste() is False:
                sciezki_bic_z_pozycji_startowej = drzewo_obowiazkowych_bic.generujSciezki(drzewo_obowiazkowych_bic)
                sciezki_obowiazkowych_bic.extend(sciezki_bic_z_pozycji_startowej)

        # bicie jest obowiazkowe, dopiero gdy nie ma bicia mozna wybrac inny ruch
        if len(sciezki_obowiazkowych_bic) != 0:
            return sciezki_obowiazkowych_bic
        else:
            return mozliwe_ruchy

    """
        Pomocnicze metody do inicjalizacji i rysowania planszy
    """
    def wstaw_pionek_na_plansze(self, pionek):
        if pionek.gracz.jest_koloru_bialego():
            self.biale_pionki.append(pionek)
            self.slownikPozycji[pionek.get_pozycja()] = pionek
        elif pionek.gracz.jest_koloru_czarnego():
            self.czarne_pionki.append(pionek)
            self.slownikPozycji[pionek.get_pozycja()] = pionek

    """
        Ustaw pionki na szachownicy
    """
    def zainicjalizuj_plansze(self):

        for i in range(self.szerokosc):
            self.wstaw_pionek_na_plansze(Pionek(self.bialy_gracz, (i, (i + 1) % 2)))
            self.wstaw_pionek_na_plansze(Pionek(self.czarny_gracz, (i, self.wysokosc - (i % 2) - 1)))

        for i in range(4):
            self.wstaw_pionek_na_plansze(Pionek(self.czarny_gracz, (i * 2, self.wysokosc - 3)))
            self.wstaw_pionek_na_plansze(Pionek(self.bialy_gracz, (i * 2 + 1, 2)))

    """
        Aktualizuj stanPlanszy uzywany w metodzie rysujaPlansze
    """
    def zaktualizujStanPlanszy(self):

        for i in range(self.szerokosc):
            for j in range(self.wysokosc):
                self.stanPlanszy[i][j] = " "

        for pionek in [item for sublist in self.pionki for item in sublist]:  # iteruj po splaszczonej liscie z wszystkimi pionkami
            self.stanPlanszy[pionek.get_pozycja()[1]][pionek.get_pozycja()[0]] = pionek.get_znak_pionka()

    """
    Narysuj plansze w UTF-8
    """
    def rysujPlansze(self):

        self.zaktualizujStanPlanszy()
        linie = []
        linie.append('  ')
        # Numery u gory planszy
        linie.append('      ' + '   '.join(map(str, list(range(self.szerokosc)))))
        # Gora plaszny
        linie.append('    ╭' + ('───┬' * (self.szerokosc - 1)) + '───╮')

        # wiersze
        for num, wiersz in enumerate(self.stanPlanszy[:-1]):
            linie.append(chr(num + 65) + '  ' + ' │ ' + ' │ '.join(wiersz) + ' │')
            linie.append('    ├' + ('───┼' * (self.szerokosc - 1)) + '───┤')

        # Dol planszy
        linie.append(chr(self.wysokosc + 64) + '  ' + ' │ ' + ' │ '.join(self.stanPlanszy[-1]) + ' │')
        linie.append('    ╰' + ('───┴' * (self.szerokosc - 1)) + '───╯')

        #log.info('\n'.join(linie))
        print('\n'.join(linie))
