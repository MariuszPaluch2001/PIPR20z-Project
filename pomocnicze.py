def sciezka_to_str(sciezka):
    if sciezka is None or len(sciezka) == 0:
        return "[ -> ]"
    sciezka_str = pozycja_to_str(sciezka[0])
    for ruch in sciezka[1:]:
        sciezka_str += " -> " + pozycja_to_str(ruch)
    return sciezka_str


def pozycja_to_str(pozycja):
    return (str(chr(pozycja[1] + 65)) + str(pozycja[0]))
