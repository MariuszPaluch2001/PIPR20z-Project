from plansza import *
from gracz import *
from drzewo import *


def test_plansza():
    print("")
    p = Plansza(8, 8, 0)

    g1 = Gracz(Plansza.WHITE)
    g2 = Gracz(Plansza.BLACK)

    startowy_pionek = Pionek(g1,(5,5))

    p.wstaw_pionek_na_plansze(Pionek(g2,(0,0)))
    p.wstaw_pionek_na_plansze(Pionek(g2,(2,2)))
    p.wstaw_pionek_na_plansze(Pionek(g2,(4,2)))
    p.wstaw_pionek_na_plansze(Pionek(g2,(4,4)))
    p.wstaw_pionek_na_plansze(startowy_pionek)

    g1.set_pionki(p.biale_pionki)
    g2.set_pionki(p.czarne_pionki)

    p.wypisz_mozliwe_ruchy(g1)
    p.rysujPlansze()

