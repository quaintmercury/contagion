"""Simple grid model of contagion"""

import mvc  # for Listenable
import enum
from typing import List, Tuple

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
import random


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
        self.next_state = Health.vulnerable
        self._time_in_state = 0
    def step(self):
        # FIXME soon
        pass

    def tick(self):
        """Time passes"""
        self._time_in_state += 1
        if self.state != self.next_state:
            self.state = self.next_state
            self.notify_all("newstate")
            # Reset clock
            self._time_in_state = 0

    def infect(self):
        """Called by another individual spreading germs.
        May also be called on "patient 0" to start simulation.
        """
        if self.state == Health.vulnerable:
            self.next_state = Health.asymptomatic

class Population(mvc.Listenable):
    def __init__(self, nrows: int, ncols: int):
        super().__init__()
        self.cells = []
        self.nrows = nrows
        self.ncols = ncols
        for rows in range(nrows):
            row_cells = []
            for col in range(ncols):
                row_cells.append(Individual())
            self.cells.append(row_cells)

    def step(self):
        """Determine next states"""
        log.debug("Population: Step")
        # Time passes
        for row in self.cells:
            for cell in row:
                cell.step()
        for row in self.cells:
            for cell in row:
                cell.tick()
        self.notify_all("timestep")

    def seed(self):
        """Patient zero"""
        row = random.randint(0,self.nrows-1)
        col = random.randint(0,self.ncols-1)
        self.cells[row][col].infect()
        self.cells[row][col].tick()

    def count_in_state(self, state: Health) -> int:
        """How many individuals are currently in state?"""

        ctr = 0
        for row in range(self.nrows):
            for col in range(self.ncols):
                if self.cells[row][col].state == state:
                    ctr += 1
        return ctr
