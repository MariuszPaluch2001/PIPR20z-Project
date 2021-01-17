from plansza import Plansza
from drzewo import WezelDrzewa
from gracz import Gracz
from pionek import Pionek
from ai import AI
from pomocnicze import *
from copy import deepcopy
import copy
import unittest



# jest zaloezenei w oparciu o ktore gra dziala -> czarne pionki ida w gore , biale w dol


def test_zainicjalizowanej_planszy():
    p = Plansza()
    p.zainicjalizuj_plansze()

    assert p.bialy_gracz.jest_koloru_bialego()
    assert p.czarny_gracz.jest_koloru_czarnego()
    assert len(p.biale_pionki) == 12
    assert len(p.czarne_pionki) == 12
    assert p.biale_pionki == p.bialy_gracz.pionki
    assert p.czarne_pionki == p.czarny_gracz.pionki
    assert len(p.bialy_gracz.pionki) == 12
    assert len(p.czarny_gracz.pionki) == 12
    p.rysujPlansze()
    p.gracz_wykonujacy_ruch = p.bialy_gracz
    assert len(p.mozliwe_ruchy()) == 7
    p.gracz_wykonujacy_ruch = p.czarny_gracz
    assert len(p.mozliwe_ruchy()) == 7


def test_koniec_gry():
    #czarny wygral, bialy nie ma ruchu
    p = Plansza()
    p.kolejka = 2
    assert p.get_gracz_wykonujacy_ruch() == p.bialy_gracz
    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(6,6)))
    p.wstaw_pionek_na_plansze(Pionek(p.czarny_gracz,(5,7)))
    p.wstaw_pionek_na_plansze(Pionek(p.czarny_gracz,(7,7)))
    p.rysujPlansze()
    assert p.koniec_gry() == p.czarny_gracz

    #bialy wygral, czarny nie ma ruchu
    p2 = Plansza()
    p2.kolejka = 3
    assert p2.get_gracz_wykonujacy_ruch() == p2.czarny_gracz
    p2.wstaw_pionek_na_plansze(Pionek(p2.czarny_gracz,(6,1)))
    p2.wstaw_pionek_na_plansze(Pionek(p2.bialy_gracz,(5,0)))
    p2.wstaw_pionek_na_plansze(Pionek(p2.bialy_gracz,(7,0)))
    p2.rysujPlansze()
    assert p2.koniec_gry() == p2.bialy_gracz

    #remis po 40 kolejnych ruchach damkami
    p3 = Plansza()
    p3.wstaw_pionek_na_plansze(Pionek(p2.czarny_gracz,(6,4)))
    p3.wstaw_pionek_na_plansze(Pionek(p2.bialy_gracz,(3,0)))
    p3.kolejka = 61
    p3.ostatni_ruch_pionkiem = 20
    p3.rysujPlansze()
    assert p3.koniec_gry() == Plansza.WYNIK_REMIS

    #bialy wygral, czarny nie ma pionkow
    p4 = Plansza()
    p4.kolejka = 3
    assert p4.get_gracz_wykonujacy_ruch() == p4.czarny_gracz
    p4.wstaw_pionek_na_plansze(Pionek(p4.bialy_gracz,(6,1)))
    p4.rysujPlansze()
    assert p2.koniec_gry() == p2.bialy_gracz

    #czarny wygral, bialy nie ma pionkow
    p5 = Plansza()
    p5.kolejka = 4
    assert p5.get_gracz_wykonujacy_ruch() == p5.bialy_gracz
    p5.wstaw_pionek_na_plansze(Pionek(p5.czarny_gracz,(6,1)))
    p5.rysujPlansze()
    assert p5.koniec_gry() == p5.czarny_gracz


def test_gleboka_kopia_planszy():
    p = Plansza()
    p.zainicjalizuj_plansze()

    p2 = copy.deepcopy(p)
    pionek = p.slownikPozycji.get((0,1))
    pionek_z_skopiowanej_planszy = p2.slownikPozycji.get((0,1))

    assert pionek.gracz.jest_koloru_bialego()
    assert pionek_z_skopiowanej_planszy != pionek
    assert pionek_z_skopiowanej_planszy.gracz.jest_koloru_bialego()

    p.get_gracz_wykonujacy_ruch().get_kolor_string() ==  p2.get_gracz_wykonujacy_ruch().get_kolor_string()

    p.usun_pionek_z_planszy(pionek) #usun bialy pionek

    assert len(p.czarne_pionki) == 12
    assert len(p.biale_pionki) == 11

    assert len(p2.czarne_pionki) == 12
    assert len(p2.biale_pionki) == 12

    assert len(pionek.gracz.pionki) == 11
    assert len(pionek_z_skopiowanej_planszy.gracz.pionki) == 12

    assert p.biale_pionki != p2.biale_pionki
    assert p.czarne_pionki != p2.czarne_pionki
    assert p.bialy_gracz != p2.bialy_gracz
    assert p.czarny_gracz != p2.czarny_gracz
    assert p.slownikPozycji != p2.slownikPozycji

    for pionek in p.slownikPozycji.values():
        assert pionek not in p2.slownikPozycji.values()


