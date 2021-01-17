from gracz import *
from warcaby import *
from ai import *
from pionek import *

"""
       alg. negamax vs losowe ruchy
"""


def test_funkcja_oceniajaca():
    p = Plansza()
    p.zainicjalizuj_plansze()
    p.kolejka = 1
    assert p.get_gracz_wykonujacy_ruch() == p.czarny_gracz

    ai = AI(8)
    p.usun_pionek_z_planszy(p.bialy_gracz.pionki[0])
    assert ai.funkcja_oceniajaca(p) == 12*10-11*10

    p.kolejka = 2

    ai2 = AI(8)
    assert p.get_gracz_wykonujacy_ruch() == p.bialy_gracz
    assert ai2.funkcja_oceniajaca(p) == 11*10-12*10

    p.bialy_gracz.pionki[0].jest_damka = True
    assert ai2.funkcja_oceniajaca(p) == 10*10-12*10+30


def test_negamax_1_ruch():

    p = Plansza()
    p.wstaw_pionek_na_plansze(Pionek(p.czarny_gracz,(3,0),True))
    p.wstaw_pionek_na_plansze(Pionek(p.czarny_gracz,(3,2)))
    p.wstaw_pionek_na_plansze(Pionek(p.czarny_gracz,(2,1)))
    p.wstaw_pionek_na_plansze(Pionek(p.czarny_gracz,(6,1)))
    p.wstaw_pionek_na_plansze(Pionek(p.czarny_gracz,(7,4)))
    p.wstaw_pionek_na_plansze(Pionek(p.czarny_gracz,(7,6)))
    p.wstaw_pionek_na_plansze(Pionek(p.bialy_gracz,(7,2)))
    p.rysujPlansze()
    p.kolejka = 2 # ruch bialego gracza

    ai2 = AI(2)
    r = ai2.zwroc_ruch(p)
    assert r is not None
    assert sciezka_to_str(r) == "C7 -> D6"


def test_ai_negamax_vs_losowy_gracz():
    gracze = []
    for i in range(1,3):
        ai = LosowyKomputer()
        gracze.append(ai)

    faworyt = InteligentnyKomputer()
    faworyt.ustaw_poziom_trudnosci(3)

    for g in gracze:
        wynik = Warcaby(faworyt, g).graj()
        assert wynik == faworyt


