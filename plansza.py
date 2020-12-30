from drzewo import *
from pionek import *

class Plansza(object):
    BLACK = 1
    WHITE = 0
    NOTDONE = -1
    def __init__(self, wysokosc, szerokosc, firstPlayer):
        """
            Tworzy plansze
        """
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc

        # Lista z pionkami obu graczy
        self.czarne_pionki = []
        self.biale_pionki = []
        self.pionki = []
   
        self.pionki = [self.biale_pionki, self.czarne_pionki]

        # aktualna plansza ze znakami do odrysowania
        self.stanPlanszy = [[' '] * self.szerokosc for x in range(self.wysokosc)]
        self.slownikPozycji= {} 
    
    def sprawdz_czy_zwyciezca(self):

        if  len(self.biale_pionki == 0):
            return self.BLACK
        elif len(self.czarne_pionki == 0):
            return self.WHITE
        else:
            return None

    #do inicjalizacji
    def wstaw_pionek_na_plansze(self, pionek):
        if pionek.gracz.kolor == self.WHITE:
            self.biale_pionki.append(pionek)
            self.slownikPozycji[pionek.get_pozycja()] = pionek
        elif pionek.gracz.kolor == self.BLACK:
            self.czarne_pionki.append(pionek)
            self.slownikPozycji[pionek.get_pozycja()] = pionek
            
    def zainicjalizuj_plansze(self,gracz1,gracz2):

        for i in range(self.szerokosc):
            self.wstaw_pionek_na_plansze(Pionek(gracz1, (i, (i+1)%2)))
            self.wstaw_pionek_na_plansze(Pionek(gracz2, (i, self.wysokosc - (i%2) - 1)))
        
        for i in range(4):
            self.wstaw_pionek_na_plansze(Pionek(gracz2, (i*2, self.wysokosc - 3)))
            self.wstaw_pionek_na_plansze(Pionek(gracz1, (i*2+1, 2)))
          
        gracz1.set_pionki(self.biale_pionki)
        gracz2.set_pionki(self.czarne_pionki)

 
    def zaktualizujStanPlanszy(self):
        """
            Aktualizuj stanPlanszy uwzgledniajac pozycje bialych i czarnych pinkow
        """

        for i in range(self.szerokosc):
            for j in range(self.wysokosc):
                self.stanPlanszy[i][j] = " "

        for pionek in  [item for sublist in self.pionki for item in sublist]: #iteruj po splaszczonej liscie z wszystkimi pionkami
            self.stanPlanszy[pionek.get_pozycja()[1]][pionek.get_pozycja()[0]] = pionek.get_znak_pionka()

        # #for pionek in  [item for sublist in self.pionki for item in sublist]: #iteruj po splaszczonej liscie z wszystkimi pionkami
        
        # for pionek in self.biale_pionki:
        #     print(pionek)
        #     self.stanPlanszy[pionek.get_pozycja()[1]][pionek.get_pozycja()[0]] = pionek.get_znak_pionka()

        # for pionek in self.czarne_pionki:
        #     self.stanPlanszy[pionek.get_pozycja()[1]][pionek.get_pozycja()[0]] = pionek.get_znak_pionka()


    #funkcja ma sprawdzic czy dany ruch jest biciem (uwaga, bic mozna tez w tyl)
    # nalezy zwrocic pozycje do zbicia
    def warunkowe_bicie(self, ruch_z, ruch_do, gracz):
        pionki_gracza = self.pionki[gracz.color]
        pionki_drugiego_gracza = self.pionki[(gracz.color+1) % 2]

        if (abs(ruch_z[0] - ruch_do[0]) == 2 and abs(ruch_z[1] - ruch_do[1]) == 2):
            poz_pomiedzy = (min(ruch_z[0], ruch_do[0]) + 1, min(ruch_z[1], ruch_do[1]) + 1 )
            pionki_drugiego_gracza.remove(poz_pomiedzy)

    def wykonaj_pojedynczy_ruch(self, ruch_z, ruch_do, gracz):
        pionki_gracza = self.pionki[gracz.color]
        self.warunkowe_bicie(ruch_z, ruch_do, gracz)
        pionki_gracza[pionki_gracza.index(ruch_z)] = ruch_do

  
  
    def sprobuj_wykonac_ruch(self, ruch_z, ruch_do, gracz):
        """
            Wykonaj ruch
        """
        if ruch_do[0] < 0 or ruch_do[0] >= self.szerokosc or ruch_do[1] < 0 or ruch_do[1] >= self.wysokosc:
            raise Exception("Ruch poza plansze !!!")

        pozycja_zajeta_przez_czarny_pionek = ruch_do in self.czarne_pionki
        pozycja_zajeta_przez_bialy_pionek = ruch_do in self.biale_pionki
        
        if not (pozycja_zajeta_przez_czarny_pionek or pozycja_zajeta_przez_bialy_pionek):

            self.wykonaj_pojedynczy_ruch(ruch_z, ruch_do, gracz)
            self.zaktualizujStanPlanszy()

            # self.turn = self.BLACK
            # self.gameWon = winLoss
        else:
            raise Exception("Pozycja zajeta")

    #sprawdza czy podana pozycja istnieje na planszy
    def sprwadz_czy_pozycja_na_planszy(self, pozycja):
        if pozycja[0] < 0 or pozycja[0] >= self.szerokosc or pozycja[1] < 0 or pozycja[1]  >= self.wysokosc:
                return False
        return True
    

    def generuj_mozliwe_ruchy(self, pozycja_startowa, pionek, gracz_wykonujacy_ruch, czy_poprzedni_ruch_byl_biciem, drzewo_obowiazkowych_bic, lista_mozliwych_ruchow):
        """
            Funkcja rekursyjna nowa
        """
        #nie uzywac pionek get.get_pozycja() tylko pozycja_startowa, bo inaczej bedzie caly czas taka sama
        for ruch in pionek.get_wektory_ruchu():
            print("Przetwarzam sciezke od " + str(pozycja_startowa) + " i ruch o wektor " + str(ruch))
            
            pozycja_do = (pozycja_startowa[0] + ruch[0], pozycja_startowa[1] + ruch[1])
      
            if not self.sprwadz_czy_pozycja_na_planszy(pozycja_do): # nie uwzgledniaj ruchow wychodzacych poz plansze
                print("Ruch poza plansza")
                continue       
           
            # sprwadz czy na danej pozycji stoi pionek i kto jest wlascicelem
            if self.slownikPozycji.get(pozycja_do) is not None:
                pionek_na_pozycji_do = self.slownikPozycji[pozycja_do]
                if pionek_na_pozycji_do.gracz == gracz_wykonujacy_ruch: # jesli gracz to pomic
                    print("Tu stoi pionek gracza")
                    continue

                # mamy potencjalne bicie, sprawdzamy czy pole za pionkiem jest wolne
                pozycja_po_biciu = (pozycja_do[0] + ruch[0], pozycja_do[1] + ruch[1])

                if not self.sprwadz_czy_pozycja_na_planszy(pozycja_po_biciu): # nie uwzgledniaj ruchow wychodzacych poz plansze
                    print("Bicie wychodzi poza plansze")
                    continue   

                #musimy rekurencyjnie zbudowac drzewo potencjalnych ruchow pionka
                nastepna_mozliwa_pozycja = Drzewo(str(pozycja_po_biciu), [], True)
                print("Mamy bicie, a nastepna mozliwa pozycja to " + str(pozycja_po_biciu) )
                drzewo_obowiazkowych_bic.add_child(nastepna_mozliwa_pozycja)
                self.generuj_mozliwe_ruchy(pozycja_po_biciu, pionek, gracz_wykonujacy_ruch, True, nastepna_mozliwa_pozycja, []) 
            else: # nie ma tam innego pionka na pozycji_do
                if czy_poprzedni_ruch_byl_biciem is True:
                    print("To pole jest wolne ale bylo juz bicie")
            
                if czy_poprzedni_ruch_byl_biciem is not True:
                   print("Pole jest wolne")
                   lista_mozliwych_ruchow.append(pozycja_do)
          
       
        return drzewo_obowiazkowych_bic

            # # Sprawdz czy nic nie stoi na drodze pionka
            # czarny_pionek_na_pozycji_docelowej = pozycja_do in self.czarne_pionki
            # bialy_pionek_na_pozycji_docelowej  = pozycja_do in self.biale_pionki

            # # cos stoi na drudze, sprwadz czy obowiazkowe bicie ( musimy sledzic ktore sa biciem) ?
            # if czarny_pionek_na_pozycji_docelowej or bialy_pionek_na_pozycji_docelowej:
           
            #     # przerywamy jesli wlasicielem pionka jest gracz
            #     if czarny_pionek_na_pozycji_docelowej and gracz_wykonujacy_ruch.color == self.BLACK:
            #         continue
                
            #     if bialy_pionek_na_pozycji_docelowej and gracz_wykonujacy_ruch.color == self.WHITE:
            #         continue
                
            #     # skocz o jedna pozycje w w tym samym kierunku jak na poczatku
            #     pozycja_po_biciu = (pozycja_do[0] + ruch[0], pozycja_do[1] + ruch[1])

            #     if not self.sprwadz_czy_pozycja_na_planszy(pozycja_po_biciu): # nie uwzgledniaj ruchow wychodzacych poz plansze
            #         continue   


            #     nastepna_pozycja = Drzewo(str(pozycja_po_biciu), [], True)
            #     root_node.add_child(nastepna_pozycja)
            #     self.generuj_mozliwe_ruchy(pozycja_po_biciu, pionek, gracz_wykonujacy_ruch, True, nastepna_pozycja) 
            # else: 
            #     #pozycja docelowa pionka jest osiagalna tzn. nie ma tam innego pionka
            #     #if czy_poprzedni_ruch_byl_biciem is True:
            #     #sciezki_ruchu.append(sciezka_ruchu)
            #     #print("Condition " + str(czy_poprzedni_ruch_byl_biciem))
            #     if czy_poprzedni_ruch_byl_biciem is True:
            #         pass
                
            #     if czy_poprzedni_ruch_byl_biciem is not True:
            #        root_node.add_child(Drzewo(str(pozycja_do)))
                 
    
    def wypisz_mozliwe_ruchy(self, gracz):
        for pionek in gracz.pionki:
            pozycja_startowa = pionek.get_pozycja()
           
            drzewo_obowiazkowych_bic = Drzewo(str(pozycja_startowa)) 
            mozliwe_ruchy = []
            self.generuj_mozliwe_ruchy(pozycja_startowa, pionek, gracz, False, drzewo_obowiazkowych_bic, mozliwe_ruchy)
            
            if drzewo_obowiazkowych_bic.puste() == False:
                print("Musisz wykonac jedno z bic ponizej")
                print(drzewo_obowiazkowych_bic.printPaths(drzewo_obowiazkowych_bic))
            else:
                print("Dostepne osiagalne pozycje ")
                for i in mozliwe_ruchy:
                    print(str(i))
       

    def rysujPlansze(self):
        """
            Contains the unicode and other BS for printing the board
        """
        # Updates Game board
        self.zaktualizujStanPlanszy()
        lines = []
        # This prints the numbers at the top of the Game Board
        lines.append('      ' + '   '.join(map(str, list(range(self.szerokosc)))))
        # Prints the top of the gameboard in unicode
        lines.append('    ╭' + ('───┬' * (self.szerokosc-1)) + '───╮')
        
        # Print the boards rows
        for num, row in enumerate(self.stanPlanszy[:-1]):
            lines.append(chr(num+65) + ' ' +  str(num ) + ' │ ' + ' │ '.join(row) + ' │')
            lines.append('    ├' + ('───┼' * (self.szerokosc-1)) + '───┤')
        
        #Print the last row
        lines.append(chr(self.wysokosc+64) + ' ' + str(num + 1) +  ' │ ' + ' │ '.join(self.stanPlanszy[-1]) + ' │')

        # Prints the final line in the board
        lines.append('    ╰' + ('───┴' * (self.szerokosc-1)) + '───╯')
        print('\n'.join(lines))
