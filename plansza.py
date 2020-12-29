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

        # ustaw pozycje
        for i in range(szerokosc):
            self.czarne_pionki.append((i, (i+1)%2))
            self.biale_pionki.append((i, wysokosc - (i%2) - 1))

        self.pionki = [self.biale_pionki, self.czarne_pionki]

        # aktualna plansza ze znakami do odrysowania
        self.stanPlanszy = [[' '] * self.szerokosc for x in range(self.wysokosc)]

    def czy_koniec(self):
        if len(self.biale_pionki ) == 0:
            return "Zwyciężyły czarne"
        elif len(self.czarne_pionki ) == 0:
            return "Zwyciężyły białe"
        else:
            return 0



        #self.gameWon = self.NOTDONE
        #self.turn = firstPlayer
        #self.maxDepth = 10

    # # Generate an iterator for all of the moves
    # def iterWhiteMoves(self):
    #     """
    #         Main generator for white moves
    #     """
    #     for piece in self.whitelist:
    #         for move in self.iterWhitePiece(piece):
    #             yield move

    # def iterBlackMoves(self):
    #     """
    #         Main Generator for black moves
    #     """
    #     for piece in self.blacklist:
    #         for move in self.iterBlackPiece(piece):
    #             yield move

    # def iterWhitePiece(self, piece):
    #     """
    #         Generates possible moves for a white piece
    #     """
    #     return self.iterBoth(piece, ((-1,-1),(1,-1)))

    # def iterBlackPiece(self, piece):
    #     """
    #         Generates possible moves for a black piece
    #     """
    #     return self.iterBoth(piece, ((-1,1),(1,1)))

    # def iterBoth(self, piece, moves):
    #     """
    #         Handles the actual generation of moves for either black or white pieces
    #     """
    #     for move in moves:
    #         # Regular Move
    #         targetx = piece[0] + move[0]
    #         targety = piece[1] + move[1]
    #         # If the move is out of bounds don't move
    #         if targetx < 0 or targetx >= self.width or targety < 0 or targety >= self.height:
    #             continue
    #         target = (targetx, targety)
    #         # Check that there is nothing in the way of moving to the target
    #         black = target in self.blacklist
    #         white = target in self.whitelist
    #         if not black and not white:
    #             yield (piece, target, self.NOTDONE)
    #         # There was something in the way, can we jump it?
    #         else:
    #             # It has to be of the opposing color to jump
    #             if self.turn == self.BLACK and black:
    #                 continue
    #             elif self.turn == self.WHITE and white:
    #                 continue
    #             # Jump proceeds by adding the same movement in order to jump over the opposing
    #             # piece on the checkerboard
    #             jumpx = target[0] + move[0]
    #             jumpy = target[1] + move[1]
    #             # If the jump is going to be out of bounds don't do it.
    #             if jumpx < 0 or jumpx >= self.width or jumpy < 0 or jumpy >= self.height:
    #                 continue
    #             jump = (jumpx, jumpy)
    #             # Check that there is nothing in the jumpzone
    #             black = jump in self.blacklist
    #             white = jump in self.whitelist
    #             if not black and not white:
    #                 yield (piece, jump, self.turn)

    def zaktualizujStanPlanszy(self):
        """
            Aktualizuj stanPlanszy uwzgledniajac pozycje bialych i czarnych pinkow
        """
        for i in range(self.szerokosc):
            for j in range(self.wysokosc):
                self.stanPlanszy[i][j] = " "
        for pionek in self.czarne_pionki:
            self.stanPlanszy[pionek[1]][pionek[0]] = '◆'
        for pionek in self.biale_pionki:
            self.stanPlanszy[pionek[1]][pionek[0]] = '◇'

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

    def wykonaj_ruch(self, ruch_z, ruch_do, gracz):
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

    # # Movement of pieces
    # def moveSilentBlack(self, moveFrom, moveTo, winLoss):
    #     """
    #         Move black piece without printing
    #     """
    #     if moveTo[0] < 0 or moveTo[0] >= self.width or moveTo[1] < 0 or moveTo[1] >= self.height:
    #         raise Exception("That would move black piece", moveFrom, "out of bounds")
    #     black = moveTo in self.blacklist
    #     white = moveTo in self.whitelist
    #     if not (black or white):
    #         self.blacklist[self.blacklist.index(moveFrom)] = moveTo
    #         self.updateBoard()
    #         self.turn = self.WHITE
    #         self.gameWon = winLoss
    #     else:
    #         raise Exception

    # def moveSilentWhite(self, moveFrom, moveTo, winLoss):
    #     """
    #         Move white piece without printing
    #     """
    #     if moveTo[0] < 0 or moveTo[0] >= self.width or moveTo[1] < 0 or moveTo[1] >= self.height:
    #         raise Exception("That would move white piece", moveFrom, "out of bounds")
    #     black = moveTo in self.blacklist
    #     white = moveTo in self.whitelist
    #     if not (black or white):
    #         self.whitelist[self.whitelist.index(moveFrom)] = moveTo
    #         self.updateBoard()
    #         self.turn = self.BLACK
    #         self.gameWon = winLoss
    #     else:
    #         raise Exception

    # def moveBlack(self, moveFrom, moveTo, winLoss):
    #     """
    #         Move a black piece from one spot to another. \n winLoss is passed as either 0(white)
    #         or 1(black) if the move is a jump
    #     """
    #     self.moveSilentBlack(moveFrom, MoveTo, winLoss)
    #     self.printBoard()

    # def moveWhite(self, moveFrom, moveTo, winLoss):
    #     """
    #         Move a white piece from one spot to another. \n winLoss is passed as either 0(white)
    #         or 1(black) if the move is a jump
    #     """
    #     self.moveSilentWhite(moveFrom, moveTo, winLoss)
    #     self.printBoard()


    # def __str__(self):
    #     return self.__unicode__().encode('utf-8')

    def rysujPlansze(self):
        """
            Contains the unicode and other BS for printing the board
        """
        # Updates Game board
        self.zaktualizujStanPlanszy()
        lines = []
        # This prints the numbers at the top of the Game Board
        lines.append('    ' + '   '.join(map(str, list(range(self.szerokosc)))))
        # Prints the top of the gameboard in unicode
        lines.append('  ╭' + ('───┬' * (self.szerokosc-1)) + '───╮')

        # Print the boards rows
        for num, row in enumerate(self.stanPlanszy[:-1]):
            lines.append(chr(num+65) + ' │ ' + ' │ '.join(row) + ' │')
            lines.append('  ├' + ('───┼' * (self.szerokosc-1)) + '───┤')

        #Print the last row
        lines.append(chr(self.wysokosc+64) + ' │ ' + ' │ '.join(self.stanPlanszy[-1]) + ' │')

        # Prints the final line in the board
        lines.append('  ╰' + ('───┴' * (self.szerokosc-1)) + '───╯')
        print('\n'.join(lines))

############## DEBUGGING
##############
#    def getWin(self):
#        return self.g
#
#    def setWin(self, val):
##        if val == 0:
##            raise Exception("Game won by white")
#        self.g = val

#    gameWon=property(getWin, setWin)
##############
##############
