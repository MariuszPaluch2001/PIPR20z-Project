from gracz import Gracz


class Pionek(object):

    def __init__(self, gracz, pozycja, damka=False):
        self.gracz = gracz
        self.pozycja = pozycja
        self.jest_damka = damka

    """
    Funkcja definiuje w jakich kierunkach moze poruszac sie pionek (lub damka)
    Rozmieszenie kolorow na planszy jest niezmienne i ma wplyw na orientacje(wartosci) wektorow ruchu
    """
    def get_wektory_ruchu(self):
        if self.jest_damka is False:
            if self.gracz.kolor == Gracz.BIALY:
                return [(-1, 1), (1, 1)]
            elif self.gracz.kolor == Gracz.CZARNY:
                return [(-1, -1), (1, -1)]
        else:
            return [(-1, -1), (1, -1), (1, 1), (-1, 1)]

    def get_pozycja(self):
        return self.pozycja

    def set_pozycja(self, pozycja):
        self.pozycja = pozycja

    def get_znak_pionka(self):
        if self.jest_damka is False and self.gracz.kolor == Gracz.CZARNY:
            return '◆'
        elif self.jest_damka is False and self.gracz.kolor == Gracz.BIALY:
            return '◇'
        elif self.jest_damka is True and self.gracz.kolor == Gracz.BIALY:
            return '♔'
        elif self.jest_damka is True and self.gracz.kolor == Gracz.CZARNY:
            return '♚'
        else:
            return '?'

    def __str__(self):
        return "Pionek " + self.get_znak_pionka() + " na pozycji " + str(self.get_pozycja())
