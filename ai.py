#from copy import deepcopy
import copy
from pomocnicze import *
import logging

ai_logger= logging.getLogger()
ai_logger.setLevel(logging.DEBUG) # or whatever
handler = logging.FileHandler('ai-utf8.log', 'w', 'utf-8') # or whatever
handler.setFormatter(logging.Formatter('%(name)s %(message)s')) # or whatever
ai_logger.addHandler(handler)



class AI:

    def __init__(self,plansza,glebokosc_drzewa_przeszukiwan):
        self.startowa_plansza = plansza
        self.startowy_gracz = plansza.get_gracz_wykonujacy_ruch()
        self.maksymalna_glebokosc = glebokosc_drzewa_przeszukiwan

    
    def punkty_za_pionki(self,gracz):
        punkty = 0
        for pionek in gracz.pionki:
            if pionek.jest_damka == True:
                punkty += 30
            else:
                punkty += 10
        return punkty


    # Zwraca wartosc uzytecznosci planszy z punktu widzenia tylko gracza ai (gracza startowego )
    # im wieksza tym lepsza
    def funkcja_oceniajaca(self, plansza):
        gracz = plansza.get_gracz_wykonujacy_ruch()
        przeciwnik = plansza.get_przeciwnik()
        #ai_logger.debug("FO " + str(len(plansza.czarne_pionki)) + " " +  str(len(plansza.biale_pionki)))
        #if gracz.get_kolor_string() == self.startowy_gracz.get_kolor_string():
        #    ai_logger.debug("FOv1 " + gracz.get_kolor_string() + " " + self.startowy_gracz.get_kolor_string())
        return self.punkty_za_pionki(gracz) - self.punkty_za_pionki(przeciwnik)
        #else:
        #    ai_logger.debug("FOv2 " + gracz.get_kolor_string()  + "(" + ") " + self.startowy_gracz.get_kolor_string())
        #    return self.punkty_za_pionki(przeciwnik) - self.punkty_za_pionki(gracz)

    def negamax(self, plansza, glebokosc):
        if plansza is None:
            plansza = self.startowa_plansza

        if glebokosc is None:
            glebokosc = self.maksymalna_glebokosc

        if glebokosc == 0: #or plansza.zwyciezca() is not None:
            ai_logger.debug("\t"*(self.maksymalna_glebokosc - glebokosc) + "Poziom [" + str(self.maksymalna_glebokosc - glebokosc) + "]" + " - koncowy -  Ocena: " + str(self.funkcja_oceniajaca(plansza)) + " dla gracza " + plansza.get_gracz_wykonujacy_ruch().get_kolor_string() ) 
            return (plansza, self.funkcja_oceniajaca(plansza), None)

        max_ocena = float('-inf')
        max_plansza = None
        max_sciezka = None
        
        for sciezka in plansza.mozliwe_ruchy():

            ai_logger.debug("\t"*(self.maksymalna_glebokosc - glebokosc) + "Poziom [" + str(self.maksymalna_glebokosc - glebokosc)  + "] Przetwarzam ruch " + plansza.get_gracz_wykonujacy_ruch().get_kolor_string() + " "  + sciezka_to_str(sciezka)  ) 
            
            plansza_potomna = copy.deepcopy(plansza)
            plansza_potomna.wykonaj_wskazane_ruchy(sciezka)
            plansza_potomna.kolejka += 1
            (plansza_negamax, ocena_negamax, sciezka_negamax) = self.negamax(plansza_potomna, glebokosc-1)
            #ai_logger.debug("\t"*(self.maksymalna_glebokosc - glebokosc) + "Ocena: " + str(ocena_negamax)) 

            if -ocena_negamax > max_ocena:
                max_ocena = -ocena_negamax
                max_plansza = plansza_negamax
                max_sciezka = sciezka

        ai_logger.debug("\t"*(self.maksymalna_glebokosc - glebokosc) + "Poziom [" + str(self.maksymalna_glebokosc - glebokosc)  + "] Maksymalna sciezka to " + sciezka_to_str(max_sciezka) + " z ocena " + str(max_ocena))

        return (max_plansza,max_ocena,max_sciezka)



