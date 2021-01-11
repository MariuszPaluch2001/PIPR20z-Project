import logging

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) # or whatever
handler = logging.FileHandler('warcaby-utf8.log', 'w', 'utf-8') # or whatever
handler.setFormatter(logging.Formatter('%(name)s %(message)s')) # or whatever
root_logger.addHandler(handler)

class WezelDrzewa(object):
    "Generic tree node."
    def __init__(self, wartosc):
        self.wartosc = wartosc
        self.wezly_potomne = []
        # if children is not None:
        #     for child in children:
        #         self.add_child(child)

    def puste(self):
        return len(self.wezly_potomne) == 0 or self.wezly_potomne is None

    def dodaj_nowy_wezel(self, node):
        root_logger.debug("-->      Do wezla " + str(self.wartosc) + " dodaje wezel " + str(node.wartosc))
        self.wezly_potomne.append(node)

    # def traverse(self, node):
    #     if node is not None:
    #         for child_node in node.children:
    #             self.traverse(child_node)
    #     return


    def generujSciezki(self, wezel_startowy):
        # list to store path
        wszystkie_sciezki = []
        sciezka = []
        self.generujRekursywnieSciezki(wezel_startowy, sciezka, wszystkie_sciezki, 0)
        return wszystkie_sciezki

    def generujRekursywnieSciezki(self, wezel, sciezka, sciezki, pathLen):

        if wezel is None:
            return

        # if length of list is gre
        if(len(sciezka) > pathLen):
            sciezka[pathLen] = wezel.wartosc
        else:
            sciezka.append(wezel.wartosc)

        # increment pathLen by 1
        pathLen = pathLen + 1

        if len(wezel.wezly_potomne) == 0:
            #logging.debug("jestem w lisciu " + str(wezel.pozycja) +  "dodaje sciezke " + str(sciezka))
            # leaf node then print the list
            #self.printArray(sciezki, pathLen)
            sciezki.append(sciezka.copy())
        else:
            #logging.debug("nie jestem w lisciu " + str(wezel.pozycja)  +  "dodaje sciezke " + str(sciezka))
            # try for left and right subtree
            for wezel_potomny in wezel.wezly_potomne:
                self.generujRekursywnieSciezki(wezel_potomny,sciezka.copy(), sciezki, pathLen)