"""
    Damka wykonuje cykl bic i wraca na pozycje startowa
"""
def test_zapetlenia_damki():
    p = Plansza()

    damka = Pionek(p.czarny_gracz,(3,7), True)

    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(2,4)))
    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(4,4)))
    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(2,6)))
    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(4,6)))
    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(6,4)))
    p.wstaw_pionek_na_plansze(damka)
    assert p.get_gracz_wykonujacy_ruch() == p.czarny_gracz
    assert len(p.czarny_gracz.pionki) == 1
    assert len(p.bialy_gracz.pionki) == 5

    p.rysujPlansze()
    sciezki_str = []
    for sciezka in p.mozliwe_ruchy():
        sciezki_str.append(sciezka_to_str(sciezka))

    assert "H3 -> F1 -> D3 -> F5 -> D7" in sciezki_str
    assert "H3 -> F1 -> D3 -> F5 -> H3" in sciezki_str
    assert "H3 -> F5 -> D3 -> F1 -> H3" in sciezki_str
    assert "H3 -> F5 -> D7" in sciezki_str

    p.wykonaj_wskazane_ruchy(p.mozliwe_ruchy()[0])
    p.rysujPlansze()
    assert len(p.czarny_gracz.pionki) == 1
    assert len(p.bialy_gracz.pionki) == 1



"""
    Damka ma dwa alterantywne bicia z jednej pozycji
"""
def test_dwoch_alternatywnych_bic():
    p = Plansza()

    damka = Pionek(p.czarny_gracz,(5,5), True)
    p.gracz_wykonujacy_ruch = p.czarny_gracz

    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(4,4)))
    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(4,6)))
    p.wstaw_pionek_na_plansze(damka)

    p.rysujPlansze()

    #bicia sa obowiazkowe, wiec tylko 2 alternatywny bicia dostepne
    sciezki = p.mozliwe_ruchy()
    assert len(sciezki) == 2
    assert len(sciezki[0]) == 2
    assert len(sciezki[1]) == 2

    sciezki_str = []
    for sciezka in p.mozliwe_ruchy():
        sciezki_str.append(sciezka_to_str(sciezka))

    assert "F5 -> D3" in sciezki_str
    assert "F5 -> H3" in sciezki_str


def test_sciezek_bic():
    a = WezelDrzewa(((2,2)))
    b = WezelDrzewa((1,3))
    a.dodaj_nowy_wezel(b)
    d = WezelDrzewa((0,4))
    b.dodaj_nowy_wezel(d)
    a.dodaj_nowy_wezel(WezelDrzewa((5,5)))
    sciezki = a.generujSciezki(a)
    assert [(2, 2), (1, 3), (0, 4)] in sciezki
    assert [(2, 2), (5, 5)] in sciezki

# pionek osiagajacy koniec plaszy jest promowany do damki
# konczy to mozliwosc ruchu, nawet jesli jest bicie
# jezeli pionek jest juz damka to powyzsze nie obowiazuje
def test_promocji():
    p = Plansza()
    p.wstaw_pionek_na_plansze(Pionek(p.czarny_gracz,(5,2)))
    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(2,1)))
    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(4,1)))
    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(7,2)))
    p.kolejka = 1
    p.rysujPlansze()
    ruch = p.mozliwe_ruchy()

    print(sciezka_to_str(ruch[0]))
    assert sciezka_to_str(ruch[0]) == "C5 -> A3"

    #a teraz ta sama plansza, tylko z czarna damka
    p.czarne_pionki[0].jest_damka = True
    p.rysujPlansze()
    ruch = p.mozliwe_ruchy()

    print(sciezka_to_str(ruch[0]))
    assert sciezka_to_str(ruch[0]) == "C5 -> A3 -> C1"



