from plansza import Plansza
from gracz import Gracz
from drzewo import WezelDrzewa
from pionek import Pionek
import copy


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



def test_gleboka_kopia():
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
def test_zapetlenia_damki_v2():
    p = Plansza()

    startowy_pionek = Pionek(p.bialy_gracz,(4,7))
    startowy_pionek.zamien_w_damke()

    p.wstaw_pionek_na_plansze(Pionek(p.czarny_gracz,(3,4)))
    p.wstaw_pionek_na_plansze(Pionek(p.czarny_gracz,(5,4)))
    p.wstaw_pionek_na_plansze(Pionek(p.czarny_gracz,(3,6)))
    p.wstaw_pionek_na_plansze(Pionek(p.czarny_gracz,(5,6)))
    p.wstaw_pionek_na_plansze(Pionek(p.czarny_gracz,(7,4)))
    p.wstaw_pionek_na_plansze(startowy_pionek)
    p.gracz_wykonujacy_ruch = p.bialy_gracz
    assert len(p.czarny_gracz.pionki) == 5
    assert len(p.bialy_gracz.pionki) == 1
    assert len(p.gracz_wykonujacy_ruch.pionki) == 1

    p.rysujPlansze()
    p.wykonaj_wskazane_ruchy(p.mozliwe_ruchy()[0])
    p.rysujPlansze()


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

    sciezki = p.mozliwe_ruchy()
    print(sciezki)
    assert len(sciezki) == 2
    assert len(sciezki[0]) == 2
    assert len(sciezki[1]) == 2
    assert (5, 5) == sciezki[0][0]
    assert (3, 3) == sciezki[0][1]
    assert (5, 5) == sciezki[1][0]
    assert (3, 7) == sciezki[1][1]

def test_podwojnego_bicia():
    p = Plansza()

    damka = Pionek(p.czarny_gracz,(5,7), True)
    p.gracz_wykonujacy_ruch = p.czarny_gracz

    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(2,2)))

    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(0,2)))
    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(2,4)))
    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(4,6)))
    p.wstaw_pionek_na_plansze(damka)

    p.rysujPlansze()



def test_drzewo():
    print(type((2,2)))
    a = WezelDrzewa(((2,2)))
    b = WezelDrzewa((1,3))
    a.dodaj_nowy_wezel(b)
    d = WezelDrzewa((0,4))
    b.dodaj_nowy_wezel(d)
    a.dodaj_nowy_wezel(WezelDrzewa((5,5)))
    sciezki = a.generujSciezki(a)
    print(sciezki)
