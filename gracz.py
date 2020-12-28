class Gracz(object):

    def __init__(self, color):
        """
            Tworzy gracza
        """ 
        self.color = color

    def wczytaj_nastepny_ruch(self, plansza):
        #statement1 = "Select one of your tokens eg. " + chr(b.whitelist[0][0]+97) + str(b.whitelist[0][1])
        print("Teraz kolej na gracza " + ( '◆' if self.color != 0 else '◇'))
        
        while True: # Dopoki poprawna wartosc pola
            ruch = []
        
            print("Wybierz pozycje pionka ktorym wykonasz ruch: ")
            ruch.append(tuple(input().lower()))
            print("Wybierz docelowa pozycje: ")
            ruch.append(tuple(input().lower()))
            
            if len(ruch[0]) != 2  or len(ruch[1]) != 2 :
                print("Ups, niepoprawny ruch")
                continue
            
            ruch_z = (int(ruch[0][1]), ord(ruch[0][0]) - 97)
            ruch_do = (int(ruch[1][1]), ord(ruch[1][0]) - 97)
        
            # Is the piece we want to move one we own?
            if not (ruch_z in plansza.pionki[self.color]):
                print("Ups, to nie twoj pionek, wybierz go z listy (wiersz, kolumna) " + str(plansza.pionki[self.color]))
                continue
            break
        move = (ruch_z, ruch_do)
        return move