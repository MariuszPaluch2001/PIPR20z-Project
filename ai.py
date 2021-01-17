import copy
from pomocnicze import *
import logging

ai_logger= logging.getLogger()
ai_logger.setLevel(logging.DEBUG) 
handler = logging.FileHandler('ai-utf8.log', 'w', 'utf-8') 
handler.setFormatter(logging.Formatter('%(name)s %(message)s'))
ai_logger.addHandler(handler)

class AI:

    def __init__(self,glebokosc_drzewa_przeszukiwan = 2):
        self.maksymalna_glebokosc = glebokosc_drzewa_przeszukiwan

    def set_maksymalna_glebokosc(self, glebokosc):
        self.maksymalna_glebokosc = glebokosc


    def punkty_za_pionki(self,gracz):
        punkty = 0
        for pionek in gracz.pionki:
            if pionek.jest_damka == True:
                punkty += 30
            else:
                punkty += 10
        return punkty

    """
        Zwraca wartosc uzytecznosci planszy z punktu widzenia gracza startowego klasy AI
    """
    def funkcja_oceniajaca(self, plansza):
        gracz = plansza.get_gracz_wykonujacy_ruch()
        przeciwnik = plansza.get_przeciwnik()
        return self.punkty_za_pionki(gracz) - self.punkty_za_pionki(przeciwnik)

    """
        algorytm negamax (wariacja minimax)
        https://en.wikipedia.org/wiki/Negamax
    """
    def negamax(self, plansza, glebokosc):

        if glebokosc == 0: #or plansza.zwyciezca() is not None:
            return (plansza, self.funkcja_oceniajaca(plansza), None)

        max_ocena = float('-inf')
        max_plansza = None
        max_sciezka = None
        
        for sciezka in plansza.mozliwe_ruchy():

            plansza_potomna = copy.deepcopy(plansza)
            plansza_potomna.wykonaj_wskazane_ruchy(sciezka)
            plansza_potomna.kolejka += 1
            (plansza_negamax, ocena_negamax, sciezka_negamax) = self.negamax(plansza_potomna, glebokosc-1)

            if -ocena_negamax > max_ocena:
                max_ocena = -ocena_negamax
                max_plansza = plansza_negamax
                max_sciezka = sciezka


        return (max_plansza,max_ocena,max_sciezka)
   
    """
        Zwraca najlepsza sciezke wg. algorytmu  
    """
    def zwroc_ruch(self, plansza):

        (najlepsza_plansza, najlepsza_ocena, najlepsza_sciezka) = self.negamax(plansza, self.maksymalna_glebokosc)

        return najlepsza_sciezka



