from plansza import *
from gracz import *
# Setup variables
width = 8
height = 8
firstPlayer = 0

print("Witamy w warcabach ... ")
p = Plansza(width, height, firstPlayer)
p.rysujPlansze()

g1 = Gracz(Plansza.WHITE)
g2 = Gracz(Plansza.BLACK)
runda = 1

while True:

    if runda % 2 != 0:
        ruch = g1.wczytaj_nastepny_ruch(p)
        p.wykonaj_ruch(ruch[0],ruch[1],g1)
    else:
        ruch = g2.wczytaj_nastepny_ruch(p)
        p.wykonaj_ruch(ruch[0],ruch[1],g2)
   
    p.rysujPlansze()
        
    runda += 1
    # # Then it is the computers turn
    # temp = minMax2(b)
    # b = temp[0]
    # print("**********COMPUTER MOVE**********")
    # b.printBoard()
    # if b.gameWon == b.WHITE:
    #     print("White Wins\nGame Over")
    #     break
    # elif b.gameWon == b.BLACK:
    #     print("Black Wins\nGame Over")
    #     break
