"""Simple grid model of contagion"""

import mvc  # for Listenable
import enum
from typing import List, Tuple

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)



class Health(enum.Enum):
    """Each individual is one discrete state of health"""
    vulnerable = enum.auto()
    asymptomatic = enum.auto()
    symptomatic = enum.auto()
    recovered = enum.auto()
    dead = enum.auto()

    def __str__(self) -> str:
        return self.name


class Individual(mvc.Listenable):
    def __init__(self):
        super().__init__()
        self.state = Health.vulnerable

class Population(mvc.Listenable):
    def __init__(self, nrows: int, ncols: int):
        super().__init__()
        self.cells = []
        self.nrows = nrows
        self.ncols = ncols
        # YOU FILL THIS IN

    def seed(self):
        pass  #FIXME soon
