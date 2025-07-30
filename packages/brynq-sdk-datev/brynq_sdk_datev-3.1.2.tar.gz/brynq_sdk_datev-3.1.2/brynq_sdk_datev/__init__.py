from .lohn_und_gehalt import DatevLohnUndGehalt, schemas
from .lodas import DatevLodas
# from .lodas.datev_lodas_mapping import DatevLodasMapping
from .lodas.datev_mapping import DatevMapping



class Datev:
    def __init__(self, berater_nr: int = None, mandanten_nr: int = None, debug: bool = False):
        self.berater_nr = berater_nr
        self.mandanten_nr = mandanten_nr
        self.lodas = DatevLodas(berater_nr, mandanten_nr)
        self.lohn_und_gehalt = DatevLohnUndGehalt(debug=debug)
