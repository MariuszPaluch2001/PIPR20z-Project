#klasa gracz nie powinna przechowywac informacji o pionkach
class Gracz(object):

    def __init__(self, kolor):
        """
            Tworzy gracza
        """ 
        self.kolor = kolor
        self.pionki = []

    def set_pionki(self, pionki):
        self.pionki = pionki

    def wczytaj_nastepny_ruch(self, plansza, gracz):
        #statement1 = "Select one of your tokens eg. " + chr(b.whitelist[0][0]+97) + str(b.whitelist[0][1])
        print("Teraz kolej na gracza " + ( '◆' if self.kolor != 0 else '◇'))
        
        while True: # Dopoki poprawna wartosc pola
            ruch = []
        
            print("Lista mozliwych ruchow: ")
            plansza.wypisz_mozliwe_ruchy(gracz)

            print("Wybierz pozycje pionka ")
            ruch.append(tuple(input().lower()))

            ruch_z = (int(ruch[0][1]), ord(ruch[0][0]) - 97)
            
      

            # for i in plansza.iterator_mozliwych_posuniec(ruch_z,[(-1,-1),(1,-1)],self, None):
            #     print(i)

         
            ruch.append(tuple(input().lower()))
            if len(ruch[0]) != 2  or len(ruch[1]) != 2 :
                print("Ups, niepoprawny ruch")
                continue
            
            
            ruch_do = (int(ruch[1][1]), ord(ruch[1][0]) - 97)
        
            # Is the piece we want to move one we own?
            if not (ruch_z in plansza.pionki[self.kolor]):
                print("Ups, to nie twoj pionek, wybierz go z listy (wiersz, kolumna) " + str(plansza.pionki[self.color]))
                continue
            break
        move = (ruch_z, ruch_do)
        return move