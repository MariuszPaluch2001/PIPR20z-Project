from gracz import Gracz

class Pionek(object):

    # BLACK = 1
    # WHITE = 0

    def __init__(self, gracz, pozycja, damka = False):
        """
            Tworzy pionka
        """
        self.gracz = gracz
        self.pozycja = pozycja
        self.jest_damka = damka

    #definiuje w jakich kierunkach moze poruszac sie pionek (lub damka)
    def get_wektory_ruchu(self):
        if self.jest_damka is False: # to jest pewna niepokajaca zelznosc pionka od jego koloru gracza !
            if self.gracz.kolor == Gracz.WHITE:
                return [(-1,1),(1,1)]
            elif self.gracz.kolor == Gracz.BLACK:
                return [(-1,-1),(1,-1)]
        else:
            return [(-1,-1),(1,-1),(1,1),(-1,1)]

    def zamien_w_damke(self):
        if self.jest_damka != True:
            self.jest_damka = True

    def get_pozycja(self):
        return self.pozycja

    def set_pozycja(self, pozycja):
        self.pozycja = pozycja

    def get_znak_pionka(self):
        if self.jest_damka is False and self.gracz.kolor == Gracz.BLACK:
            return '◆'
        elif self.jest_damka is False and self.gracz.kolor == Gracz.WHITE:
            return '◇'
        elif self.jest_damka is True and self.gracz.kolor == Gracz.WHITE:
            return '♔'
        elif self.jest_damka is True and self.gracz.kolor == Gracz.BLACK:
            return '♚'
        else:
            return '?'

    def __str__(self):
        return "Pionek " + self.get_znak_pionka() + " na pozycji " + str(self.get_pozycja())